from rest_framework.permissions import BasePermission


class CanManageEmissions(BasePermission):
    """Permission stub for emissions data management endpoints."""

    message = "User does not have emissions management permissions."

    def has_permission(self, request, view) -> bool:
        return bool(getattr(request, "user", None) and request.user.is_authenticated)
