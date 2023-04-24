from django.conf import settings
import uuid
from helpers.validators import ischarfieldvalidator
from helpers.models import TrackingModel
from django.db import models


class Project(TrackingModel):
    """Projet."""
    PROJECT_TYPE = [
        ('BACK-END', 'Back-end'),
        ('FRONT-END', 'Front-end'),
        ('IOS', 'iOS'),
        ('ANDROID', 'Android'),
    ]
    project_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(
        'Titre ',
        validators=[ischarfieldvalidator],
        max_length=128
    )
    description = models.TextField(
        validators=[ischarfieldvalidator],
        max_length=2048
    )
    type = models.CharField(
        'Type ',
        max_length=9,
        choices=PROJECT_TYPE,
    )
    contributors = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        through='Contributor',
        related_name='project_contributors'
    )

    def __str__(self):
        return self.title


class Contributor(TrackingModel):
    """Contributeur."""
    CONTRIBUTOR_PERMISSION = [
        ('AUTHOR', 'Auteur'),
        ('ASSIGNED', 'Assigné'),
    ]
    contributor_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    permission = models.CharField(
        'Permission ',
        max_length=8,
        choices=CONTRIBUTOR_PERMISSION,
    )
    role = models.CharField(
        'Rôle ',
        validators=[ischarfieldvalidator],
        max_length=128,
    )
    user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='utilisateur',
    )
    project_id = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        verbose_name='projet',
    )

    class Meta:
        """Interdit le doublon d'assignement d'un utilisateur au projet."""
        unique_together = ('user_id', 'project_id')

    def __str__(self):
        return f"Contributeur {self.user_id.last_name} {self.user_id.first_name} au projet {self.project_id.title}"

    def is_author(self):
        """Retourne True si la permission du contributeur est auteur."""
        return self.permission == "AUTHOR"


class Issue(TrackingModel):
    """Problèmes."""
    TAG = [
        ('BUG', 'Bug'),
        ('IMPROVEMENT', 'Amélioration'),
        ('TASK', 'Tâche')
    ]
    PRIORITY = [
        ('WEAK', 'Faible'),
        ('MEDIUM', 'Moyenne'),
        ('HIGH', 'Élevée')
    ]
    STATUS = [
        ('TODO', 'À faire'),
        ('ONGOING', 'En cours'),
        ('ENDED', 'Terminé')
    ]
    issue_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(
        'Titre ',
        validators=[ischarfieldvalidator],
        max_length=128
    )
    description = models.TextField(
        validators=[ischarfieldvalidator],
        max_length=2048
    )
    tag = models.CharField(
        'Balise ',
        max_length=11,
        choices=TAG
    )
    priority = models.CharField(
        'Priorité ',
        max_length=6,
        choices=PRIORITY
    )
    status = models.CharField(
        'Statut ',
        max_length=7,
        choices=STATUS
    )
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="author_user_id",
        verbose_name='utilisateur auteur'
    )
    project_id = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        verbose_name='projet'
    )
    assigned_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned_user_id",
        verbose_name='utilisateur assigné'
    )

    def __str__(self):
        return self.title


class Comment(TrackingModel):
    """Commentaire."""
    comment_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    description = models.TextField(
        validators=[ischarfieldvalidator],
        max_length=2048
    )
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comment_author_user_id",
        verbose_name='auteur du commentaire'
    )
    issue_id = models.ForeignKey(
        to=Issue,
        on_delete=models.CASCADE,
        verbose_name='projet'
    )
    
    def __str__(self):
        return f"Commentaire de {self.author_user_id.last_name} {self.author_user_id.first_name} au problème {self.issue_id.title}"
