from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Answer
from apps.notifications.models import Notification


@receiver(post_save, sender=Answer)
def create_answer_notification(sender, instance, created, **kwargs):
    """Create notification when someone answers a question."""
    if created and instance.created_by != instance.question.created_by:
        Notification.objects.create(
            recipient=instance.question.created_by,
            sender=instance.created_by,
            notification_type='answer',
            title=f"New answer to your question",
            message=f"{instance.created_by.display_name} answered your question: {instance.question.title}",
            related_object_id=instance.question.pk,
            related_object_type='question'
        )


@receiver(post_save, sender=Answer)
def handle_accepted_answer_notification(sender, instance, **kwargs):
    """Create notification when answer is accepted."""
    if instance.is_accepted and instance.created_by != instance.question.created_by:
        # Check if this is a new acceptance (not an update)
        if not Notification.objects.filter(
            recipient=instance.created_by,
            notification_type='answer_accepted',
            related_object_id=instance.pk,
            related_object_type='answer'
        ).exists():
            Notification.objects.create(
                recipient=instance.created_by,
                sender=instance.question.created_by,
                notification_type='answer_accepted',
                title="Your answer was accepted!",
                message=f"Your answer to '{instance.question.title}' was accepted.",
                related_object_id=instance.pk,
                related_object_type='answer'
            )
