from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    """
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    reputation = models.PositiveIntegerField(default=1)
    is_banned = models.BooleanField(default=False)
    ban_reason = models.TextField(blank=True)
    
    # Social links
    github_username = models.CharField(max_length=100, blank=True)
    twitter_username = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'username': self.username})

    @property
    def display_name(self):
        return self.get_full_name() or self.username

    def can_vote(self):
        """Check if user has enough reputation to vote."""
        from apps.core.models import SiteConfiguration
        config = SiteConfiguration.get_config()
        return self.reputation >= config.min_reputation_to_vote

    def add_reputation(self, points):
        """Add reputation points to user."""
        self.reputation += points
        self.save(update_fields=['reputation'])

    def remove_reputation(self, points):
        """Remove reputation points from user."""
        self.reputation = max(1, self.reputation - points)
        self.save(update_fields=['reputation'])


class UserProfile(models.Model):
    """
    Extended user profile information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    skills = models.TextField(help_text="Comma-separated list of skills", blank=True)
    experience_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('expert', 'Expert'),
        ],
        default='beginner'
    )
    preferred_languages = models.TextField(
        help_text="Comma-separated programming languages", 
        blank=True
    )
    
    # Notification preferences
    email_notifications = models.BooleanField(default=True)
    email_on_answer = models.BooleanField(default=True)
    email_on_comment = models.BooleanField(default=True)
    email_on_mention = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
