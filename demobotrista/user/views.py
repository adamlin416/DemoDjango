from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import CanListUsersPermission
from .serializers import UserSerializer, UserUpdateSerializer

User = get_user_model()


class UserListAPIView(APIView):
    """
    Get a list of all users or create a new user.
    """

    def get_permissions(self):
        if self.request.method == "POST":
            # Allow any user to create an account, or restrict as necessary
            return [AllowAny()]
        return [CanListUsersPermission()]  # Only allow users with the permission

    @extend_schema(
        operation_id="users_list",
        request=None,
        responses={200: UserSerializer(many=True)},
    )
    def get(self, request):
        """Return a list of all users. Only managers can list all users."""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=UserSerializer,
        responses={201: UserSerializer},
    )
    def post(self, request):
        """Create a new user. Does NOT NEED logged in."""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(APIView):
    """
    Perform CRUD operations on the logged-in user's own data.
    Path `/users/<id>` will check if `id` is the ID of the currently logged-in user.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={200: UserSerializer},
    )
    def get(self, request, pk):
        """Get the user's own information if `id` is their ID."""
        if pk == request.user.id:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        else:
            return Response(
                {"detail": "You can only access your own data."},
                status=status.HTTP_403_FORBIDDEN,
            )

    @extend_schema(
        request=UserUpdateSerializer,
        responses={200: UserUpdateSerializer},
    )
    def put(self, request, pk):
        """Update the user's own information if `id` is their ID."""
        if pk == request.user.id:
            serializer = UserUpdateSerializer(
                request.user, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"detail": "You can only update your own data."},
                status=status.HTTP_403_FORBIDDEN,
            )

    def delete(self, request, pk):
        """Delete the user's own account if `id` is their ID."""
        if pk != request.user.id:
            return Response(
                {"detail": "You can only delete your own account."},
                status=status.HTTP_403_FORBIDDEN,
            )
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
