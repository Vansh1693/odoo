from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'reputation', 'is_banned', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_banned', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile Info', {
            'fields': ('bio', 'location', 'website', 'avatar', 'reputation')
        }),
        ('Social Links', {
            'fields': ('github_username', 'twitter_username', 'linkedin_url')
        }),
        ('Moderation', {
            'fields': ('is_banned', 'ban_reason')
        }),
    )

    actions = ['ban_users', 'unban_users']

    def ban_users(self, request, queryset):
        queryset.update(is_banned=True)
        self.message_user(request, f"Successfully banned {queryset.count()} users.")
    ban_users.short_description = "Ban selected users"

    def unban_users(self, request, queryset):
        queryset.update(is_banned=False, ban_reason='')
        self.message_user(request, f"Successfully unbanned {queryset.count()} users.")
    unban_users.short_description = "Unban selected users"
