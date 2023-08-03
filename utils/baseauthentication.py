import jwt

from django.middleware.csrf import CsrfViewMiddleware
from django.views.decorators.csrf import csrf_exempt
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from django.conf import settings
from users.models import User

class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        # Return the failure reason instead of an HttpResponse
        return reason


class UserAuthentication(BaseAuthentication):
    """
    custom authentication class for DRF, Fernet and JWT
    """

    @csrf_exempt
    def authenticate(self, request):
        authorization_header = request.headers.get("Authorization")
        if not authorization_header:
            raise exceptions.AuthenticationFailed("User token is required")


        try:
            """DECODE FERNET TOKEN"""
            access_token = authorization_header.split(" ")[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=["HS256"]
            )
        except IndexError:
            raise exceptions.AuthenticationFailed("Token prefix missing")
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise exceptions.NotAcceptable("Invalid token")

        user = User.objects.filter(id=payload["id"]).first()

        if user is None:
            raise exceptions.AuthenticationFailed("User not found")

        return user, None


def encode_jwt_token(instance):
    payload = {
        "iss": "showbiz",
        "id": str(instance.id),
        "role": instance.role,
    }
    jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return jwt_token

