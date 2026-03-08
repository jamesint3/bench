from rest_framework.permissions import BasePermission


class RolePermission(BasePermission):
    message = "User role does not have permission for this action."

    def has_permission(self, request, view) -> bool:
        allowed_roles = getattr(view, "required_roles", None)
        if not allowed_roles:
            return True

        role = getattr(request, "gexable_role", None) or request.headers.get("X-User-Role", "preparer")
        return role in allowed_roles
