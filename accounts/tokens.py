from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

CustomUser = get_user_model()


def get_tokens_for_user(CustomUser):
    refresh = RefreshToken.for_user(CustomUser)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }