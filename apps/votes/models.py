from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from apps.core.models import BaseModel

User = get_user_model()


class Vote(BaseModel):
    """
    Generic voting model for questions and answers.
    """
    VOTE_CHOICES = [
        (1, 'Upvote'),
        (-1, 'Downvote'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    value = models.SmallIntegerField(choices=VOTE_CHOICES)
    
    # Generic foreign key to vote on any model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ['user', 'content_type', 'object_id']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        vote_type = "upvote" if self.value == 1 else "downvote"
        return f"{self.user.username} {vote_type} on {self.content_object}"

    def save(self, *args, **kwargs):
        # Prevent users from voting on their own content
        if hasattr(self.content_object, 'created_by') and self.user == self.content_object.created_by:
            raise ValueError("Users cannot vote on their own content")
        
        super().save(*args, **kwargs)
        
        # Update vote score on the content object
        if hasattr(self.content_object, 'update_vote_score'):
            self.content_object.update_vote_score()
        
        # Award/remove reputation
        self._update_reputation()

    def delete(self, *args, **kwargs):
        content_object = self.content_object
        super().delete(*args, **kwargs)
        
        # Update vote score on the content object
        if hasattr(content_object, 'update_vote_score'):
            content_object.update_vote_score()
        
        # Remove reputation changes
        self._update_reputation(remove=True)

    def _update_reputation(self, remove=False):
        """Update reputation for content author based on vote."""
        if not hasattr(self.content_object, 'created_by') or not self.content_object.created_by:
            return
        
        author = self.content_object.created_by
        multiplier = -1 if remove else 1
        
        if self.value == 1:  # Upvote
            if self.content_type.model == 'question':
                author.add_reputation(5 * multiplier)  # +5 for question upvote
            elif self.content_type.model == 'answer':
                author.add_reputation(10 * multiplier)  # +10 for answer upvote
        elif self.value == -1:  # Downvote
            if self.content_type.model == 'question':
                author.remove_reputation(2 * multiplier)  # -2 for question downvote
            elif self.content_type.model == 'answer':
                author.remove_reputation(2 * multiplier)  # -2 for answer downvote
