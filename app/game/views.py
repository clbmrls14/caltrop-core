from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Game, Player
from game import serializers


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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Player.objects.all()
    serializer_class = serializers.PlayerSerializer

    def get_queryset(self):
        """Return players for the current game"""
        return self.queryset.filter(game=self.request.user).order_by('-name')
