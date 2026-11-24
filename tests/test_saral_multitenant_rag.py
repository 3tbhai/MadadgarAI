"""Integration Tests for Multi-Tenant Saral AI: Google/JWT Auth, RBAC Modes, Cross-User Isolation & Streaming RAG."""
import json
import pytest
from fastapi.testclient import TestClient

from src.api.main import app
from src.auth.security import ACCESS_COOKIE_NAME, REFRESH_COOKIE_NAME


def test_1_unauthenticated_requests_strictly_rejected():
    """Verify every protected Saral AI & Auth endpoint rejects unauthenticated requests with HTTP 401."""
    with TestClient(app) as client:
        assert client.get("/api/auth/me").status_code == 401
        assert client.patch("/api/auth/mode", json={"user_mode": "researcher"}).status_code == 401
        assert client.get("/api/saral/documents").status_code == 401
        assert client.post(
            "/api/saral/documents/upload",
            files={"file": ("notes.txt", b"Hello world study notes", "text/plain")},
        ).status_code == 401
        assert client.post("/api/saral/chat", json={"query": "Explain gravity"}).status_code == 401
        assert client.post("/api/saral/chat/stream", json={"query": "Explain gravity"}).status_code == 401
        assert client.get("/api/saral/sessions").status_code == 401


def test_2_jwt_cookies_user_modes_and_refresh_token_rotation():
    """Verify HTTP-only JWT cookie login, default Student mode, mode switching, and refresh token reuse detection."""
    with TestClient(app) as client:
        r_login = client.post(
            "/api/auth/dev-login",
            json={"email": "mode_tester@saral.test", "full_name": "Mode Tester"},
        )
        assert r_login.status_code == 200
        user = r_login.json()["user"]
        assert user["user_mode"] == "student"
        assert ACCESS_COOKIE_NAME in client.cookies
        assert REFRESH_COOKIE_NAME in client.cookies
        old_refresh = client.cookies.get(REFRESH_COOKIE_NAME)

        # Switch Student -> Researcher -> Educator via Strategy Registry
        r_res = client.patch("/api/auth/mode", json={"user_mode": "researcher"})
        assert r_res.status_code == 200
        assert r_res.json()["user"]["user_mode"] == "researcher"
        assert r_res.json()["user"]["mode_config"]["retrieval_top_k"] == 7

        r_edu = client.patch("/api/auth/mode", json={"user_mode": "educator"})
        assert r_edu.status_code == 200
        assert r_edu.json()["user"]["user_mode"] == "educator"
        assert r_edu.json()["user"]["mode_config"]["display_name"] == "Educator Mode"

        # Refresh token rotation succeeds and issues a new refresh token
        latest_refresh = client.cookies.get(REFRESH_COOKIE_NAME)
        r_ref = client.post("/api/auth/refresh")
        assert r_ref.status_code == 200
        rotated_refresh = client.cookies.get(REFRESH_COOKIE_NAME)
        assert rotated_refresh and rotated_refresh != latest_refresh

        # Replaying either the superseded login refresh token OR the rotated refresh token is strictly rejected with 401
        for revoked_tok in (old_refresh, latest_refresh):
            with TestClient(app) as replay_client:
                replay_client.cookies.set(REFRESH_COOKIE_NAME, revoked_tok)
                r_replay = replay_client.post("/api/auth/refresh")
                assert r_replay.status_code == 401


def test_3_strict_cross_user_vector_and_document_isolation():
    """Verify User A's private documents & vector chunks can NEVER leak to User B."""
    with TestClient(app) as client_a, TestClient(app) as client_b:
        assert client_a.post(
            "/api/auth/dev-login",
            json={"email": "tenant_a@saral.test", "full_name": "Tenant Alpha"},
        ).status_code == 200
        assert client_b.post(
            "/api/auth/dev-login",
            json={"email": "tenant_b@saral.test", "full_name": "Tenant Beta"},
        ).status_code == 200

        # User A uploads private quantum notes
        secret_md = (
            "# Quantum Entanglement Lecture\n\n"
            "Project code QUANTUM_SECRET_ALPHA_991 defines Bell state $|\\Phi^+\\rangle = \\frac{1}{\\sqrt{2}}(|00\\rangle + |11\\rangle)$.\n"
            "Entangled qubits share non-classical correlations across arbitrary distances."
        ).encode("utf-8")
        r_up_a = client_a.post(
            "/api/saral/documents/upload",
            files={"file": ("quantum_notes.md", secret_md, "text/markdown")},
        )
        assert r_up_a.status_code == 202
        doc_a_id = r_up_a.json()["document"]["id"]

        # Re-uploading identical content for User A triggers SHA-256 deduplication
        r_dup_a = client_a.post(
            "/api/saral/documents/upload",
            files={"file": ("quantum_notes_copy.md", secret_md, "text/markdown")},
        )
        assert r_dup_a.status_code == 202
        assert r_dup_a.json()["deduplicated"] is True

        # User B uploads unrelated botany notes
        botany_md = (
            "# Plant Photosynthesis Basics\n\n"
            "Chlorophyll marker BOTANY_CHLOROPHYLL_334 absorbs blue and red wavelengths to synthesize glucose."
        ).encode("utf-8")
        r_up_b = client_b.post(
            "/api/saral/documents/upload",
            files={"file": ("botany.md", botany_md, "text/markdown")},
        )
        assert r_up_b.status_code == 202
        doc_b_id = r_up_b.json()["document"]["id"]

        # User B cannot see, fetch, or delete User A's document
        docs_b = client_b.get("/api/saral/documents").json()["documents"]
        assert all(d["id"] != doc_a_id for d in docs_b)
        assert client_b.get(f"/api/saral/documents/{doc_a_id}").status_code == 404
        assert client_b.delete(f"/api/saral/documents/{doc_a_id}").status_code == 404

        # User B querying User A's secret gets ZERO citations from User A and no leaked secret
        r_chat_b = client_b.post("/api/saral/chat", json={"query": "What is QUANTUM_SECRET_ALPHA_991?"})
        assert r_chat_b.status_code == 200
        chat_b = r_chat_b.json()
        assert "QUANTUM_SECRET_ALPHA_991" not in chat_b["answer"]
        assert all(c["doc_id"] != doc_a_id for c in chat_b["citations"])

        # Cleanup
        assert client_a.delete(f"/api/saral/documents/{doc_a_id}").status_code == 200
        assert client_b.delete(f"/api/saral/documents/{doc_b_id}").status_code == 200


