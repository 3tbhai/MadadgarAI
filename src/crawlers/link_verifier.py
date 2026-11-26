"""Async Anti-404, Anti-Homepage & Optional Playwright Headless Fallback Link Verification Guard."""
import asyncio
from datetime import datetime, timezone
import importlib.util
import logging
import ssl
from typing import Dict, List, Optional, Tuple
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
import httpx

logger = logging.getLogger("MadadgaarAI.Crawlers.LinkVerifier")


def _is_tls_cert_error(exc: Exception) -> bool:
    cur: Optional[BaseException] = exc
    while cur is not None:
        if isinstance(cur, ssl.SSLCertVerificationError) or "CERTIFICATE_VERIFY_FAILED" in str(cur):
            return True
        cur = cur.__cause__ or cur.__context__
    return False


async def smart_http_get(
    url: str,
    timeout: float = 12.0,
    headers: Optional[Dict[str, str]] = None,
    follow_redirects: bool = True,
) -> httpx.Response:
    """Verifies TLS strictly first; falls back to verify=False ONLY on certificate chain errors (common on .gov.in portals)."""
    hdrs = headers or DEFAULT_HEADERS
    try:
        async with httpx.AsyncClient(verify=True, headers=hdrs, timeout=timeout, follow_redirects=follow_redirects) as hc:
            return await hc.get(url)
    except Exception as exc:
        if not _is_tls_cert_error(exc):
            raise
        logger.debug(f"TLS chain fallback for {urlparse(url).netloc}: {exc}")
        async with httpx.AsyncClient(verify=False, headers=hdrs, timeout=timeout, follow_redirects=follow_redirects) as hc:
            return await hc.get(url)

PLAYWRIGHT_AVAILABLE = importlib.util.find_spec("playwright") is not None


async def playwright_fetch_page(url: str, timeout_ms: int = 12000) -> Tuple[int, str, str]:
    """
    Optional headless Chromium fallback for JS-rendered or anti-bot portals.
    Returns (status_code, final_url, html_content). Safely returns (0, url, '') if Playwright is not installed.
    """
    if not PLAYWRIGHT_AVAILABLE:
        return (0, url, "")
    try:
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent=DEFAULT_HEADERS["User-Agent"])
            page = await context.new_page()
            resp = await page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
            status = resp.status if resp else 0
            final_url = page.url or url
            html = await page.content()
            await browser.close()
            return (status, final_url, html)
    except Exception as exc:
        logger.debug(f"Playwright fallback skipped for {url}: {exc}")
        return (0, url, "")

TRACKING_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "fbclid", "gclid", "ref", "source", "mc_cid", "mc_eid",
}

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def canonicalize_url(url: str) -> str:
    """Normalizes a URL by stripping tracking query parameters, fragments, and trailing slashes."""
    if not url:
        return ""
    parsed = urlparse(url.strip())
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return ""
    clean_query = urlencode(
        [(k, v) for k, v in parse_qsl(parsed.query, keep_blank_values=False) if k.lower() not in TRACKING_PARAMS]
    )
    clean_path = parsed.path.rstrip("/") or "/"
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), clean_path, "", clean_query, ""))


def is_specific_listing_url(url: str) -> bool:
    """Rejects malformed URLs and generic bare homepages when specific listing URLs are required."""
    if not url:
        return False
    parsed = urlparse(url.strip())
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return False
    path = (parsed.path or "").strip("/")
    # Must have a non-empty path or query identifying a specific listing
    if not path and not parsed.query:
        return False
    # Reject javascript:, mailto:, or obvious dead hash links
    if parsed.scheme in ("javascript", "mailto", "tel"):
        return False
    return True


class AsyncLinkVerifier:
    """Verifies candidate opportunity URLs concurrently and discards 404/5xx/unreachable links."""

    def __init__(self, concurrency: int = 12, timeout_seconds: float = 7.0):
        self.concurrency = concurrency
        self.timeout_seconds = timeout_seconds

    async def verify_single(
        self, url: str, client: httpx.AsyncClient, semaphore: asyncio.Semaphore
    ) -> Tuple[str, bool, int, str, datetime]:
        """Returns (original_url, is_valid, status_code, final_url, verified_at)."""
        now = datetime.now(timezone.utc)
        if not is_specific_listing_url(url):
            return (url, False, 0, url, now)

        async with semaphore:
            try:
                try:
                    resp = await client.head(url, timeout=self.timeout_seconds, follow_redirects=True)
                except Exception as tls_exc:
                    if not _is_tls_cert_error(tls_exc):
                        raise
                    async with httpx.AsyncClient(verify=False, headers=DEFAULT_HEADERS, timeout=self.timeout_seconds) as fb:
                        resp = await fb.head(url, follow_redirects=True)
                status = resp.status_code
                final_url = str(resp.url)

                # Some servers reject HEAD with 403/405/501; fall back to streaming GET
                if status in (403, 405, 501) or status >= 400:
                    try:
                        async with client.stream("GET", url, timeout=self.timeout_seconds, follow_redirects=True) as get_resp:
                            status = get_resp.status_code
                            final_url = str(get_resp.url)
                    except Exception as tls_exc:
                        if not _is_tls_cert_error(tls_exc):
                            raise
                        async with httpx.AsyncClient(verify=False, headers=DEFAULT_HEADERS, timeout=self.timeout_seconds) as fb:
                            async with fb.stream("GET", url, follow_redirects=True) as get_resp:
                                status = get_resp.status_code
                                final_url = str(get_resp.url)

                # Optional Playwright headless fallback when installed and anti-bot 403/503 is encountered
                if status in (403, 503) and PLAYWRIGHT_AVAILABLE:
                    pw_status, pw_url, _ = await playwright_fetch_page(url, timeout_ms=int(self.timeout_seconds * 1000))
                    if 200 <= pw_status <= 399:
                        status = pw_status
                        final_url = pw_url

                is_ok = 200 <= status <= 399
                return (url, is_ok, status, final_url, datetime.now(timezone.utc))
            except Exception as exc:
                logger.debug(f"Link check failed for {url}: {exc}")
                return (url, False, 0, url, datetime.now(timezone.utc))

    async def verify_batch(self, urls: List[str]) -> Dict[str, Tuple[bool, int, str, datetime]]:
        """Concurrently verifies a batch of unique URLs and returns a map of url -> (is_valid, status, final_url, ts)."""
        unique_urls = list(dict.fromkeys(urls))
        if not unique_urls:
            return {}

        semaphore = asyncio.Semaphore(self.concurrency)
        results: Dict[str, Tuple[bool, int, str, datetime]] = {}
        async with httpx.AsyncClient(
            verify=True,
            headers=DEFAULT_HEADERS,
            limits=httpx.Limits(max_connections=self.concurrency + 4, max_keepalive_connections=self.concurrency),
        ) as client:
            tasks = [self.verify_single(u, client, semaphore) for u in unique_urls]
            completed = await asyncio.gather(*tasks, return_exceptions=True)
            for item in completed:
                if isinstance(item, tuple) and len(item) == 5:
                    orig, ok, code, final_u, ts = item
                    results[orig] = (ok, code, final_u, ts)
        return results
