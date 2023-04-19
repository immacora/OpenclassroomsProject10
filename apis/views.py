import datetime
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from projects.permissions import IsProjectAuthorOrContributorReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from projects.models import Project, Contributor
from .serializers import SignupSerializer, ProjectListSerializer, ProjectDetailSerializer#, ContributorSerializer, #CustomUserSerializer

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
    Afficher la liste des projets auxquels l'utilisateur connecté contribue.
    Créer un projet en tant que contributeur-auteur (permission 'AUTHOR' et role 'Propriétaire').
    """
    serializer_class = ProjectListSerializer

    def get_queryset(self):
        user = self.request.user
        return user.project_contributors.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
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
    Afficher le détail du projet auquel l'utilisateur connecté contribue.
    Mettre à jour le projet (permission : auteur).
    Supprimer le projet (permission : auteur).
    """
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated, IsProjectAuthorOrContributorReadOnly]

    def put(self, request, *args, **kwargs):
        project = self.get_object()
        updated_at = datetime.datetime.now()
        project.updated_at = updated_at
        project.save()
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': "Le projet a été supprimé"}, status=status.HTTP_200_OK)
