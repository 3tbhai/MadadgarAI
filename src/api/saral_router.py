"""FastAPI Routers for Google OAuth 2.0 + JWT Auth and Multi-Tenant Gemini RAG."""
import json
import logging
import secrets
from typing import Any, Dict, List, Optional

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    Request,
    Response,
    UploadFile,
    status,
)
from fastapi.responses import RedirectResponse, StreamingResponse
from pydantic import BaseModel, Field

from src.auth.database import SaralMultiTenantDB
from src.auth.security import (
    REFRESH_COOKIE_NAME,
    SlidingWindowRateLimiter,
    build_get_current_user,
    build_google_oauth_authorize_url,
    clear_auth_cookies,
    create_token_pair,
    exchange_google_auth_code,
    get_google_client_id,
    get_google_client_secret,
    is_cookie_secure,
    is_dev_auth_allowed,
    rotate_refresh_session,
    set_auth_cookies,
    verify_google_id_token_server_side,
)
from src.rag.gemini_client import GeminiRAGClient
from src.rag.service import MultiTenantRAGService

logger = logging.getLogger("MadadgaarAI.API.SaralV2")

# Shared singletons for multi-tenant auth & RAG
saral_db = SaralMultiTenantDB()
saral_gemini = GeminiRAGClient()
saral_rag_service = MultiTenantRAGService(db=saral_db, gemini_client=saral_gemini)
get_current_user = build_get_current_user(saral_db)

# Per-user sliding window rate limiters for /ingest and /chat
ingest_rate_limiter = SlidingWindowRateLimiter(max_requests=25, window_seconds=60)
chat_rate_limiter = SlidingWindowRateLimiter(max_requests=40, window_seconds=60)

router = APIRouter(tags=["Saral AI Multi-Tenant Auth & Gemini RAG"])


# ------------------------------------------------------------------
# Request / Response Schemas
# ------------------------------------------------------------------

class GoogleTokenLoginRequest(BaseModel):
    credential: str = Field(..., min_length=10, description="Google Identity Services JWT ID Token")


class DevLoginRequest(BaseModel):
    email: str = Field(default="student@madadgaarai.local")
    full_name: str = Field(default="Demo Student")


class URLIngestRequest(BaseModel):
    url: str = Field(..., min_length=8)
    title: Optional[str] = None


class SaralMultiTenantChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=4000)
    session_id: Optional[str] = None
    doc_ids: Optional[List[str]] = None


def _format_user_response(user: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": user["id"],
        "email": user["email"],
        "full_name": user["full_name"],
        "avatar_url": user.get("avatar_url") or "",
    }


# ------------------------------------------------------------------
# 1. Google OAuth 2.0 + JWT Cookie Authentication
# ------------------------------------------------------------------

@router.get("/api/auth/config")
async def get_auth_config():
    """Public auth metadata for frontend Google Sign-In button."""
    cid = get_google_client_id()
    csec = get_google_client_secret()
    return {
        "google_oauth_enabled": bool(cid),
        "google_oauth_code_flow_enabled": bool(cid and csec),
        "google_client_id": cid,
        "dev_auth_allowed": is_dev_auth_allowed(),
        "gemini_rag_backend": saral_gemini.backend_label,
        "gemini_live_enabled": saral_gemini.is_live_gemini_enabled,
    }


@router.get("/api/auth/google/login")
async def start_google_oauth_login(request: Request):
    """Starts Google OAuth 2.0 Authorization Code flow with CSRF state cookie."""
    state = secrets.token_urlsafe(24)
    auth_url = build_google_oauth_authorize_url(request, state=state)
    resp = RedirectResponse(url=auth_url, status_code=status.HTTP_302_FOUND)
    resp.set_cookie(
        key="saral_oauth_state",
        value=state,
        httponly=True,
        secure=is_cookie_secure(),
        samesite="lax",
        max_age=600,
        path="/",
    )
    return resp


