from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserDetailSerializer

User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for User model.
    """
    queryset = User.objects.filter(is_active=True, is_banned=False)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer

    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        """Get top users by reputation."""
        top_users = User.objects.filter(
            is_active=True, 
            is_banned=False
        ).order_by('-reputation')[:10]
        
        serializer = self.get_serializer(top_users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """Get current user profile."""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
