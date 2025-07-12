from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from apps.core.models import BaseModel

User = get_user_model()


class Question(BaseModel):
    """
    Question model for the Q&A platform.
    """
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()
    tags = TaggableManager(blank=True)
    views = models.PositiveIntegerField(default=0)
    is_closed = models.BooleanField(default=False)
    close_reason = models.TextField(blank=True)
    
    # Denormalized fields for performance
    answer_count = models.PositiveIntegerField(default=0)
    vote_score = models.IntegerField(default=0)
    has_accepted_answer = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['-vote_score']),
            models.Index(fields=['created_by']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('questions:detail', kwargs={'pk': self.pk})

    def increment_views(self):
        """Increment view count."""
        self.views += 1
        self.save(update_fields=['views'])

    def update_answer_count(self):
        """Update denormalized answer count."""
        self.answer_count = self.answers.count()
        self.save(update_fields=['answer_count'])

    def update_vote_score(self):
        """Update denormalized vote score."""
        from apps.votes.models import Vote
        votes = Vote.objects.filter(
            content_type__model='question',
            object_id=self.pk
        )
        self.vote_score = sum(vote.value for vote in votes)
        self.save(update_fields=['vote_score'])

    def check_accepted_answer(self):
        """Check if question has an accepted answer."""
        self.has_accepted_answer = self.answers.filter(is_accepted=True).exists()
        self.save(update_fields=['has_accepted_answer'])

    @property
    def tag_list(self):
        """Get comma-separated list of tags."""
        return ', '.join([tag.name for tag in self.tags.all()])


class QuestionView(models.Model):
    """
    Track question views by users.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['question', 'user', 'ip_address']
        indexes = [
            models.Index(fields=['question', 'user']),
            models.Index(fields=['question', 'ip_address']),
        ]

    def __str__(self):
        return f"View of {self.question.title}"
