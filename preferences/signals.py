from django.db.models.signals import post_save
from django.dispatch import receiver

from preferences.models import UserInteraction
from recommender.services import reset_recommendations_cache


@receiver(post_save, sender=UserInteraction)
def reset_cache_on_user_interaction(sender, instance, **kwargs):
    """Сбрасывает кэш рекомендаций после любого изменения UserInteraction."""
    reset_recommendations_cache(instance.user_id_id)