def test_4_end_to_end_ingestion_cited_rag_sse_stream_and_cascading_delete():
    """Verify document indexing, cited RAG chat, SSE streaming, chunk inspection, MIME validation, and cascading deletion."""
    with TestClient(app) as client:
        assert client.post(
            "/api/auth/dev-login",
            json={"email": "e2e_student@saral.test", "full_name": "E2E Student"},
        ).status_code == 200

        # Invalid extension rejected with 400
        r_bad = client.post(
            "/api/saral/documents/upload",
            files={"file": ("malware.exe", b"MZ\x90\x00", "application/octet-stream")},
        )
        assert r_bad.status_code == 400

        # Upload valid study guide
        study_md = (
            "# Special Relativity & Energy\n\n"
            "Einstein's mass-energy equivalence formula is $E = mc^2$, where $c$ is the speed of light in vacuum.\n\n"
            "## Lorentz Factor\n\n"
            "Time dilation uses the Lorentz factor $\\gamma = 1 / \\sqrt{1 - v^2/c^2}$ for relativistic speeds."
        ).encode("utf-8")
        r_up = client.post(
            "/api/saral/documents/upload",
            files={"file": ("relativity_guide.md", study_md, "text/markdown")},
        )
        assert r_up.status_code == 202
        doc_id = r_up.json()["document"]["id"]

        # Verify background task completed indexing
        r_doc = client.get(f"/api/saral/documents/{doc_id}")
        assert r_doc.status_code == 200
        doc = r_doc.json()["document"]
        assert doc["status"] == "indexed"
        assert doc["chunk_count"] >= 1

        # Grounded chat returns inline citations and persisted session/messages
        r_chat = client.post(
            "/api/saral/chat",
            json={"query": "Explain Einstein's mass-energy equivalence and Lorentz factor"},
        )
        assert r_chat.status_code == 200
        chat_data = r_chat.json()
        assert chat_data["grounded"] is True
        assert len(chat_data["citations"]) >= 1
        assert "[Source:" in chat_data["answer"]
        sid = chat_data["session_id"]

        # Inspect cited chunk via Citation Drawer endpoint
        first_cite = chat_data["citations"][0]
        r_chk = client.get(f"/api/saral/documents/{first_cite['doc_id']}/chunks/{first_cite['chunk_id']}")
        assert r_chk.status_code == 200
        assert "Lorentz" in r_chk.json()["chunk"]["content"] or "mass-energy" in r_chk.json()["chunk"]["content"]

        # Verify session history persistence
        r_msgs = client.get(f"/api/saral/sessions/{sid}/messages")
        assert r_msgs.status_code == 200
        assert len(r_msgs.json()["messages"]) == 2

        # Verify SSE streaming endpoint emits meta, delta, and done events
        with client.stream(
            "POST",
            "/api/saral/chat/stream",
            json={"query": "What is the Lorentz factor?", "session_id": sid},
        ) as stream_resp:
            assert stream_resp.status_code == 200
            raw_stream = "".join(stream_resp.iter_text())
        events = [
            json.loads(line[5:].strip())
            for line in raw_stream.splitlines()
            if line.startswith("data:")
        ]
        event_types = {e["type"] for e in events}
        assert {"meta", "delta", "done"}.issubset(event_types)

        # Delete document and confirm cascading deletion of vector chunks
        assert client.delete(f"/api/saral/documents/{doc_id}").status_code == 200
        assert client.get(f"/api/saral/documents/{first_cite['doc_id']}/chunks/{first_cite['chunk_id']}").status_code == 404
        assert client.delete(f"/api/saral/sessions/{sid}").status_code == 200
