from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view
import logging

from .models import User
from .serializers import RegisterSerializer, UserSerializer

logger = logging.getLogger(__name__)

@extend_schema(tags=['Authentication'])
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info("New user registered: %s (id=%s)", user.username, user.id)
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            logger.error("Registration failed: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token


class LoginView(TokenObtainPairView):
    serializer_class = CustomLoginSerializer

    @extend_schema(tags=['Authentication'])
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            logger.info("User %s logged in successfully", request.data.get("username"))
        else:
            logger.warning("Login failed for user %s", request.data.get("username"))
        return response


@extend_schema_view(
    list=extend_schema(tags=['Users']),
    retrieve=extend_schema(tags=['Users']),
    create=extend_schema(tags=['Users']),
    update=extend_schema(tags=['Users']),
    partial_update=extend_schema(tags=['Users']),
    destroy=extend_schema(tags=['Users']),
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer