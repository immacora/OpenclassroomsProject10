from django.db import models


class TrackingModel(models.Model):
    created_at = models.DateTimeField(
        'Date de création',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        'Date de modification',
        auto_now_add=True
    )

    class Meta:
        abstract = True
        ordering = ("-created_at",)
