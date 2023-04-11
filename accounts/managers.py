from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):
    """Gestionnaire personnalisé utilisant l'email comme identifiant unique."""

    def create_user(self, email, last_name, first_name, password, **extra_fields):
        if not email:
            raise ValueError(_("L'email est obligatoire"))
        if not first_name:
            raise ValueError(_("Le prénom est obligatoire"))
        if not last_name:
            raise ValueError(_("Le nom est obligatoire"))
        email = self.normalize_email(email)
        user = self.model(email=email, last_name=last_name, first_name=first_name, **extra_fields)
        user.password = make_password(password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, last_name, first_name, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        if extra_fields.get("is_active") is not True:
            raise ValueError(_("Superuser must have is_active=True."))       
        return self.create_user(email, last_name, first_name, password, **extra_fields)