@router.get("/api/auth/google/callback")
async def handle_google_oauth_callback(request: Request, code: str, state: str = ""):
    """Handles Google OAuth 2.0 callback, verifies ID token, upserts user, and sets HTTP-only JWT cookies."""
    expected_state = request.cookies.get("saral_oauth_state")
    if not expected_state or expected_state != state:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OAuth state parameter.")

    profile = await exchange_google_auth_code(request, code=code)
    user = saral_db.upsert_google_user(
        google_sub=profile["sub"],
        email=profile["email"],
        full_name=profile["name"],
        avatar_url=profile["picture"],
    )
    access_tok, refresh_tok, _ = create_token_pair(saral_db, user)
    resp = RedirectResponse(url="/?auth=success#assistant", status_code=status.HTTP_302_FOUND)
    resp.delete_cookie("saral_oauth_state", path="/")
    set_auth_cookies(resp, access_tok, refresh_tok)
    return resp


@router.post("/api/auth/google/token")
async def login_with_google_id_token(req: GoogleTokenLoginRequest, response: Response):
    """Verifies a Google Identity Services ID token server-side and sets HTTP-only JWT session cookies."""
    profile = verify_google_id_token_server_side(req.credential)
    user = saral_db.upsert_google_user(
        google_sub=profile["sub"],
        email=profile["email"],
        full_name=profile["name"],
        avatar_url=profile["picture"],
    )
    access_tok, refresh_tok, _ = create_token_pair(saral_db, user)
    set_auth_cookies(response, access_tok, refresh_tok)
    return {"authenticated": True, "user": _format_user_response(user)}


@router.post("/api/auth/dev-login")
async def local_dev_login(req: DevLoginRequest, response: Response):
    """Local development & automated test login (disabled when ALLOW_LOCAL_DEV_AUTH=false)."""
    if not is_dev_auth_allowed():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Local dev authentication is disabled in production. Use Google Sign-In.",
        )
    clean_email = req.email.strip().lower()
    if "@" not in clean_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Valid email address required.")
    user = saral_db.upsert_google_user(
        google_sub=f"dev_sub_{clean_email}",
        email=clean_email,
        full_name=req.full_name.strip() or clean_email.split("@")[0],
        avatar_url="",
    )
    access_tok, refresh_tok, _ = create_token_pair(saral_db, user)
    set_auth_cookies(response, access_tok, refresh_tok)
    return {"authenticated": True, "user": _format_user_response(user)}


@router.post("/api/auth/refresh")
async def refresh_jwt_session(request: Request, response: Response):
    """Rotates the HTTP-only refresh token cookie and issues fresh access + refresh tokens."""
    raw_refresh = request.cookies.get(REFRESH_COOKIE_NAME)
    if not raw_refresh:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token cookie missing.")
    user = rotate_refresh_session(saral_db, raw_refresh, response)
    return {"authenticated": True, "user": _format_user_response(user)}


@router.post("/api/auth/logout")
async def logout_session(request: Request, response: Response):
    """Revokes active refresh token and clears HTTP-only auth cookies."""
    raw_refresh = request.cookies.get(REFRESH_COOKIE_NAME)
    if raw_refresh:
        try:
            import jwt
            from src.auth.security import JWT_ALGORITHM, get_jwt_secret
            payload = jwt.decode(raw_refresh, get_jwt_secret(), algorithms=[JWT_ALGORITHM])
            if payload.get("jti"):
                saral_db.revoke_refresh_token(payload["jti"])
        except Exception:
            pass
    clear_auth_cookies(response)
    return {"authenticated": False, "status": "logged_out"}


