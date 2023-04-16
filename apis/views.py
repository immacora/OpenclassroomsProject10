from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from projects.models import Project, Contributor
from .serializers import SignupSerializer, ProjectSerializer#, ContributorSerializer#, CustomUserSerializer

CustomUser = get_user_model()


class SignupAPIView(CreateAPIView):
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
    """Afficher la liste des projets auxquels l'utilisateur connecté contribue."""
    serializer_class = ProjectSerializer

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
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer