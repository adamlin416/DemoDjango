from rest_framework.permissions import BasePermission


class CanOrderPermission(BasePermission):
    """
    Check that the user has the 'can_order' permission.
    """

    def has_permission(self, request, view):
        # Check if the user has the specific permission
        return request.user.has_perm("order.can_order")
