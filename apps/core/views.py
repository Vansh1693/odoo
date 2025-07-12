from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q, Count
from django.contrib import messages
from apps.questions.models import Question


from django.db.models import Count

class HomeView(ListView):
    """
    Home page showing recent questions with optional sorting and filtering.
    """
    model = Question
    template_name = 'core/home.html'
    context_object_name = 'questions'
    paginate_by = 20

    def get_queryset(self):
        queryset = Question.objects.select_related('created_by').prefetch_related(
            'tags', 'answers'
        ).annotate(
            total_answers=Count('answers')
        )

        status = self.request.GET.get('status')
        sort = self.request.GET.get('sort')

        # ✅ Filter logic
        if status == 'unanswered':
            queryset = queryset.filter(total_answers=0)
        elif status == 'answered':
            queryset = queryset.filter(total_answers__gt=0)  # ✅ ADD THIS

        # ✅ Sort logic
        if sort == 'votes':
            queryset = queryset.order_by('-vote_score')
        elif sort == 'views':
            queryset = queryset.order_by('-views')
        elif sort == 'newest':
            queryset = queryset.order_by('-created_at')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Latest Questions'
        context['status'] = self.request.GET.get('status', '')
        context['sort'] = self.request.GET.get('sort', '')
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
