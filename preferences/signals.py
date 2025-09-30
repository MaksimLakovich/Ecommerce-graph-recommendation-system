from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from preferences.models import UserInteraction
from recommender.services import reset_recommendations_cache


@receiver(post_save, sender=UserInteraction)
def reset_cache_on_user_interaction(sender, instance, **kwargs):
    """Сбрасывает кэш рекомендаций после изменения UserInteraction.
    Используем transaction.on_commit, чтобы дождаться фиксации всех изменений в БД, а не сбрасывать
    после каждого post_save()."""
    user_id = instance.user_id_id

    def _reset_cache():
        reset_recommendations_cache(user_id)

    transaction.on_commit(_reset_cache)
