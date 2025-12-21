from rest_framework.permissions import BasePermission,SAFE_METHODS 


class IsAdminUserOrReadOnly(BasePermission):
    """
    Custom permission to allow only admin users to edit objects,
    while allowing read-only access to others.
    """
    
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
    

class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to allow only owners of an object or admin users to access it.
    """
    
    def has_object_permission(self, request, view, obj):
        return request.user and (request.user.is_staff or obj == request.user)