import datetime
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from projects.permissions import IsProjectContributor, IsProjectAuthorOrReadOnlyContributor, IsCommentAuthor
from projects.models import Project, Contributor, Issue, Comment
from .serializers import (
    SignupSerializer,
    ProjectListSerializer,
    ProjectDetailSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer
    )

CustomUser = get_user_model()


class SignupAPIView(CreateAPIView):
    """Créer un compte CustomUser."""

    permission_classes = [AllowAny]
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return self.create(request, *args, **kwargs)


class ProjectListAPIView(ListCreateAPIView):
    """
    Afficher la liste des projets auxquels l'utilisateur connecté contribue
    (permission: settings IsAuthenticated + queryset).
    Créer un projet en tant que contributeur-auteur
    (permission 'AUTHOR' et role 'Propriétaire').
    """

    serializer_class = ProjectListSerializer

    def get_queryset(self):
        user = self.request.user
        return user.project_contributors.all()

    def post(self, request, *args, **kwargs):
        serializer = ProjectDetailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            project = serializer.save()
            Contributor.objects.create(
                permission='AUTHOR',
                role='Propriétaire',
                user_id=request.user,
                project_id=project
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, *args, **kwargs)


class ProjectDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    Afficher le détail du projet auquel l'utilisateur connecté contribue (filtrage: project_id).
    Mettre à jour le projet (permission: auteur connecté).
    Supprimer le projet (permission: auteur connecté).
    """

    serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsProjectAuthorOrReadOnlyContributor]

    def get_object(self):
        project_id = self.kwargs['project_id']
        obj = get_object_or_404(Project, project_id=project_id)
        self.check_object_permissions(self.request, obj)
        return obj

    def put(self, request, *args, **kwargs):
        project = self.get_object()
        project.updated_at = datetime.datetime.now()
        project.save()
        return self.update(request, *args, **kwargs)


class ContributorsAPIView(ListCreateAPIView):
    """
    Afficher la liste des collaborateurs au projet (filtrage par project_id).
    Ajouter un collaborateur-assigné si l'utilisateur existe
    et n'est pas déjà rattaché au projet (permission : auteur connecté).
    """

    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsProjectAuthorOrReadOnlyContributor]

    def list(self, request, *args, **kwargs):
        project_id = kwargs['project_id']
        queryset = Contributor.objects.filter(project_id=project_id)

        if not queryset:
            return Response(status=status.HTTP_403_FORBIDDEN)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        project_id = kwargs['project_id']

        if serializer.is_valid(raise_exception=True):

            try:
                user_id = request.data['user_id']['user_id']
                custom_user = CustomUser.objects.get(user_id=user_id)
            except Exception:
                return Response(
                    {'message': "Le champ contributeur est absent ou incorrectement renseigné."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if Contributor.objects.filter(user_id=user_id, project_id=project_id).exists():
                return Response(
                    {'message': "L'utilisateur fait déjà partie des contributeurs."},
                    status=status.HTTP_409_CONFLICT
                )

            project = Project.objects.get(project_id=project_id)
            contributor = Contributor.objects.create(
                permission='ASSIGNED',
                role=request.data['role'],
                user_id=custom_user,
                project_id=project
            )
            json_contributor = ContributorSerializer(contributor)
            json = {
                'rôle': serializer.data,
                'Contributeur': json_contributor.data,
            }
            return Response(json, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST, *args, **kwargs)


class ContributorDeleteAPIView(DestroyAPIView):
    """Supprimer un collaborateur (hors auteur, permission: contributeur connecté)."""

    permission_classes = [IsAuthenticated, IsProjectContributor]

    def delete(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        user_id = self.kwargs['user_id']

        try:
            contributor_to_delete = Contributor.objects.get(user_id=user_id, project_id=project_id)
        except Contributor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if contributor_to_delete:
            requesting_user = Contributor.objects.get(user_id=self.request.user, project_id=project_id)

            if not requesting_user.is_author():
                return Response(status=status.HTTP_403_FORBIDDEN)
            elif contributor_to_delete.is_author():
                return Response(
                    {'message': "L'auteur du projet ne peut pas être supprimé."},
                    status=status.HTTP_403_FORBIDDEN
                )
            else:
                contributor_to_delete.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class IssuesAPIView(ListCreateAPIView):
    """
    Afficher la liste des problèmes du projet (filtrage par project_id).
    Créer un problème lié au projet si l'assigned_user_id est un contributeur
    (utilise la donnée assigned_user_id de contexte pour la création du problème
    ou celle du champ de saisie s'il existe, permission: contributeur connecté)
    """

    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor]
    queryset = Issue.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)

        if self.perform_create(serializer) is False:
            return Response(
                {'message': "L'utilisateur assigné ne fait pas partie des contributeurs"},
                status=status.HTTP_404_NOT_FOUND
            )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        project_id = self.kwargs['project_id']
        project = Project.objects.get(project_id=project_id)

        if (assigned_user_id := self.request.data.get("assigned_user_id")):
            assigned_user = CustomUser.objects.get(user_id=assigned_user_id)

            if Contributor.objects.filter(user_id=assigned_user_id, project_id=project_id).exists():
                serializer.save(project_id=project, assigned_user_id=assigned_user)
                return Response(status=status.HTTP_201_CREATED)
            else:
                return False
        serializer.save(project_id=project)


class IssueAPIView(RetrieveUpdateDestroyAPIView):
    """
    Mettre à jour ou supprimer le problème récupéré par le get_object
    (author du problème + permission: contributeur connecté).
    """

    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor]

    def get_object(self):
        project_id = self.kwargs['project_id']
        issue_id = self.kwargs['issue_id']
        obj = get_object_or_404(Issue, author_user_id=self.request.user, project_id=project_id, issue_id=issue_id)
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        if self.perform_update(serializer) is False:
            return Response(
                {'message': "L'utilisateur assigné ne fait pas partie des contributeurs"},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(serializer.data)

    def perform_update(self, serializer):
        project_id = self.kwargs['project_id']
        assigned_user_id = self.request.data.get("assigned_user_id", None)

        if assigned_user_id:
            try:
                assigned_user = CustomUser.objects.get(user_id=assigned_user_id)
                if Contributor.objects.filter(user_id=assigned_user_id, project_id=project_id).exists():
                    serializer.save(assigned_user_id=assigned_user, updated_at=datetime.datetime.now())
                else:
                    return False
            except CustomUser.DoesNotExist:
                return False
        else:
            serializer.save(updated_at=datetime.datetime.now())


class CommentsAPIView(ListCreateAPIView):
    """
    Afficher la liste des commentaires du problème.
    Créer un commentaire sur un problème du projet (permission: contributeur connecté)
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor]

    def list(self, request, *args, **kwargs):
        issue_id = self.kwargs['issue_id']
        queryset = Comment.objects.filter(issue_id=issue_id)

        if not queryset:
            return Response(status=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        issue_id = self.kwargs['issue_id']
        issue = Issue.objects.get(issue_id=issue_id)
        serializer.save(author_user_id=self.request.user, issue_id=issue)


class CommentAPIView(RetrieveUpdateDestroyAPIView):
    """
    Consulter, mettre à jour ou supprimer le commentaire du problème
    récupéré par le get_object (comment_id + permission: contributeur connecté
    et auteur du commentaire).
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsCommentAuthor]

    def get_object(self):
        comment_id = self.kwargs['comment_id']
        obj = get_object_or_404(Comment, comment_id=comment_id)
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_update(self, serializer):
        serializer.save(updated_at=datetime.datetime.now())
