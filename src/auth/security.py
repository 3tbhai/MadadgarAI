"""Google OAuth 2.0 Verification, HTTP-only JWT Session Cookies with Refresh Rotation, and Rate Limiting."""
from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone
import hashlib
import logging
import os
import secrets
import time
from typing import Any, Deque, Dict, Optional, Tuple
from urllib.parse import urlencode

from fastapi import Depends, HTTPException, Request, Response, status
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
import httpx
import jwt

from src.auth.database import SaralMultiTenantDB

logger = logging.getLogger("MadadgaarAI.Auth.Security")

ACCESS_COOKIE_NAME = "saral_access_token"
REFRESH_COOKIE_NAME = "saral_refresh_token"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_TTL_MINUTES = int(os.getenv("JWT_ACCESS_TTL_MINUTES", "30"))
REFRESH_TOKEN_TTL_DAYS = int(os.getenv("JWT_REFRESH_TTL_DAYS", "14"))

# Stable fallback secret generated per process when JWT_SECRET_KEY is not configured in env
_EPHEMERAL_DEV_SECRET = secrets.token_hex(32)


def get_jwt_secret() -> str:
    return (os.getenv("JWT_SECRET_KEY") or "").strip() or _EPHEMERAL_DEV_SECRET


def get_google_client_id() -> str:
    return (os.getenv("GOOGLE_CLIENT_ID") or "").strip()


def get_google_client_secret() -> str:
    return (os.getenv("GOOGLE_CLIENT_SECRET") or "").strip()


def get_google_redirect_uri(request: Request) -> str:
    configured = (os.getenv("GOOGLE_REDIRECT_URI") or "").strip()
    if configured:
        return configured
    return str(request.base_url).rstrip("/") + "/api/auth/google/callback"


def is_cookie_secure() -> bool:
    return (os.getenv("COOKIE_SECURE", "false").strip().lower() in ("1", "true", "yes"))


def is_dev_auth_allowed() -> bool:
    explicit = os.getenv("ALLOW_LOCAL_DEV_AUTH")
    if explicit is not None and explicit.strip() != "":
        return explicit.strip().lower() in ("1", "true", "yes")
    env_mode = (os.getenv("MADADGAAR_ENV") or "").strip().lower()
    if env_mode in ("prod", "production"):
        return False
    return True


def _hash_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def verify_google_id_token_server_side(credential: str) -> Dict[str, Any]:
    """Verifies a Google OIDC ID token server-side using google-auth against GOOGLE_CLIENT_ID."""
    client_id = get_google_client_id()
    if not client_id:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="GOOGLE_CLIENT_ID is not configured on the server.",
        )
    try:
        idinfo = google_id_token.verify_oauth2_token(
            credential,
            google_requests.Request(),
            client_id,
        )
        if idinfo.get("iss") not in ("accounts.google.com", "https://accounts.google.com"):
            raise ValueError("Invalid Google token issuer.")
        if not idinfo.get("email_verified", False):
            raise ValueError("Google account email is not verified.")
        return {
            "sub": str(idinfo["sub"]),
            "email": str(idinfo["email"]),
            "name": str(idinfo.get("name") or idinfo["email"].split("@")[0]),
            "picture": str(idinfo.get("picture") or ""),
        }
    except Exception as exc:
        logger.warning(f"Google ID token verification failed: {exc}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Google ID token: {str(exc)[:120]}",
        )


def build_google_oauth_authorize_url(request: Request, state: str) -> str:
    client_id = get_google_client_id()
    if not client_id or not get_google_client_secret():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google OAuth 2.0 credentials (GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET) are not configured.",
        )
    params = {
        "client_id": client_id,
        "redirect_uri": get_google_redirect_uri(request),
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account",
        "state": state,
    }
    return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"


async def exchange_google_auth_code(request: Request, code: str) -> Dict[str, Any]:
    """Exchanges Google OAuth 2.0 authorization code for ID token and verifies it server-side."""
    token_resp = None
    async with httpx.AsyncClient(timeout=12.0) as hc:
        token_resp = await hc.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": get_google_client_id(),
                "client_secret": get_google_client_secret(),
                "redirect_uri": get_google_redirect_uri(request),
                "grant_type": "authorization_code",
            },
        )
    if token_resp.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to exchange Google OAuth authorization code.",
        )
    payload = token_resp.json()
    id_tok = payload.get("id_token")
    if not id_tok:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing id_token from Google OAuth.")
    return verify_google_id_token_server_side(id_tok)


def create_token_pair(db: SaralMultiTenantDB, user: Dict[str, Any]) -> Tuple[str, str, str]:
    """Creates signed JWT access + refresh tokens and persists refresh token hash for rotation."""
    now = datetime.now(timezone.utc)
    access_exp = now + timedelta(minutes=ACCESS_TOKEN_TTL_MINUTES)
    refresh_exp = now + timedelta(days=REFRESH_TOKEN_TTL_DAYS)
    refresh_jti = f"rt_{secrets.token_hex(16)}"

    access_payload = {
        "sub": user["id"],
        "email": user["email"],
        "mode": user["user_mode"],
        "type": "access",
        "iat": int(now.timestamp()),
        "exp": int(access_exp.timestamp()),
    }
    refresh_payload = {
        "sub": user["id"],
        "jti": refresh_jti,
        "type": "refresh",
        "iat": int(now.timestamp()),
        "exp": int(refresh_exp.timestamp()),
    }
    secret = get_jwt_secret()
    access_token = jwt.encode(access_payload, secret, algorithm=JWT_ALGORITHM)
    refresh_token = jwt.encode(refresh_payload, secret, algorithm=JWT_ALGORITHM)
    db.store_refresh_token(
        jti=refresh_jti,
        user_id=user["id"],
        token_hash=_hash_token(refresh_token),
        expires_at=refresh_exp.isoformat(),
    )
    return access_token, refresh_token, refresh_jti


def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    secure = is_cookie_secure()
    response.set_cookie(
        key=ACCESS_COOKIE_NAME,
        value=access_token,
        httponly=True,
        secure=secure,
        samesite="lax",
        max_age=ACCESS_TOKEN_TTL_MINUTES * 60,
        path="/",
    )
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=secure,
        samesite="lax",
        max_age=REFRESH_TOKEN_TTL_DAYS * 86400,
        path="/",
    )


def clear_auth_cookies(response: Response) -> None:
    response.delete_cookie(key=ACCESS_COOKIE_NAME, path="/")
    response.delete_cookie(key=REFRESH_COOKIE_NAME, path="/")


def rotate_refresh_session(
    db: SaralMultiTenantDB, raw_refresh_token: str, response: Response
) -> Dict[str, Any]:
    """Validates a refresh JWT, detects token reuse, revokes the old JTI, and issues a rotated pair."""
    try:
        payload = jwt.decode(raw_refresh_token, get_jwt_secret(), algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        clear_auth_cookies(response)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token.")

    if payload.get("type") != "refresh" or not payload.get("jti"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token type.")

    jti = payload["jti"]
    user_id = payload["sub"]
    stored = db.get_refresh_token(jti)
    if not stored:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh session not found.")

    # Reuse detection: if an already-revoked token is replayed, revoke ALL tokens for that user!
    if stored["revoked"] or stored["token_hash"] != _hash_token(raw_refresh_token):
        db.revoke_all_user_refresh_tokens(user_id)
        clear_auth_cookies(response)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token reuse detected. All sessions revoked for security.",
        )

    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User no longer exists.")

    new_access, new_refresh, new_jti = create_token_pair(db, user)
    db.revoke_refresh_token(jti=jti, replaced_by=new_jti)
    set_auth_cookies(response, new_access, new_refresh)
    return user


def decode_access_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, get_jwt_secret(), algorithms=[JWT_ALGORITHM])
        if payload.get("type") != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token type.")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired. Please refresh or sign in.")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token.")


def build_get_current_user(db: SaralMultiTenantDB):
    """FastAPI dependency factory enforcing strict JWT authentication via HTTP-only cookie or Bearer token."""

    def get_current_user(request: Request) -> Dict[str, Any]:
        token = request.cookies.get(ACCESS_COOKIE_NAME)
        if not token:
            auth_hdr = request.headers.get("Authorization") or ""
            if auth_hdr.lower().startswith("bearer "):
                token = auth_hdr[7:].strip()
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required. Sign in with Google to access your private Saral AI workspace.",
            )
        payload = decode_access_token(token)
        user = db.get_user_by_id(payload["sub"])
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authenticated user not found.")
        return user

    return get_current_user


def get_optional_current_user(request: Request, db: SaralMultiTenantDB) -> Optional[Dict[str, Any]]:
    """Returns authenticated user dict if a valid JWT cookie/Bearer token is present, else None."""
    token = request.cookies.get(ACCESS_COOKIE_NAME)
    if not token:
        auth_hdr = request.headers.get("Authorization") or ""
        if auth_hdr.lower().startswith("bearer "):
            token = auth_hdr[7:].strip()
    if not token:
        return None
    try:
        payload = decode_access_token(token)
        return db.get_user_by_id(payload["sub"])
    except HTTPException:
        return None


class SlidingWindowRateLimiter:
    """In-memory per-user/IP sliding window rate limiter for /ingest and /chat protection."""

    def __init__(self, max_requests: int = 30, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._hits: Dict[str, Deque[float]] = defaultdict(deque)

    def check(self, key: str) -> None:
        now = time.monotonic()
        bucket = self._hits[key]
        cutoff = now - self.window_seconds
        while bucket and bucket[0] < cutoff:
            bucket.popleft()
        if len(bucket) >= self.max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded ({self.max_requests} requests per {self.window_seconds}s). Please slow down.",
            )
        bucket.append(now)
