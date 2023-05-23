from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from .serializers import GameSerializer, UserSerializer, UserSerializerCreate
from .models import Game, User

class GameViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class UserViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet):
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return UserSerializerCreate
        return UserSerializer
    