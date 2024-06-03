from rest_framework.permissions import BasePermission


class CanManageProductsPermission(BasePermission):
    """
    Check that the user has the 'can_manage_products' permission.
    """

    def has_permission(self, request, view):
        # Check if the user has the specific permission
        return request.user.has_perm("product.can_manage_products")
