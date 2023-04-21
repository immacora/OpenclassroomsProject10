from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from .views import (
    SignupAPIView,
    ProjectListAPIView,
    ProjectDetailAPIView,
    ContributorsAPIView,
    ContributorDeleteAPIView
)

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('projects/', ProjectListAPIView.as_view(), name='projects'),
    path('projects/<uuid:pk>/', ProjectDetailAPIView.as_view(), name='project_detail'),
    path('projects/<uuid:pk>/users/', ContributorsAPIView.as_view(), name='contributors'),
    path('projects/<uuid:pk>/users/<uuid:pk>', ContributorDeleteAPIView.as_view(), name='delete_contributor'),
    #projects/<uuid:pk>/issues/
    #projects/<uuid:pk>/issues/<uuid:pk>
    #projects/<uuid:pk>/issues/<uuid:pk>/comments/
    #projects/<uuid:pk>/issues/<uuid:pk>/comments/<uuid:pk>
]
