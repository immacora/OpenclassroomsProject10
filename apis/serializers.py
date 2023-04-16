from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework import serializers

from projects.models import Project, Contributor

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


class ProjectSerializer(serializers.ModelSerializer):

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


class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields = (
            'created_at',
            'updated_at',
            'contributor_id',
            'permission',
            'role',
            'user_id',
            'project_id'
        )
