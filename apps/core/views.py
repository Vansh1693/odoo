from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q, Count
from django.contrib import messages
from apps.questions.models import Question


from django.db.models import Count

class HomeView(ListView):
    """
    Home page showing recent questions.
    """
    model = Question
    template_name = 'core/home.html'
    context_object_name = 'questions'
    paginate_by = 20

    def get_queryset(self):
        return Question.objects.select_related('created_by').prefetch_related(
            'tags', 'answers'
        ).annotate(
            total_answers=Count('answers')  # ✅ Changed name to avoid conflict
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Latest Questions'
        return context


class SearchView(ListView):
    """
    Search questions by title, content, or tags.
    """
    model = Question
    template_name = 'core/search.html'
    context_object_name = 'questions'
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        tag = self.request.GET.get('tag', '').strip()
        
        if not query and not tag:
            return Question.objects.none()

        queryset = Question.objects.select_related('created_by').prefetch_related(
            'tags', 'answers'
        ).annotate(answer_count=Count('answers'))

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query)
            )

        if tag:
            queryset = queryset.filter(tags__name__icontains=tag)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['tag'] = self.request.GET.get('tag', '')
        context['page_title'] = f"Search Results"
        return context
