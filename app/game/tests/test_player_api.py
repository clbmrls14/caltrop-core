from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core import models

from game.serializers import PlayerSerializer

PLAYERS_URL = reverse('game:player-list')


def game_detail_url(game_id):
    """Return game details URL based on game id"""
    return reverse('game:game-details', args=[game_id])


class PublicPlayersApiTests(TestCase):
    """Test the publicly available player API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access players"""
        res = self.client.get(PLAYERS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePlayersApiTest(TestCase):
    """Test the private players API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user('test@gmail.com', 'testpassword')
        self.game = models.Game.objects.create(
            owner=self.user,
            title='Test Game',
        )
        self.client.force_authenticate(self.user)

    # def test_retrieve_player_list(self):
    #     """Test retrieving a list of players"""
    #     models.Player.objects.create(name='Test Player 1')
    #     models.Player.objects.create(name='Test Player 2')

    #     res = self.client.get(PLAYERS_URL)

    #     players = models.Player.objects.all().order_by('-name')
    #     serializer = PlayerSerializer(players, many=True)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)

    # def test_players_limited_to_game(self):
    #     """Test that only players for a specific game are returned"""
    #     game2 = models.Game.objects.create(
    #         owner=self.user,
    #         title='Test Game',
    #     )
    #     game2.add(models.Player.objects.create(
    #         game=game2, name='Test Player 1'))

    #     player = models.Player.objects.create(
    #         game=self.game, name='Test Player 2')
    #     self.game.add(player)

    #     res = self.client.get(PLAYERS_URL, game2)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['name'], player.name)
