import datetime
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from projects.permissions import IsProjectContributor, IsProjectAuthorOrReadOnlyContributor
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView

from projects.models import Project, Contributor
from .serializers import SignupSerializer, ProjectListSerializer, ProjectDetailSerializer, ContributorSerializer

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
    Afficher la liste des projets auxquels l'utilisateur connecté contribue (permission: settings IsAuthenticated + filtre queryset).
    Créer un projet en tant que contributeur-auteur (permission 'AUTHOR' et role 'Propriétaire').
    """
    serializer_class = ProjectListSerializer

    def get_queryset(self):
        user = self.request.user
        return user.project_contributors.all()

    def post(self, request, *args, **kwargs):
        serializer = ProjectDetailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = request.user
            project = serializer.save()
            Contributor.objects.create(
                permission='AUTHOR',
                role='Propriétaire',
                user_id=user,
                project_id=project
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, *args, **kwargs)


class ProjectDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    Afficher le détail du projet auquel l'utilisateur connecté contribue (filtrage: project_id).
    Mettre à jour le projet (permission: auteur).
    Supprimer le projet (permission: auteur).
    """
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    lookup_field = 'project_id'
    permission_classes = [IsAuthenticated, IsProjectContributor, IsProjectAuthorOrReadOnlyContributor]

    def put(self, request, *args, **kwargs):
        project = self.get_object()
        updated_at = datetime.datetime.now()
        project.updated_at = updated_at
        project.save()
        return self.update(request, *args, **kwargs)


class ContributorsAPIView(ListCreateAPIView):
    """
    Afficher la liste des collaborateurs au projet (filtrage par project_id).
    Ajouter un collaborateur-assigné (permission : auteur).
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
        user_id = request.data['user_id']['user_id']

        if serializer.is_valid(raise_exception=True):
            try:
                custom_user = CustomUser.objects.get(user_id=user_id)
            except Exception:
                return Response({'message': "L'utilisateur n'a pas été trouvé"}, status=status.HTTP_404_NOT_FOUND)
            
            if Contributor.objects.filter(user_id=user_id, project_id=project_id).exists():
                return Response({'message': "L'utilisateur fait déjà partie des contributeurs."}, status=status.HTTP_409_CONFLICT)
            
            project = Project.objects.get(project_id=project_id)

            try:
                Contributor.objects.create(
                permission='ASSIGNED',
                role=request.data['role'],
                user_id=custom_user,
                project_id=project
            )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception:
                return Response({'message': "Une erreur s'est produite, l'utilisateur n'a pas été créé"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(status=status.HTTP_400_BAD_REQUEST, *args, **kwargs)
