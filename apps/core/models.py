from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseModel(models.Model):
    """
    Abstract base model with common fields for all models.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='%(class)s_created',
        null=True,
        blank=True
    )

    class Meta:
        abstract = True


class SiteConfiguration(models.Model):
    """
    Site-wide configuration settings.
    """
    site_name = models.CharField(max_length=100, default='StackIt')
    site_description = models.TextField(default='A Q&A platform for developers')
    allow_registration = models.BooleanField(default=True)
    maintenance_mode = models.BooleanField(default=False)
    max_tags_per_question = models.PositiveIntegerField(default=5)
    min_reputation_to_vote = models.PositiveIntegerField(default=15)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Configuration'
        verbose_name_plural = 'Site Configuration'

    def __str__(self):
        return self.site_name

    @classmethod
    def get_config(cls):
        """Get or create site configuration."""
        config, created = cls.objects.get_or_create(pk=1)
        return config
