from rest_framework import permissions


class IsParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user in obj.participants.all():
            return True
