from rest_framework.permissions import BasePermission


class FileDecryptPermission(BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.user == obj.user:
            return True

        return request.user.groups.filter(
            files__id__in=[obj.id],
            permissions__codename='decrypt_file'
        ).exists()


class FileViewPermission(BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.user == obj.user:
            return True

        return request.user.groups.filter(
            files__id__in=[obj.id],
            permissions__codename='view_file'
        ).exists()
