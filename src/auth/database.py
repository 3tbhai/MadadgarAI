"""Multi-Tenant ACID Relational + Vector Chunk Store for Saral AI (Strict user_id Isolation)."""
from datetime import datetime, timezone
import json
import logging
from pathlib import Path
import sqlite3
from typing import Any, Dict, List, Optional
import uuid

from src.auth.modes import UserMode
from src.config import DATABASE_PATH

logger = logging.getLogger("MadadgaarAI.Auth.DB")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class SaralMultiTenantDB:
    """
    ACID SQLite store for Users, Refresh Tokens, Tenant-Isolated Documents,
    Vector Chunks (with ON DELETE CASCADE), and Multi-Turn Chat Sessions/Messages.
    Production PostgreSQL + pgvector schema parity is provided in migrations/001_saral_multitenant_pgvector.sql.
    """

    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = Path(db_path)
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        return conn

    def _init_schema(self):
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
                    user_mode TEXT NOT NULL DEFAULT 'student',
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
                    user_mode TEXT NOT NULL DEFAULT 'student',
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
                    user_mode TEXT NOT NULL DEFAULT 'student',
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
                    user_mode TEXT NOT NULL DEFAULT 'student',
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
                INSERT INTO users (id, google_sub, email, full_name, avatar_url, user_mode, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (uid, google_sub, clean_email, full_name.strip() or clean_email, avatar_url or "", UserMode.STUDENT.value, now, now),
            )
            conn.commit()
            cur.execute("SELECT * FROM users WHERE id = ?", (uid,))
            return dict(cur.fetchone())

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            return dict(row) if row else None

    def update_user_mode(self, user_id: str, mode: UserMode) -> Optional[Dict[str, Any]]:
        now = _utc_now()
        with self._connect() as conn:
            conn.execute(
                "UPDATE users SET user_mode = ?, updated_at = ? WHERE id = ?",
                (mode.value, now, user_id),
            )
            conn.commit()
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
                VALUES (?, ?, ?, ?, 0, ?)
                """,
                (jti, user_id, token_hash, expires_at, _utc_now()),
            )
            conn.commit()

    def get_refresh_token(self, jti: str) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM refresh_tokens WHERE jti = ?", (jti,)).fetchone()
            return dict(row) if row else None

    def revoke_refresh_token(self, jti: str, replaced_by: Optional[str] = None) -> None:
        with self._connect() as conn:
            conn.execute(
                "UPDATE refresh_tokens SET revoked = 1, replaced_by = ? WHERE jti = ?",
                (replaced_by, jti),
            )
            conn.commit()

    def revoke_all_user_refresh_tokens(self, user_id: str) -> None:
        with self._connect() as conn:
            conn.execute("UPDATE refresh_tokens SET revoked = 1 WHERE user_id = ?", (user_id,))
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
        user_mode: str,
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
                    id, user_id, user_mode, title, source_type, source_uri,
                    mime_type, file_size_bytes, content_sha256, status, error_message,
                    chunk_count, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending', '', 0, ?, ?)
                """,
                (
                    doc_id, user_id, user_mode, title, source_type, source_uri,
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
                cur.execute(
                    """
                    INSERT INTO document_chunks (
                        id, doc_id, user_id, user_mode, doc_title, page_number,
                        section_header, chunk_index, content, token_count,
                        embedding_json, embedding_dim, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        ch["id"],
                        doc_id,
                        user_id,
                        ch["user_mode"],
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
                d["embedding"] = json.loads(d.pop("embedding_json") or "[]")
                results.append(d)
            return results

    def get_user_chunk(self, chunk_id: str, doc_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id, doc_id, user_id, user_mode, doc_title, page_number, section_header, chunk_index, content, token_count, created_at "
                "FROM document_chunks WHERE id = ? AND doc_id = ? AND user_id = ?",
                (chunk_id, doc_id, user_id),
            ).fetchone()
            return dict(row) if row else None

    # ------------------------------------------------------------------
    # Multi-Turn Chat Sessions & Messages
    # ------------------------------------------------------------------

    def get_or_create_chat_session(
        self, user_id: str, user_mode: str, session_id: Optional[str] = None, title: str = "New Study Session"
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
                INSERT INTO chat_sessions (id, user_id, user_mode, title, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (sid, user_id, user_mode, title[:90], now, now),
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
                d["cited_chunk_ids"] = json.loads(d.pop("cited_chunk_ids_json") or "[]")
                d["citations"] = json.loads(d.pop("citations_json") or "[]")
                out.append(d)
            return out
