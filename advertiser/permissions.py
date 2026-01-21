from rest_framework.permissions import BasePermission

class IsAdvertiserRole(BasePermission):
    
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and request.user.role=="advertiser")