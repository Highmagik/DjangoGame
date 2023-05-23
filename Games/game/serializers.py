from rest_framework import serializers
from django.core.cache import cache
from .models import Game, User

class GameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Game
        fields = '__all__'

    def to_representation(self, instance):
        cache_key = f'game_{instance.id}'
        game = cache.get(cache_key)
        if game is None:
            game = super().to_representation(instance)
            cache.set(cache_key, game, 60)
        return game


class UserSerializer(serializers.ModelSerializer):
    game = GameSerializer()

    class Meta:
        model = User
        fields = ("id", "name", "stage1", "stage2", "game")

class UserSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "name", "stage1", "stage2", "game")