from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if  request.method in permissions.SAFE_METHODS or \
            request.user.is_authenticated:
            return True
        
    def has_object_permission(self, request, view, obj):

        if  request.method in permissions.SAFE_METHODS :
            return True
        
        return bool (obj.author == request.user or  request.user.is_superuser)


            

