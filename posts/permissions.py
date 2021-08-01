from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Check if user is admin or is the owner of record.
    """

    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_staff):
            return True
        
        return obj.writer.id == request.user.id
