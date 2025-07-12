from django.contrib import admin
from .models import Vote


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'object_id', 'value', 'created_at')
    list_filter = ('value', 'content_type', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'content_type')
