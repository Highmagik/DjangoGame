from django.core.cache import cache
from django.dispatch import receiver
from .serializers import GameSerializer
from django.db.models.signals import post_save, post_delete, post_init
from .models import Game


@receiver([post_save, post_delete, post_init], sender=Game)
def update_post_save_cache(sender, instance, **kwargs):
    cache.delete(f'game_{instance.id}')
    GameSerializer(instance=instance).to_representation(instance)
    

