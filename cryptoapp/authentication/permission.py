from rest_framework.permissions import BasePermission


class OwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        queryset = view.get_queryset().filter(user=request.user, pk=obj.id)

        return queryset.exists()


