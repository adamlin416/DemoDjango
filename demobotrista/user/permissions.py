from rest_framework.permissions import BasePermission


class CanListUsersPermission(BasePermission):
    """
    Check that the user has the 'can_list_users' permission.
    """

    def has_permission(self, request, view):
        # Check if the user has the specific permission
        return request.user.has_perm("user.can_list_users")
