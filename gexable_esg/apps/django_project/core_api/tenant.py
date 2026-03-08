from __future__ import annotations

from contextvars import ContextVar, Token

from django.db import models

_current_tenant: ContextVar[str | None] = ContextVar("gexable_current_tenant", default=None)


def set_current_tenant(tenant_id: str | None) -> Token:
    return _current_tenant.set(tenant_id)


def get_current_tenant() -> str | None:
    return _current_tenant.get()


def reset_current_tenant(token: Token) -> None:
    _current_tenant.reset(token)


class TenantScopedQuerySet(models.QuerySet):
    def scoped(self) -> models.QuerySet:
        tenant_id = get_current_tenant()
        if tenant_id:
            return self.filter(tenant_id=tenant_id)
        return self


class TenantScopedManager(models.Manager):
    def get_queryset(self) -> TenantScopedQuerySet:
        return TenantScopedQuerySet(self.model, using=self._db).scoped()
