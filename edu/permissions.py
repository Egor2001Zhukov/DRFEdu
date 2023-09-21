from rest_framework import permissions


class IsModeratorOrCreator(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            if request.user.groups.filter(name="moderators").exists():
                return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        elif request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.method == 'PUT':
                return request.user.groups.filter(name="moderators").exists()
            return False
