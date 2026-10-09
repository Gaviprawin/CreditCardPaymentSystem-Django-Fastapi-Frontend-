from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    RegisterSerializer,
    MyTokenObtainPairSerializer,
    UserSerializer,
)


class RegisterView(generics.CreateAPIView):

    serializer_class = RegisterSerializer

    permission_classes = [AllowAny]


class LoginView(TokenObtainPairView):

    serializer_class = MyTokenObtainPairSerializer


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {
                    "message": "Refresh token is required."
                },
                status=400
            )

        try:

            token = RefreshToken(refresh_token)

            token.blacklist()

            return Response(
                {
                    "message": "Logout successful."
                },
                status=200
            )

        except Exception:

            return Response(
                {
                    "message": "Invalid refresh token."
                },
                status=400
            )


class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(serializer.data)