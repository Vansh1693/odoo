from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'sender', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('recipient__username', 'sender__username', 'title', 'message')
    readonly_fields = ('created_at', 'updated_at', 'read_at')
    
    fieldsets = (
        (None, {
            'fields': ('recipient', 'sender', 'notification_type', 'title', 'message')
        }),
        ('Related Object', {
            'fields': ('related_object_id', 'related_object_type'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_read', 'read_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        for notification in queryset:
            notification.mark_as_read()
        self.message_user(request, f"Successfully marked {queryset.count()} notifications as read.")
    mark_as_read.short_description = "Mark selected notifications as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False, read_at=None)
        self.message_user(request, f"Successfully marked {queryset.count()} notifications as unread.")
    mark_as_unread.short_description = "Mark selected notifications as unread"
