import uuid
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from helpers.validators import isalphavalidator
from django.db import models
from django.contrib.auth.models import (PermissionsMixin, AbstractBaseUser)

from .managers import CustomUserManager


class CustomUser(PermissionsMixin, AbstractBaseUser):
    """Utilisateur personnalisé."""

    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    email = models.EmailField(_("email address"), blank=False, unique=True)
    username = None
    first_name = models.CharField(_("first name"), validators=[isalphavalidator], max_length=150, blank=False, null=False)
    last_name = models.CharField(_("last name"), validators=[isalphavalidator], max_length=150, blank=False, null=False)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
