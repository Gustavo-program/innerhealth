from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .serializers import UserSerializer
from core.models import Doctor, Patient
from .models import User


class UserListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer


class LoginAPIView(APIView):
    """
    Login view.
    RETURNS Authentication Token.

    METHOD POST.
    Body.
    {
        "username": "",
        "password": "",
    }
    """
    permission_classes = (AllowAny, )

    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        if email in ['', None]:
            return Response({"detail": "No se proporciono un nombre de usuario"},
                            HTTP_400_BAD_REQUEST)

        if password in ['', None]:
            return Response({"detail": "No se proporciono una contrasenha de usuario"},
                            HTTP_400_BAD_REQUEST)

        user = authenticate(username=email, password=password)

        if not user:
            return Response({"detail": "Se proporcionaron credenciales invalidas"},
                            HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)

        is_doctor = Doctor.objects.filter(user=user).exists()
        is_patient = Patient.objects.filter(user=user).exists()

        user_data = {
            "user_id": user.id,
            "email": user.email,
            "token": token.key,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "is_doctor": is_doctor,
            "is_patient": is_patient
        }

        return Response(data=user_data, status=HTTP_200_OK)


class SignUpAPIView(APIView):
    """
    Sign-up View.
    RETURNS User Instance

    METHOD POST.
    Body.
    {
        "password": "",
        "email": "",
    }
    """
    permission_classes = (AllowAny, )

    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        is_staff = request.data.get("is_staff", False)

        if email in ['', None]:
            return Response({"detail": "No se proporciono un email de usuario"},
                            HTTP_400_BAD_REQUEST)

        if password in ['', None]:
            return Response({"detail": "No se proporciono una contrasenha de usuario"},
                            HTTP_400_BAD_REQUEST)

        if len(password) < 6:
            return Response({"detail": "El password debe tener longitud de al menos 6 caracteres"},
                            HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email):
            return Response({"detail": "El nombre de usuario ya ha sido tomado"},
                            HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            email=email,
            password=password,
            is_staff=is_staff,
        )

        user_data = {
            "user_id": user.id,
            "email": user.email,
            "is_staff": user.is_staff,
        }

        return Response(data=user_data, status=HTTP_200_OK)
