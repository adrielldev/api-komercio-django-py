from rest_framework import permissions

class ProductPermission(permissions.BasePermission):
    def has_permission(self, request, view):
            if request.method in permissions.SAFE_METHODS:
                return True
            
            if str(request.user) == 'AnonymousUser':
                return False
            return request.user.is_seller 

class ProductOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
                return True
        
        return request.user == obj.seller