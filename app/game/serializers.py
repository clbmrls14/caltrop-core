from rest_framework import serializers

from core.models import Game


class GameSerializer(serializers.ModelSerializer):
    """Serializer for game objects"""

    class Meta:
        model = Game
        fields = ('id', 'title', 'track_health')
        read_only_fields = ('id',)
