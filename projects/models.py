from django.conf import settings
import uuid
from django.db import models


class Project(models.Model):
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
        max_length=128
    )
    description = models.TextField(
        max_length=2048,
        blank=True
    )
    type = models.CharField(
        'Type ',
        max_length=9,
        choices=PROJECT_TYPE,
    )
    contributors = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        through='Contributor',
        related_name='contributions'
    )

    def __str__(self):
        return self.title


class Contributor(models.Model):
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
        max_length=128
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
        unique_together = ('user_id', 'project_id')

    def __str__(self):
        return f"Contributeur {self.user_id.last_name} {self.user_id.first_name} au projet {self.project_id.title}"
