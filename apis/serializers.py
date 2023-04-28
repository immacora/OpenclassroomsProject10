from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework import serializers

from projects.models import Project, Contributor, Issue

CustomUser = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    """Serializer utilisé pour l'inscription du customuser."""

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
    """Serializer du projet intégrant les informations utiles à la logique métier (destiné à la vue de liste)."""

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
    """Serializer intégrant toutes les informations du projet (destiné à la vue de détail)."""

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
    """Serializer du customuser intégrant les informations utiles à la logique métier (destiné au contributeur)."""

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
    """Serializer du contributeur intégrant le détail de l'utilisateur pour la logique métier."""

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
    """Serializer du projet (id du projet et liste des id de ses contributeurs) à intégrer à la liste des problèmes pour la logique métier."""

    class Meta:
        model = Project
        fields = (
            'project_id',
            'contributors'
        )

class IssuesSerializer(serializers.ModelSerializer):
    """
    Serializer du problème à consulter / créer.
    Assigne l'utilisateur-auteur par défaut (utilisateur connecté).
    Utilise le ProjectContributorsSerializer (affichage des infos utiles du projet).
    Assigne l'utilisateur-assigné par défaut (utilisateur connecté) si le champ de saisie est vide.
    """

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
