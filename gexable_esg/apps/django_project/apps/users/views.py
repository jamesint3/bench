from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .authentication import BearerTokenAuthentication, AuthenticatedUserPermission, issue_user_token, revoke_token


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"detail": "email is required"}, status=status.HTTP_400_BAD_REQUEST)

        User = get_user_model()
        user = User.objects.filter(email=email, is_active=True).first()
        if not user:
            return Response({"authenticated": False, "detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        token = issue_user_token(user)
        return Response(
            {
                "authenticated": True,
                "access_token": token,
                "token_type": "Bearer",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": getattr(user, "first_name", ""),
                    "last_name": getattr(user, "last_name", ""),
                    "is_superuser": bool(getattr(user, "is_superuser", False)),
                },
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [AuthenticatedUserPermission]

    def post(self, request):
        token = request.auth
        if token:
            revoke_token(token)
        return Response({"logged_out": True}, status=status.HTTP_200_OK)


class MeView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [AuthenticatedUserPermission]

    def get(self, request):
        user = request.user
        return Response(
            {
                "id": user.id,
                "email": getattr(user, "email", ""),
                "first_name": getattr(user, "first_name", ""),
                "last_name": getattr(user, "last_name", ""),
                "is_superuser": bool(getattr(user, "is_superuser", False)),
            }
        )
