from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from ..models import User
from ..serializers import UserSerializer
from ..permissions import IsAdminUserOrReadOnly


@extend_schema(
    tags=['Users'],
    parameters=[
        OpenApiParameter("username", type=str,
                         description="Username for the account",
                         required=True),
        OpenApiParameter("email", type=OpenApiTypes.EMAIL,
                         description="User email", required=True),
        OpenApiParameter("first_name", type=str,
                         description="User first name", required=True),
        OpenApiParameter("last_name", type=str,
                         description="User last name", required=True),
        OpenApiParameter("password", type=str,
                         description="User password", required=True)
    ]
)
class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []


@extend_schema(tags=['Users'])
class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'


@extend_schema(tags=['Users'])
class UserDeleteView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]

    def delete(self, request, username, *args, **kwargs):
        user = get_object_or_404(User, username=username)
        user.delete()
        return Response(
            {'message': f'User {user.username} was successfully deleted.'},
            status=status.HTTP_200_OK
        )


@extend_schema(
    tags=['Users'],
    parameters=[
        OpenApiParameter("username", type=str,
                         description="Username", required=True),
        OpenApiParameter("password", type=str,
                         description="User password", required=True)
    ]
)
class UserLoginView(APIView):
    permission_classes = []
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            access_token['privileged'] = user.is_staff

            return Response({
                'refresh': str(refresh),
                'access': str(access_token),
                'username': user.username,
                'privileged': user.is_staff
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'},
                            status=status.HTTP_401_UNAUTHORIZED)
