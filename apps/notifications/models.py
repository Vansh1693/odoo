from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import BaseModel

User = get_user_model()


class Notification(BaseModel):
    """
    Notification model for user notifications.
    """
    NOTIFICATION_TYPES = [
        ('answer', 'New Answer'),
        ('comment', 'New Comment'),
        ('mention', 'Mention'),
        ('answer_accepted', 'Answer Accepted'),
        ('vote', 'Vote Received'),
        ('system', 'System Notification'),
    ]
    
    recipient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications_received'
    )
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications_sent',
        null=True,
        blank=True
    )
    
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Generic relation to any object
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object_type = models.CharField(max_length=50, null=True, blank=True)
    
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['recipient', 'is_read']),
        ]

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.title}"

    def mark_as_read(self):
        """Mark notification as read."""
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])

    def get_related_url(self):
        """Get URL for the related object."""
        if self.related_object_type == 'question':
            from apps.questions.models import Question
            try:
                question = Question.objects.get(pk=self.related_object_id)
                return question.get_absolute_url()
            except Question.DoesNotExist:
                pass
        elif self.related_object_type == 'answer':
            from apps.answers.models import Answer
            try:
                answer = Answer.objects.get(pk=self.related_object_id)
                return answer.question.get_absolute_url()
            except Answer.DoesNotExist:
                pass
        return '#'
