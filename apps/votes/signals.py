from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Vote


@receiver(post_save, sender=Vote)
def update_content_vote_score_on_save(sender, instance, **kwargs):
    """Update content vote score when vote is saved."""
    if hasattr(instance.content_object, 'update_vote_score'):
        instance.content_object.update_vote_score()


@receiver(post_delete, sender=Vote)
def update_content_vote_score_on_delete(sender, instance, **kwargs):
    """Update content vote score when vote is deleted."""
    if hasattr(instance.content_object, 'update_vote_score'):
        instance.content_object.update_vote_score()
