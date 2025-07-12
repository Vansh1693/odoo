from django.db import models
from django.contrib.auth import get_user_model
from ckeditor_uploader.fields import RichTextUploadingField
from apps.core.models import BaseModel
from apps.questions.models import Question

User = get_user_model()


class Answer(BaseModel):
    """
    Answer model for questions.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = RichTextUploadingField()
    is_accepted = models.BooleanField(default=False)
    
    # Denormalized fields for performance
    vote_score = models.IntegerField(default=0)

    class Meta:
        ordering = ['-is_accepted', '-vote_score', '-created_at']
        indexes = [
            models.Index(fields=['question', '-is_accepted', '-vote_score']),
            models.Index(fields=['created_by']),
        ]

    def __str__(self):
        return f"Answer to: {self.question.title}"

    def accept(self):
        """Mark this answer as accepted and unaccept others."""
        # Unaccept other answers for this question
        Answer.objects.filter(question=self.question).update(is_accepted=False)
        
        # Accept this answer
        self.is_accepted = True
        self.save(update_fields=['is_accepted'])
        
        # Update question's accepted answer status
        self.question.check_accepted_answer()
        
        # Award reputation to answer author
        if self.created_by:
            self.created_by.add_reputation(15)  # +15 for accepted answer

    def unaccept(self):
        """Unaccept this answer."""
        if self.is_accepted:
            self.is_accepted = False
            self.save(update_fields=['is_accepted'])
            
            # Update question's accepted answer status
            self.question.check_accepted_answer()
            
            # Remove reputation from answer author
            if self.created_by:
                self.created_by.remove_reputation(15)  # -15 for unaccepted answer

    def update_vote_score(self):
        """Update denormalized vote score."""
        from apps.votes.models import Vote
        votes = Vote.objects.filter(
            content_type__model='answer',
            object_id=self.pk
        )
        self.vote_score = sum(vote.value for vote in votes)
        self.save(update_fields=['vote_score'])
