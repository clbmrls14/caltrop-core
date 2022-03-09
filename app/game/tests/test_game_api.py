from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Game, Player

from game.serializers import GameSerializer, GameDetailSerializer

GAMES_URL = reverse('game:game-list')


def game_detail_url(game_id):
    """Return game details URL based on game id"""
    return reverse('game:game-detail', args=[game_id])


def get_sample_game(user, **params):
    """Create and return a default game for testing"""
    defaults = {
        'title': 'Test Game',
    }
    defaults.update(params)

    return Game.objects.create(owner=user, **defaults)


def get_sample_player(name='Test Player'):
    return Player.objects.create(name='name')


class PublicGamesApiTests(TestCase):
    """Test the publicly available games API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to retrieve games"""
        res = self.client.get(GAMES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateGamesApiTests(TestCase):
    """Test the authorized user games API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpassword'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_games(self):
        """Test retrieving games"""
        Game.objects.create(owner=self.user, title='Test Game 1')
        Game.objects.create(owner=self.user, title='Test Game 2')
        Game.objects.create(owner=self.user, title='Test Game 3')

        res = self.client.get(GAMES_URL)

        games = Game.objects.all().order_by('-id')
        serializer = GameSerializer(games, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_games_limited_to_user(self):
        """Test that we only get games returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'test2@gmail.com',
            'testpassword'
        )
        Game.objects.create(owner=user2, title='Test Game 1')
        game = Game.objects.create(owner=self.user, title='Test Game 2')

        res = self.client.get(GAMES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], game.title)

    def test_create_game_successful(self):
        """Test creating a new game"""
        payload = {'title': 'Test Game'}
        self.client.post(GAMES_URL, payload)

        self.assertTrue(Game.objects.filter(
            owner=self.user,
            title=payload['title']
        ).exists())

    def test_create_game_invalid(self):
        """Test creating a new game with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(GAMES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_game_details(self):
        """Test retrieving details about a game"""
        game = get_sample_game(user=self.user)
        game.players.add(get_sample_player())

        url = game_detail_url(game.id)
        res = self.client.get(url)

        serialializer = GameDetailSerializer(game)
        self.assertEqual(res.data, serialializer.data)
