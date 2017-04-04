from rest_framework.permissions import BasePermission


class CanManageUserPermissions(BasePermission):
    permission = 'auth.permissions_manage_access'

    def has_permission(self, request, view):
        if not request.user:
            return False

        return request.user.is_staff or request.user.has_perm(
            self.permission
        )
