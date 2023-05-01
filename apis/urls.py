from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (
    SignupAPIView,
    ProjectListAPIView,
    ProjectDetailAPIView,
    ContributorsAPIView,
    ContributorDeleteAPIView,
    IssuesAPIView,
    IssueAPIView,
    CommentsAPIView,
    CommentAPIView
)

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('projects/', ProjectListAPIView.as_view(), name='projects'),
    path('projects/<uuid:project_id>/', ProjectDetailAPIView.as_view(), name='project_detail'),
    path('projects/<uuid:project_id>/users/', ContributorsAPIView.as_view(), name='contributors'),
    path(
            'projects/<uuid:project_id>/users/<uuid:user_id>/',
            ContributorDeleteAPIView.as_view(),
            name='delete_contributor'
        ),
    path('projects/<uuid:project_id>/issues/', IssuesAPIView.as_view(), name='issues'),
    path(
            'projects/<uuid:project_id>/issues/<uuid:issue_id>/',
            IssueAPIView.as_view(),
            name='issue'
        ),
    path('projects/<uuid:project_id>/issues/<uuid:issue_id>/comments/', CommentsAPIView.as_view(), name='comments'),
    path(
            'projects/<uuid:project_id>/issues/<uuid:issue_id>/comments/<uuid:comment_id>/',
            CommentAPIView.as_view(), name='comment'
        )
]
