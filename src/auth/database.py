"""Multi-Tenant ACID Relational + Vector Chunk Store for Saral AI (Dual SQLite WAL & PostgreSQL pgvector)."""
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import logging
import os
from pathlib import Path
import sqlite3
from typing import Any, Dict, Iterator, List, Optional, Tuple
import uuid

from src.config import DATABASE_PATH

PROJECT_ROOT = Path(__file__).resolve().parents[2]

logger = logging.getLogger("MadadgaarAI.Auth.DB")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _format_pgvector(vec: List[float]) -> str:
    return "[" + ",".join(f"{float(v):.6f}" for v in vec) + "]"


def _parse_pgvector(raw: Any) -> List[float]:
    if isinstance(raw, (list, tuple)):
        return [float(x) for x in raw]
    if isinstance(raw, str):
        s = raw.strip().strip("[]")
        if not s:
            return []
        return [float(x) for x in s.split(",") if x.strip()]
    return []


class _PgCursorWrapper:
    """Thin DB-API wrapper exposing SQLite-like dict rows and `?` -> `%s` parameter conversion."""

    def __init__(self, cur: Any):
        self._cur = cur

    @property
    def rowcount(self) -> int:
        return int(getattr(self._cur, "rowcount", 0) or 0)

    def execute(self, sql: str, params: Tuple[Any, ...] | List[Any] = ()) -> "_PgCursorWrapper":
        pg_sql = sql.replace("?", "%s")
        self._cur.execute(pg_sql, params or ())
        return self

    def fetchone(self) -> Optional[Dict[str, Any]]:
        row = self._cur.fetchone()
        if row is None:
            return None
        if isinstance(row, dict):
            return row
        cols = [d[0] for d in (self._cur.description or [])]
        return dict(zip(cols, row))

    def fetchall(self) -> List[Dict[str, Any]]:
        rows = self._cur.fetchall() or []
        if not rows:
            return []
        if isinstance(rows[0], dict):
            return list(rows)
        cols = [d[0] for d in (self._cur.description or [])]
        return [dict(zip(cols, r)) for r in rows]


class _PgConnWrapper:
    def __init__(self, raw_conn: Any):
        self._conn = raw_conn

    def cursor(self) -> _PgCursorWrapper:
        return _PgCursorWrapper(self._conn.cursor())

    def execute(self, sql: str, params: Tuple[Any, ...] | List[Any] = ()) -> _PgCursorWrapper:
        return self.cursor().execute(sql, params)

    def commit(self) -> None:
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()


