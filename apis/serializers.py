from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework import serializers

from projects.models import Project, Contributor, Issue

CustomUser = get_user_model()


class SignupSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=68,
        min_length=8,
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        max_length=68,
        min_length=8,
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )

    class Meta:
        model = CustomUser
        fields = ('user_id', 'email', 'first_name', 'last_name', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop("password2")
        return CustomUser.objects.create_user(**validated_data)


class ProjectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = (
            'created_at',
            'updated_at',
            'project_id',
            'title',
            'type'
        )


class ProjectDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = (
            'created_at',
            'updated_at',
            'project_id',
            'title',
            'description',
            'type',
            'contributors'
        )


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'user_id',
            'email',
            'first_name',
            'last_name',
            'date_joined',
        )

class ContributorSerializer(serializers.ModelSerializer):

    user_id = CustomUserSerializer(read_only=True)

    class Meta:
        model = Contributor
        fields = (
            'created_at',
            'contributor_id',
            'role',
            'user_id'
        )


class ProjectContributorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = (
            'project_id',
            'contributors'
        )

class IssuesSerializer(serializers.ModelSerializer):

    author_user_id = serializers.UUIDField(
        default=serializers.CurrentUserDefault()
    )
    assigned_user_id = serializers.UUIDField(
        default=serializers.CurrentUserDefault()
    )
    project_id = ProjectContributorsSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = (
            'created_at',
            'updated_at',
            'issue_id',
            'title',
            'description',
            'tag',
            'priority',
            'status',
            'author_user_id',
            'project_id',
            'assigned_user_id'
        )
        read_only_fields = ['author_user_id']
