from rest_framework.permissions import BasePermission


class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        allowed_methods = ["GET", "DELETE", "PATCH"]
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
            and request.method in allowed_methods
        )
