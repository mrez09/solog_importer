import hmac
import re
import secrets
from urllib.parse import urlsplit

from fastapi import HTTPException, Request

CSRF_COOKIE_NAME = "solog_csrf"
_CSRF_TOKEN_PATTERN = re.compile(r"^[A-Za-z0-9_-]{43}$")


def issue_csrf_token(request: Request) -> str:
    cookie_token = request.cookies.get(CSRF_COOKIE_NAME, "")
    if _CSRF_TOKEN_PATTERN.fullmatch(cookie_token):
        return cookie_token
    return secrets.token_urlsafe(32)


def require_same_origin_and_csrf(request: Request, submitted_token: str) -> None:
    supplied_origin = request.headers.get("origin")
    if supplied_origin is None:
        supplied_origin = request.headers.get("referer")
    if not supplied_origin or not _matches_request_origin(request, supplied_origin):
        raise HTTPException(status_code=403, detail="Permintaan lintas-origin ditolak.")

    cookie_token = request.cookies.get(CSRF_COOKIE_NAME, "")
    if (
        not _CSRF_TOKEN_PATTERN.fullmatch(cookie_token)
        or not _CSRF_TOKEN_PATTERN.fullmatch(submitted_token)
        or not hmac.compare_digest(cookie_token, submitted_token)
    ):
        raise HTTPException(status_code=403, detail="Token CSRF tidak valid.")


def _matches_request_origin(request: Request, value: str) -> bool:
    try:
        supplied = urlsplit(value)
        expected = request.url
        is_origin = request.headers.get("origin") is not None
        if supplied.username is not None or supplied.password is not None:
            return False
        if supplied.scheme.casefold() != expected.scheme.casefold():
            return False
        if supplied.netloc.casefold() != expected.netloc.casefold():
            return False
        if is_origin and (
            supplied.path not in ("", "/")
            or supplied.query
            or supplied.fragment
        ):
            return False
        return True
    except ValueError:
        return False
