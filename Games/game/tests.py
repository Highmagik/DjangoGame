import json
from django.urls import reverse
from .models import Game, User
from datetime import datetime
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .serializers import GameSerializer, UserSerializer
from django.urls import reverse
from django.core.cache import cache
from collections import OrderedDict

class GameViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_game(self):
        url = reverse('game-list')
        data = {'id': 1,
                'name': 'test game',
                'description': 'test description',
                'stage_number':1,
                'end_date': '20.04.2023'}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Game.objects.count(), 1)
        game = Game.objects.first()
        expected_data = {'id': game.id,
                         'name': game.name,
                         'description': game.description,
                         'stage_number': game.stage_number,
                         'end_date': game.end_date.strftime('%d.%m.%Y')}
        self.assertEqual(data, expected_data)
        cache.delete(f'game_{data["id"]}')

    def test_update_game(self):
        game = Game.objects.create(id=10,
                                   name='test game',
                                   description='test description',
                                   stage_number=1,
                                   end_date='2023-04-01')
        url = reverse('game-detail', args=[game.id])
        data = {'id': 10,
                'name': 'test game',
                'description': 'updated description',
                'stage_number': 1,
                'end_date': '23.04.2023'}
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        game.refresh_from_db()
        expected_data = {'id': game.id,
                         'name': game.name,
                         'description': game.description,
                         'stage_number': game.stage_number,
                         'end_date': game.end_date.strftime('%d.%m.%Y')}
        self.assertEqual(data, expected_data)
        cache.delete(f'game_{game.id}')

    def test_retrieve_game(self):
        game = Game.objects.create(id=1,
                                   name='test game',
                                   description='test description',
                                   stage_number=1,
                                   end_date='2023-04-01')
        url = reverse('game-detail', args=[game.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {'id': game.id,
                         'name': game.name,
                         'description': game.description,
                         'stage_number': game.stage_number,
                         'end_date': datetime.strptime(game.end_date, '%Y-%m-%d').strftime('%d.%m.%Y')}
        self.assertEqual(response.data, expected_data)
        cache.delete(f'game_{game.id}')


class UserViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        game = Game.objects.create(id = 10,
                                   name='test game',
                                   description='test description',
                                   stage_number=1,
                                   end_date='2023-04-01')
        url = reverse('user-list')
        data = {'id': 1,
                'name': 'test user',
                'stage1': True,
                'stage2': False,
                'game': game.id}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        expected_data = {'id': user.id,
                         'name': user.name,
                         'stage1': user.stage1,
                         'stage2': user.stage2,
                         'game': user.game.id}
        self.assertEqual(data, expected_data)
        cache.delete(f'game_{game.id}')
        
    def test_update_user(self):
        game = Game.objects.create(id = 10,
                                   name='test game',
                                   description='test description',
                                   stage_number=1,
                                   end_date='2023-04-01')
        user = User.objects.create(id=10,
                                   name='test user',
                                   stage1=True,
                                   stage2=False,
                                   game=game)
        url = reverse('user-detail', args=[user.id])
        data = {'id': 10,
                'name': 'updated user',
                'stage1': True,
                'stage2': False,
                'game': game.id}
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        expected_data = {'id': user.id,
                         'name': user.name,
                         'stage1': user.stage1,
                         'stage2': user.stage2,
                         'game': user.game.id}
        self.assertEqual(data, expected_data)
        cache.delete(f'game_{game.id}')

    def test_retrieve_user(self):
        game = Game.objects.create(id = 10,
                                   name='test game',
                                   description='test description',
                                   stage_number=1,
                                   end_date='2023-04-01')
        user = User.objects.create(id=10,
                                   name='test user',
                                   stage1=True,
                                   stage2=False,
                                   game=game)
        url = reverse('user-detail', args=[user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        game_dict = OrderedDict([('id', game.id),
                                 ('name', game.name),
                                 ('description', game.description),
                                 ('stage_number', game.stage_number),
                                 ('end_date', datetime.strptime(game.end_date, '%Y-%m-%d').strftime('%d.%m.%Y'))])
        expected_data = {
            'id': user.id,
            'name': user.name,
            'stage1': user.stage1,
            'stage2': user.stage2,
            'game': game_dict,
        }
        self.assertEqual(response.data, expected_data)
        cache.delete(f'game_{game.id}')


class GameSerializerTests(TestCase):

    def test_serialize_game(self):
        game = Game.objects.create(id = 10,
                                   name='test game',
                                   description='test description',
                                   stage_number=1,
                                   end_date='2023-04-01')
        serializer = GameSerializer(game)
        expected_data = {'id': game.id,
                         'name': game.name,
                         'description': game.description,
                         'stage_number': game.stage_number,
                         'end_date': game.end_date}
        self.assertEqual(serializer.data, expected_data)
        cache.delete(f'game_{game.id}')

    def test_serialize_game_caches_result(self):
        game = Game.objects.create(id = 10,
                                   name='test game',
                                   description='test description',
                                   stage_number=1,
                                   end_date='2023-04-01')
        serializer = GameSerializer(game)
        cache_key = f'game_{game.id}'
        data = serializer.data
        self.assertEqual(data, 
                         {'id': game.id,
                         'name': game.name,
                         'description': game.description,
                         'stage_number': game.stage_number,
                         'end_date': game.end_date})
        self.assertIsNotNone(cache.get(cache_key))
        cache.delete(f'game_{game.id}')


class UserSerializerTests(TestCase):

    def test_serialize_user(self):
        game = Game.objects.create(id = 10,
                                   name='test game',
                                   description='test description',
                                   stage_number=1,
                                   end_date='2023-04-01')
        user = User.objects.create(id=10,
                                   name='test user',
                                   stage1=True,
                                   stage2=False,
                                   game=game)
        serializer = UserSerializer(user)
        game_dict = OrderedDict([('id', game.id),
                                 ('name', game.name),
                                 ('description', game.description),
                                 ('stage_number', game.stage_number),
                                 ('end_date', game.end_date)])
        expected_data = {
            'id': user.id,
            'name': user.name,
            'stage1': user.stage1,
            'stage2': user.stage2,
            'game': game_dict
        }
        self.assertEqual(serializer.data, expected_data)
        cache.delete(f'game_{game.id}')