@router.get("/api/auth/me")
async def get_authenticated_profile(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Returns the authenticated user profile."""
    return {"authenticated": True, "user": _format_user_response(current_user)}


# ------------------------------------------------------------------
# 2. Tenant-Isolated Document Ingestion & Library Management
# ------------------------------------------------------------------

@router.post("/api/saral/documents/upload", status_code=status.HTTP_202_ACCEPTED)
async def upload_private_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """Uploads PDF, Markdown, or TXT into the user's isolated knowledge base and indexes asynchronously."""
    ingest_rate_limiter.check(f"ingest:{current_user['id']}")
    file_bytes = await file.read()
    try:
        doc, is_duplicate = saral_rag_service.prepare_file_document(
            user=current_user,
            filename=file.filename or "document.txt",
            mime_type=file.content_type or "text/plain",
            file_bytes=file_bytes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    if not is_duplicate:
        background_tasks.add_task(
            saral_rag_service.process_file_job,
            doc["id"],
            current_user["id"],
            doc["title"],
            doc["source_type"],
            file_bytes,
        )
    return {"document": doc, "deduplicated": is_duplicate}


@router.post("/api/saral/documents/ingest-url")
async def ingest_private_url(
    req: URLIngestRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """Ingests a web URL or arXiv paper link into the authenticated user's isolated knowledge base."""
    ingest_rate_limiter.check(f"ingest:{current_user['id']}")
    try:
        doc, is_duplicate = await saral_rag_service.prepare_and_process_url(
            user=current_user,
            url=req.url,
            custom_title=req.title,
        )
        return {"document": doc, "deduplicated": is_duplicate}
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"URL ingestion failed: {str(exc)[:140]}")


@router.get("/api/saral/documents")
async def list_private_documents(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Lists all documents owned strictly by the authenticated user."""
    docs = saral_db.list_user_documents(current_user["id"])
    return {"user_id": current_user["id"], "total": len(docs), "documents": docs}


@router.get("/api/saral/documents/{doc_id}")
async def get_private_document_status(
    doc_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    doc = saral_db.get_user_document(doc_id, current_user["id"])
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")
    return {"document": doc}


@router.get("/api/saral/documents/{doc_id}/chunks/{chunk_id}")
async def inspect_source_chunk(
    doc_id: str,
    chunk_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """Returns exact source chunk metadata and text for the clickable Citation Drawer."""
    chunk = saral_db.get_user_chunk(chunk_id=chunk_id, doc_id=doc_id, user_id=current_user["id"])
    if not chunk:
        raise HTTPException(status_code=404, detail="Citation chunk not found.")
    return {"chunk": chunk}


@router.delete("/api/saral/documents/{doc_id}")
async def delete_private_document(
    doc_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """Deletes a document and cascades deletion to all its vector chunks (strictly scoped to user_id)."""
    deleted = saral_db.delete_user_document(doc_id=doc_id, user_id=current_user["id"])
    if not deleted:
        raise HTTPException(status_code=404, detail="Document not found.")
    return {"status": "deleted", "doc_id": doc_id}


# ------------------------------------------------------------------
# 3. Tenant-Isolated Grounded Chat & SSE Streaming + Session History
# ------------------------------------------------------------------

@router.get("/api/saral/sessions")
async def list_user_chat_sessions(current_user: Dict[str, Any] = Depends(get_current_user)):
    sessions = saral_db.list_chat_sessions(current_user["id"])
    return {"sessions": sessions}


@router.get("/api/saral/sessions/{session_id}/messages")
async def get_user_chat_messages(
    session_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    messages = saral_db.get_chat_messages(session_id=session_id, user_id=current_user["id"])
    return {"session_id": session_id, "messages": messages}


@router.delete("/api/saral/sessions/{session_id}")
async def delete_user_chat_session(
    session_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    ok = saral_db.delete_chat_session(session_id=session_id, user_id=current_user["id"])
    if not ok:
        raise HTTPException(status_code=404, detail="Chat session not found.")
    return {"status": "deleted", "session_id": session_id}


@router.post("/api/saral/chat")
async def saral_private_rag_chat(
    req: SaralMultiTenantChatRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """Executes tenant-isolated Hybrid Vector + BM25 RRF retrieval and grounded generation."""
    chat_rate_limiter.check(f"chat:{current_user['id']}")
    return await saral_rag_service.chat(
        user=current_user,
        query=req.query.strip(),
        session_id=req.session_id,
        doc_ids=req.doc_ids,
    )


@router.post("/api/saral/chat/stream")
async def saral_private_rag_chat_stream(
    req: SaralMultiTenantChatRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """Streams grounded mode-specific Gemini RAG responses via Server-Sent Events (SSE)."""
    chat_rate_limiter.check(f"chat:{current_user['id']}")

    async def _sse_generator():
        async for evt in saral_rag_service.chat_stream_events(
            user=current_user,
            query=req.query.strip(),
            session_id=req.session_id,
            doc_ids=req.doc_ids,
        ):
            yield f"data: {json.dumps(evt)}\n\n"

    return StreamingResponse(
        _sse_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
