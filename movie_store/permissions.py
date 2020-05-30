from rest_framework import permissions


def check_permissions(object_owner, user):
    return object_owner == user


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        obj_owner_field = view.owner_field
        return check_permissions(getattr(obj, obj_owner_field), request.user)