from django import forms
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()


class UserProfileForm(forms.ModelForm):
    """
    Form for editing user profile.
    """
    # User fields
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField()
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    location = forms.CharField(max_length=100, required=False)
    website = forms.URLField(required=False)
    github_username = forms.CharField(max_length=100, required=False)
    twitter_username = forms.CharField(max_length=100, required=False)
    linkedin_url = forms.URLField(required=False)
    
    # Profile fields
    skills = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        help_text="Comma-separated list of skills",
        required=False
    )
    experience_level = forms.ChoiceField(
        choices=UserProfile._meta.get_field('experience_level').choices,
        required=False
    )
    preferred_languages = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        help_text="Comma-separated programming languages",
        required=False
    )
    
    # Notification preferences
    email_notifications = forms.BooleanField(required=False)
    email_on_answer = forms.BooleanField(required=False)
    email_on_comment = forms.BooleanField(required=False)
    email_on_mention = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'bio', 'location', 
            'website', 'avatar', 'github_username', 'twitter_username', 
            'linkedin_url'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'profile'):
            profile = self.instance.profile
            self.fields['skills'].initial = profile.skills
            self.fields['experience_level'].initial = profile.experience_level
            self.fields['preferred_languages'].initial = profile.preferred_languages
            self.fields['email_notifications'].initial = profile.email_notifications
            self.fields['email_on_answer'].initial = profile.email_on_answer
            self.fields['email_on_comment'].initial = profile.email_on_comment
            self.fields['email_on_mention'].initial = profile.email_on_mention

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit and hasattr(user, 'profile'):
            profile = user.profile
            profile.skills = self.cleaned_data.get('skills', '')
            profile.experience_level = self.cleaned_data.get('experience_level', 'beginner')
            profile.preferred_languages = self.cleaned_data.get('preferred_languages', '')
            profile.email_notifications = self.cleaned_data.get('email_notifications', True)
            profile.email_on_answer = self.cleaned_data.get('email_on_answer', True)
            profile.email_on_comment = self.cleaned_data.get('email_on_comment', True)
            profile.email_on_mention = self.cleaned_data.get('email_on_mention', True)
            profile.save()
        return user
