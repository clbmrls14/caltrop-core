from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Game, Player
from game import serializers


class BaseGameAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Base viewset for user owned game attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the currect authenticated user only"""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0)))
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(user=self.request.user).order_by('-id').distinct()

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(owner=self.request.user)


class GameViewSet(viewsets.ModelViewSet):
    """Manage games in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Game.objects.all()
    serializer_class = serializers.GameSerializer

    def get_queryset(self):
        """Return objects for the currect authenticated user only"""
        return self.queryset.filter(owner=self.request.user).order_by('-title')

    def perform_create(self, serializer):
        """Create a new game"""
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.GameDetailSerializer

        return self.serializer_class


class PlayerViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage players in the database"""
    queryset = Player.objects.all()
    serializer_class = serializers.PlayerSerializer
