from __future__ import annotations

from django.core.cache import cache
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from rest_framework import authentication, exceptions, permissions

from .models import User


TOKEN_MAX_AGE_SECONDS = 60 * 60 * 12
TOKEN_PREFIX = "Bearer "
TOKEN_REVOKED_PREFIX = "revoked_token:"


def issue_user_token(user: User) -> str:
    payload = f"{user.id}:{user.email}"
    return TimestampSigner(salt="gexable-auth").sign(payload)


def revoke_token(token: str) -> None:
    cache.set(f"{TOKEN_REVOKED_PREFIX}{token}", True, timeout=TOKEN_MAX_AGE_SECONDS)


class BearerTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith(TOKEN_PREFIX):
            return None

        token = auth_header[len(TOKEN_PREFIX) :]
        if cache.get(f"{TOKEN_REVOKED_PREFIX}{token}"):
            raise exceptions.AuthenticationFailed("Token revoked")

        try:
            raw = TimestampSigner(salt="gexable-auth").unsign(token, max_age=TOKEN_MAX_AGE_SECONDS)
            user_id_str, email = raw.split(":", 1)
            user = User.objects.filter(id=int(user_id_str), email=email, is_active=True).first()
            if not user:
                raise exceptions.AuthenticationFailed("Invalid token user")
            return user, token
        except (BadSignature, SignatureExpired, ValueError) as exc:
            raise exceptions.AuthenticationFailed("Invalid or expired token") from exc


class AuthenticatedUserPermission(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        user = getattr(request, "user", None)
        return user is not None and getattr(user, "id", None) is not None
