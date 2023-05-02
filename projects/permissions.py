from django.shortcuts import get_object_or_404
from rest_framework import permissions
from projects.models import Project, Contributor, Comment


class IsProjectContributor(permissions.BasePermission):
    """Autorise l'accès au contributeur connecté et au super utilisateur uniquement."""

    def has_permission(self, request, view):
        project_id = view.kwargs['project_id']
        project = get_object_or_404(Project, project_id=project_id)

        if request.user.is_superuser:
            return True

        if (request.user.is_authenticated and request.user.is_contributor(project)):
            return True

        return False


class IsProjectAuthorOrReadOnlyContributor(permissions.BasePermission):
    """Autorise le CRUD à l'auteur connecté du projet et au super utilisateur
    et les SAFE_METHODS ('GET', 'HEAD', 'OPTIONS') au contributeur connecté."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        project_id = view.kwargs['project_id']
        project = get_object_or_404(Project, project_id=project_id)
        contributor = get_object_or_404(Contributor, user_id=request.user, project_id=project_id)

        if request.user.is_superuser:
            return True

        """try:
            contributor = Contributor.objects.get(
                user_id=request.user,
                project_id=project_id)
        except Contributor.DoesNotExist:
            return False"""

        if contributor.is_author():
            return True

        if request.user.is_contributor(project) and request.method in permissions.SAFE_METHODS:
            return True

        return False


class IsCommentAuthor(permissions.BasePermission):
    """Autorise la modification et la suppression à l'auteur connecté du commentaire d'un problème
    et au super utilisateur."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        comment_id = view.kwargs['comment_id']
        comment = get_object_or_404(Comment, comment_id=comment_id)

        if request.user.is_superuser:
            return True

        if comment.author_user_id == request.user:
            return True

        return False
