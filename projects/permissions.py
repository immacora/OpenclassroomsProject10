from rest_framework import permissions
from django.http import Http404
from projects.models import Contributor

BaseException
class IsProjectAuthorOrContributorReadOnly(permissions.BasePermission):
    """Autorise les SAFE_METHODS ('GET', 'HEAD', 'OPTIONS') au contributeur connecté et les méthodes PUT et DELETE au contributeur auteur ou au super utilisateur."""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        try:
            contributor = Contributor.objects.get(user_id=request.user, project_id=obj)
        except Contributor.DoesNotExist:
            raise Http404
        if contributor.is_author():
            return True
        if obj in request.user.project_contributors.all() and request.method in permissions.SAFE_METHODS:
            return True
        return False