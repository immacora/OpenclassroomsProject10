import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models

class Project(models.Model):
    """Projet."""
    PROJECT_TYPE = (
        (0, 'back-end'),
        (1, 'front-end'),
        (2, 'iOS'),
        (3, 'Android'),
    )
    id = models.UUIDField(
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
    type = models.PositiveSmallIntegerField(
        'Type ',
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        choices=PROJECT_TYPE,
    )
    time_created = models.DateTimeField(
        'Date de création',
        auto_now_add=True
    )
    """contributor_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Contributor',
        related_name='contributions'
    )"""

    class Meta:
        ordering = ["-time_created"]

    def __str__(self):
        return self.title
