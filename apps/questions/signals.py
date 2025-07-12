from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Question
from apps.answers.models import Answer


@receiver(post_save, sender=Answer)
def update_question_answer_count_on_save(sender, instance, created, **kwargs):
    """Update question answer count when answer is created."""
    if created:
        instance.question.update_answer_count()


@receiver(post_delete, sender=Answer)
def update_question_answer_count_on_delete(sender, instance, **kwargs):
    """Update question answer count when answer is deleted."""
    instance.question.update_answer_count()
