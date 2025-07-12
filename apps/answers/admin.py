from django.contrib import admin
from .models import Answer


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_by', 'is_accepted', 'vote_score', 'created_at')
    list_filter = ('is_accepted', 'created_at')
    search_fields = ('question__title', 'content', 'created_by__username')
    readonly_fields = ('vote_score', 'created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('question', 'content', 'created_by')
        }),
        ('Status', {
            'fields': ('is_accepted',)
        }),
        ('Statistics', {
            'fields': ('vote_score',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['accept_answers', 'unaccept_answers']

    def accept_answers(self, request, queryset):
        for answer in queryset:
            answer.accept()
        self.message_user(request, f"Successfully accepted {queryset.count()} answers.")
    accept_answers.short_description = "Accept selected answers"

    def unaccept_answers(self, request, queryset):
        for answer in queryset:
            answer.unaccept()
        self.message_user(request, f"Successfully unaccepted {queryset.count()} answers.")
    unaccept_answers.short_description = "Unaccept selected answers"
