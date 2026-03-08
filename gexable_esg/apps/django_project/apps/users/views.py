from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"detail": "email is required"}, status=status.HTTP_400_BAD_REQUEST)

        User = get_user_model()
        user = User.objects.filter(email=email).first()
        return Response(
            {
                "authenticated": bool(user),
                "user_id": getattr(user, "id", None),
                "email": email,
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        return Response({"logged_out": True}, status=status.HTTP_200_OK)


class MeView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        email = request.headers.get("X-User-Email")
        User = get_user_model()
        user = User.objects.filter(email=email).first() if email else User.objects.first()
        if not user:
            return Response({"user": None}, status=status.HTTP_200_OK)
        return Response(
            {
                "id": user.id,
                "email": getattr(user, "email", ""),
                "first_name": getattr(user, "first_name", ""),
                "last_name": getattr(user, "last_name", ""),
                "is_superuser": bool(getattr(user, "is_superuser", False)),
            }
        )
