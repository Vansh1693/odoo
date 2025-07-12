from django.contrib import admin
from .models import Question, QuestionView


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'answer_count', 'vote_score', 'views', 'is_closed', 'created_at')
    list_filter = ('is_closed', 'has_accepted_answer', 'created_at', 'tags')
    search_fields = ('title', 'content', 'created_by__username')
    readonly_fields = ('views', 'answer_count', 'vote_score', 'has_accepted_answer', 'created_at', 'updated_at')
    filter_horizontal = ('tags',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'tags', 'created_by')
        }),
        ('Status', {
            'fields': ('is_closed', 'close_reason')
        }),
        ('Statistics', {
            'fields': ('views', 'answer_count', 'vote_score', 'has_accepted_answer'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['close_questions', 'open_questions']

    def close_questions(self, request, queryset):
        queryset.update(is_closed=True)
        self.message_user(request, f"Successfully closed {queryset.count()} questions.")
    close_questions.short_description = "Close selected questions"

    def open_questions(self, request, queryset):
        queryset.update(is_closed=False, close_reason='')
        self.message_user(request, f"Successfully opened {queryset.count()} questions.")
    open_questions.short_description = "Open selected questions"


@admin.register(QuestionView)
class QuestionViewAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'ip_address', 'viewed_at')
    list_filter = ('viewed_at',)
    search_fields = ('question__title', 'user__username', 'ip_address')
    readonly_fields = ('viewed_at',)
