from rest_framework import serializers

from core.models import Game, Player


class PlayerSerializer(serializers.ModelSerializer):
    """Serializer for player objects"""

    class Meta:
        model = Player
        fields = ('id', 'name')
        read_only_fields = ('id',)


class GameSerializer(serializers.ModelSerializer):
    """Serializer for game objects"""
    players = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Player.objects.all()
    )

    class Meta:
        model = Game
        fields = ('id', 'title', 'track_health', 'players')
        read_only_fields = ('id',)


class GameDetailSerializer(GameSerializer):
    """Serialize a game detail"""
    players = PlayerSerializer(many=True, read_only=True)
