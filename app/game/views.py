from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Game
from game import serializers


class GameViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage games in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Game.objects.all()
    serializer_class = serializers.GameSerializer

    def get_queryset(self):
        """Return objects for the currect authenticated user only"""
        return self.queryset.filter(owner=self.request.user).order_by('-title')
