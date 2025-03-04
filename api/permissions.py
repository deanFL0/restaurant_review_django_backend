from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission: 
    - Owners can update/delete their own reviews.
    - Admins can delete any review.
    - Other users can only read.
    """

    def has_object_permission(self, request, view, obj):
        # Allow read-only access to anyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow admin to delete any review
        if request.method == "DELETE" and request.user.is_staff:
            return True
        
        # Allow the owner to update/delete their own review
        return obj.user == request.user