class SaralMultiTenantDB:
    """
    ACID Multi-Tenant Store for Users, Refresh Tokens, Tenant-Isolated Documents,
    Vector Chunks (with ON DELETE CASCADE), and Multi-Turn Chat Sessions/Messages.

    Automatically connects to PostgreSQL + pgvector when `DATABASE_URL=postgresql://...`
    is configured and reachable (psycopg v3 or psycopg2), and seamlessly falls back to
    local SQLite WAL mode otherwise.
    """

    def __init__(self, db_path: Path = DATABASE_PATH, database_url: Optional[str] = None):
        self.db_path = Path(db_path)
        self.database_url = (database_url if database_url is not None else (os.getenv("DATABASE_URL") or "")).strip()
        self._pg_driver: Optional[str] = None
        self.backend_name: str = "sqlite"
        self._detect_backend()
        self._init_schema()

    def _detect_backend(self) -> None:
        if not self.database_url.startswith(("postgresql://", "postgres://")):
            self.backend_name = "sqlite"
            return
        for mod_name in ("psycopg", "psycopg2"):
            try:
                mod = __import__(mod_name)
                test_conn = mod.connect(self.database_url, connect_timeout=3)
                test_conn.close()
                self._pg_driver = mod_name
                self.backend_name = f"postgresql+pgvector ({mod_name})"
                logger.info(f"SaralMultiTenantDB connected to PostgreSQL via {mod_name}.")
                return
            except Exception as exc:
                logger.debug(f"PostgreSQL driver {mod_name} unavailable/unreachable: {exc}")
        logger.info("PostgreSQL not reachable locally; using SQLite WAL backend for SaralMultiTenantDB.")
        self.backend_name = "sqlite"

    @property
    def is_postgres(self) -> bool:
        return self._pg_driver is not None

    @contextmanager
    def _connect(self) -> Iterator[Any]:
        if self.is_postgres:
            mod = __import__(self._pg_driver)
            raw = mod.connect(self.database_url)
            wrapper = _PgConnWrapper(raw)
            try:
                yield wrapper
            finally:
                wrapper.close()
            return

        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        try:
            yield conn
        finally:
            conn.close()

    def _init_schema(self):
        if self.is_postgres:
            mig_path = PROJECT_ROOT / "migrations" / "001_saral_multitenant_pgvector.sql"
            if mig_path.exists():
                sql_script = mig_path.read_text(encoding="utf-8")
                with self._connect() as conn:
                    conn.execute(sql_script)
                    conn.commit()
            return

        with self._connect() as conn:
            cur = conn.cursor()
            cur.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    google_sub TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    full_name TEXT NOT NULL,
                    avatar_url TEXT DEFAULT '',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS refresh_tokens (
                    jti TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    token_hash TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    revoked INTEGER NOT NULL DEFAULT 0,
                    replaced_by TEXT,
                    created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_rt_user ON refresh_tokens(user_id);

                CREATE TABLE IF NOT EXISTS user_documents (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    title TEXT NOT NULL,
                    source_type TEXT NOT NULL,
                    source_uri TEXT DEFAULT '',
                    mime_type TEXT NOT NULL DEFAULT 'text/plain',
                    file_size_bytes INTEGER NOT NULL DEFAULT 0,
                    content_sha256 TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    error_message TEXT DEFAULT '',
                    chunk_count INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(user_id, content_sha256)
                );
                CREATE INDEX IF NOT EXISTS idx_udoc_user ON user_documents(user_id, created_at DESC);

                CREATE TABLE IF NOT EXISTS document_chunks (
                    id TEXT PRIMARY KEY,
                    doc_id TEXT NOT NULL REFERENCES user_documents(id) ON DELETE CASCADE,
                    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    doc_title TEXT NOT NULL,
                    page_number INTEGER NOT NULL DEFAULT 1,
                    section_header TEXT NOT NULL DEFAULT 'Overview',
                    chunk_index INTEGER NOT NULL DEFAULT 0,
                    content TEXT NOT NULL,
                    token_count INTEGER NOT NULL DEFAULT 0,
                    embedding_json TEXT NOT NULL,
                    embedding_dim INTEGER NOT NULL DEFAULT 384,
                    created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_chunk_user ON document_chunks(user_id);
                CREATE INDEX IF NOT EXISTS idx_chunk_doc ON document_chunks(doc_id, user_id);

                CREATE TABLE IF NOT EXISTS chat_sessions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    title TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_csess_user ON chat_sessions(user_id, updated_at DESC);

                CREATE TABLE IF NOT EXISTS chat_messages (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
                    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    cited_chunk_ids_json TEXT NOT NULL DEFAULT '[]',
                    citations_json TEXT NOT NULL DEFAULT '[]',
                    created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_cmsg_sess ON chat_messages(session_id, user_id, created_at ASC);
                """
            )
            conn.commit()

    # ------------------------------------------------------------------
    # Users & Modes
    # ------------------------------------------------------------------

    def upsert_google_user(
        self, google_sub: str, email: str, full_name: str, avatar_url: str = ""
    ) -> Dict[str, Any]:
        now = _utc_now()
        clean_email = email.strip().lower()
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE google_sub = ? OR email = ?", (google_sub, clean_email))
            row = cur.fetchone()
            if row:
                cur.execute(
                    """
                    UPDATE users
                    SET google_sub = ?, email = ?, full_name = ?, avatar_url = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    (google_sub, clean_email, full_name.strip() or clean_email, avatar_url or "", now, row["id"]),
                )
                conn.commit()
                cur.execute("SELECT * FROM users WHERE id = ?", (row["id"],))
                return dict(cur.fetchone())

            uid = f"usr_{uuid.uuid4().hex[:16]}"
            cur.execute(
                """
                INSERT INTO users (id, google_sub, email, full_name, avatar_url, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (uid, google_sub, clean_email, full_name.strip() or clean_email, avatar_url or "", now, now),
            )
            conn.commit()
            cur.execute("SELECT * FROM users WHERE id = ?", (uid,))
            return dict(cur.fetchone())

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            return dict(row) if row else None

    # ------------------------------------------------------------------
    # Refresh Token Rotation Store
    # ------------------------------------------------------------------

    def store_refresh_token(self, jti: str, user_id: str, token_hash: str, expires_at: str) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO refresh_tokens (jti, user_id, token_hash, expires_at, revoked, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (jti, user_id, token_hash, expires_at, False if self.is_postgres else 0, _utc_now()),
            )
            conn.commit()

    def get_refresh_token(self, jti: str) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM refresh_tokens WHERE jti = ?", (jti,)).fetchone()
            return dict(row) if row else None

    def revoke_refresh_token(self, jti: str, replaced_by: Optional[str] = None) -> None:
        with self._connect() as conn:
            conn.execute(
                "UPDATE refresh_tokens SET revoked = ?, replaced_by = ? WHERE jti = ?",
                (True if self.is_postgres else 1, replaced_by, jti),
            )
            conn.commit()

    def revoke_all_user_refresh_tokens(self, user_id: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "UPDATE refresh_tokens SET revoked = ? WHERE user_id = ?",
                (True if self.is_postgres else 1, user_id),
            )
            conn.commit()

    # ------------------------------------------------------------------
    # Tenant-Isolated Documents & Chunks
    # ------------------------------------------------------------------

    def find_document_by_hash(self, user_id: str, content_sha256: str) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM user_documents WHERE user_id = ? AND content_sha256 = ?",
                (user_id, content_sha256),
            ).fetchone()
            return dict(row) if row else None

    def create_document(
        self,
        user_id: str,
        title: str,
        source_type: str,
        mime_type: str,
        file_size_bytes: int,
        content_sha256: str,
        source_uri: str = "",
    ) -> Dict[str, Any]:
        doc_id = f"doc_{uuid.uuid4().hex[:16]}"
        now = _utc_now()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO user_documents (
                    id, user_id, title, source_type, source_uri,
                    mime_type, file_size_bytes, content_sha256, status, error_message,
                    chunk_count, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending', '', 0, ?, ?)
                """,
                (
                    doc_id, user_id, title, source_type, source_uri,
                    mime_type, int(file_size_bytes), content_sha256, now, now,
                ),
            )
            conn.commit()
            row = conn.execute("SELECT * FROM user_documents WHERE id = ? AND user_id = ?", (doc_id, user_id)).fetchone()
            return dict(row)

    def update_document_status(
        self,
        doc_id: str,
        user_id: str,
        status: str,
        chunk_count: Optional[int] = None,
        error_message: str = "",
    ) -> None:
        now = _utc_now()
        with self._connect() as conn:
            if chunk_count is not None:
                conn.execute(
                    """
                    UPDATE user_documents
                    SET status = ?, chunk_count = ?, error_message = ?, updated_at = ?
                    WHERE id = ? AND user_id = ?
                    """,
                    (status, int(chunk_count), error_message, now, doc_id, user_id),
                )
            else:
                conn.execute(
                    """
                    UPDATE user_documents
                    SET status = ?, error_message = ?, updated_at = ?
                    WHERE id = ? AND user_id = ?
                    """,
                    (status, error_message, now, doc_id, user_id),
                )
            conn.commit()

    def list_user_documents(self, user_id: str) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM user_documents WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,),
            ).fetchall()
            return [dict(r) for r in rows]

    def get_user_document(self, doc_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM user_documents WHERE id = ? AND user_id = ?",
                (doc_id, user_id),
            ).fetchone()
            return dict(row) if row else None

    def delete_user_document(self, doc_id: str, user_id: str) -> bool:
        """Deletes document & cascades to all document_chunks strictly scoped to user_id."""
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM document_chunks WHERE doc_id = ? AND user_id = ?", (doc_id, user_id))
            cur.execute("DELETE FROM user_documents WHERE id = ? AND user_id = ?", (doc_id, user_id))
            deleted = cur.rowcount > 0
            conn.commit()
            return deleted

    def replace_document_chunks(self, doc_id: str, user_id: str, chunks: List[Dict[str, Any]]) -> int:
        now = _utc_now()
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM document_chunks WHERE doc_id = ? AND user_id = ?", (doc_id, user_id))
            for ch in chunks:
                emb = ch["embedding"]
                if self.is_postgres:
                    vec_768 = (list(emb) + [0.0] * 768)[:768]
                    cur.execute(
                        """
                        INSERT INTO document_chunks (
                            id, doc_id, user_id, doc_title, page_number,
                            section_header, chunk_index, content, token_count,
                            embedding, created_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?::vector, ?)
                        """,
                        (
                            ch["id"], doc_id, user_id, ch["doc_title"],
                            int(ch["page_number"]), ch["section_header"], int(ch["chunk_index"]),
                            ch["content"], int(ch["token_count"]), _format_pgvector(vec_768), now,
                        ),
                    )
                else:
                    cur.execute(
                        """
                        INSERT INTO document_chunks (
                            id, doc_id, user_id, doc_title, page_number,
                            section_header, chunk_index, content, token_count,
                            embedding_json, embedding_dim, created_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            ch["id"],
                            doc_id,
                            user_id,
                            ch["doc_title"],
                            int(ch["page_number"]),
                            ch["section_header"],
                            int(ch["chunk_index"]),
                            ch["content"],
                            int(ch["token_count"]),
                            json.dumps(emb),
                            len(emb),
                            now,
                        ),
                    )
            conn.commit()
        return len(chunks)

    def load_user_chunks(self, user_id: str, doc_ids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Mandatory metadata pre-filtering WHERE user_id = ? — cross-tenant leakage is impossible."""
        with self._connect() as conn:
            if doc_ids:
                placeholders = ",".join("?" for _ in doc_ids)
                sql = (
                    f"SELECT * FROM document_chunks "
                    f"WHERE user_id = ? AND doc_id IN ({placeholders}) "
                    f"ORDER BY doc_id, chunk_index ASC"
                )
                rows = conn.execute(sql, [user_id, *doc_ids]).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM document_chunks WHERE user_id = ? ORDER BY created_at DESC",
                    (user_id,),
                ).fetchall()
            results: List[Dict[str, Any]] = []
            for r in rows:
                d = dict(r)
                if self.is_postgres:
                    d["embedding"] = _parse_pgvector(d.get("embedding"))
                else:
                    d["embedding"] = json.loads(d.pop("embedding_json") or "[]")
                results.append(d)
            return results

    def vector_search_user_chunks(
        self,
        user_id: str,
        query_embedding: List[float],
        top_k: int = 20,
        doc_ids: Optional[List[str]] = None,
    ) -> Optional[List[Dict[str, Any]]]:
        """Executes native pgvector HNSW cosine search with strict WHERE user_id pre-filtering when on Postgres."""
        if not self.is_postgres or not query_embedding:
            return None
        vec_lit = _format_pgvector((list(query_embedding) + [0.0] * 768)[:768])
        with self._connect() as conn:
            if doc_ids:
                placeholders = ",".join("?" for _ in doc_ids)
                sql = (
                    f"SELECT id, doc_id, user_id, doc_title, page_number, section_header, "
                    f"chunk_index, content, token_count, 1 - (embedding <=> ?::vector) AS dense_sim "
                    f"FROM document_chunks WHERE user_id = ? AND doc_id IN ({placeholders}) "
                    f"ORDER BY embedding <=> ?::vector LIMIT ?"
                )
                rows = conn.execute(sql, [vec_lit, user_id, *doc_ids, vec_lit, int(top_k)]).fetchall()
            else:
                sql = (
                    "SELECT id, doc_id, user_id, doc_title, page_number, section_header, "
                    "chunk_index, content, token_count, 1 - (embedding <=> ?::vector) AS dense_sim "
                    "FROM document_chunks WHERE user_id = ? "
                    "ORDER BY embedding <=> ?::vector LIMIT ?"
                )
                rows = conn.execute(sql, [vec_lit, user_id, vec_lit, int(top_k)]).fetchall()
            return [dict(r) for r in rows]

    def get_user_chunk(self, chunk_id: str, doc_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id, doc_id, user_id, doc_title, page_number, section_header, chunk_index, content, token_count, created_at "
                "FROM document_chunks WHERE id = ? AND doc_id = ? AND user_id = ?",
                (chunk_id, doc_id, user_id),
            ).fetchone()
            return dict(row) if row else None

    # ------------------------------------------------------------------
    # Multi-Turn Chat Sessions & Messages
    # ------------------------------------------------------------------

    def get_or_create_chat_session(
        self, user_id: str, session_id: Optional[str] = None, title: str = "New Study Session"
    ) -> Dict[str, Any]:
        now = _utc_now()
        with self._connect() as conn:
            if session_id:
                row = conn.execute(
                    "SELECT * FROM chat_sessions WHERE id = ? AND user_id = ?",
                    (session_id, user_id),
                ).fetchone()
                if row:
                    return dict(row)

            sid = f"chat_{uuid.uuid4().hex[:16]}"
            conn.execute(
                """
                INSERT INTO chat_sessions (id, user_id, title, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (sid, user_id, title[:90], now, now),
            )
            conn.commit()
            row = conn.execute("SELECT * FROM chat_sessions WHERE id = ? AND user_id = ?", (sid, user_id)).fetchone()
            return dict(row)

    def list_chat_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM chat_sessions WHERE user_id = ? ORDER BY updated_at DESC LIMIT 40",
                (user_id,),
            ).fetchall()
            return [dict(r) for r in rows]

    def delete_chat_session(self, session_id: str, user_id: str) -> bool:
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM chat_messages WHERE session_id = ? AND user_id = ?", (session_id, user_id))
            cur.execute("DELETE FROM chat_sessions WHERE id = ? AND user_id = ?", (session_id, user_id))
            ok = cur.rowcount > 0
            conn.commit()
            return ok

    def add_chat_message(
        self,
        session_id: str,
        user_id: str,
        role: str,
        content: str,
        cited_chunk_ids: Optional[List[str]] = None,
        citations: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        msg_id = f"msg_{uuid.uuid4().hex[:16]}"
        now = _utc_now()
        with self._connect() as conn:
            if self.is_postgres:
                conn.execute(
                    """
                    INSERT INTO chat_messages (
                        id, session_id, user_id, role, content,
                        cited_chunk_ids, citations, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?::jsonb, ?::jsonb, ?)
                    """,
                    (
                        msg_id, session_id, user_id, role, content,
                        json.dumps(cited_chunk_ids or []), json.dumps(citations or []), now,
                    ),
                )
            else:
                conn.execute(
                    """
                    INSERT INTO chat_messages (
                        id, session_id, user_id, role, content,
                        cited_chunk_ids_json, citations_json, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        msg_id,
                        session_id,
                        user_id,
                        role,
                        content,
                        json.dumps(cited_chunk_ids or []),
                        json.dumps(citations or []),
                        now,
                    ),
                )
            conn.execute(
                "UPDATE chat_sessions SET updated_at = ? WHERE id = ? AND user_id = ?",
                (now, session_id, user_id),
            )
            conn.commit()
        return {
            "id": msg_id,
            "session_id": session_id,
            "user_id": user_id,
            "role": role,
            "content": content,
            "cited_chunk_ids": cited_chunk_ids or [],
            "citations": citations or [],
            "created_at": now,
        }

    def get_chat_messages(self, session_id: str, user_id: str, limit: int = 40) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT * FROM chat_messages
                WHERE session_id = ? AND user_id = ?
                ORDER BY created_at ASC
                LIMIT ?
                """,
                (session_id, user_id, int(limit)),
            ).fetchall()
            out: List[Dict[str, Any]] = []
            for r in rows:
                d = dict(r)
                if self.is_postgres:
                    cids = d.get("cited_chunk_ids")
                    cits = d.get("citations")
                    d["cited_chunk_ids"] = cids if isinstance(cids, list) else json.loads(cids or "[]")
                    d["citations"] = cits if isinstance(cits, list) else json.loads(cits or "[]")
                else:
                    d["cited_chunk_ids"] = json.loads(d.pop("cited_chunk_ids_json") or "[]")
                    d["citations"] = json.loads(d.pop("citations_json") or "[]")
                out.append(d)
            return out
