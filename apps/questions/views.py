from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.http import Http404
from taggit.models import Tag
from .models import Question, QuestionView
from .forms import QuestionForm
from apps.answers.models import Answer
from apps.answers.forms import AnswerForm


class QuestionListView(ListView):
    """
    List all questions with filtering and sorting options.
    """
    model = Question
    template_name = 'questions/list.html'
    context_object_name = 'questions'
    paginate_by = 20

    def get_queryset(self):
        queryset = Question.objects.select_related('created_by').prefetch_related(
            'tags'
        ).annotate(
            answer_count=Count('answers')
        )

        # Filter by status
        status = self.request.GET.get('status', 'all')
        if status == 'unanswered':
            queryset = queryset.filter(answer_count=0)
        elif status == 'answered':
            queryset = queryset.filter(answer_count__gt=0)
        elif status == 'accepted':
            queryset = queryset.filter(has_accepted_answer=True)

        # Sort options
        sort = self.request.GET.get('sort', 'newest')
        if sort == 'votes':
            queryset = queryset.order_by('-vote_score', '-created_at')
        elif sort == 'views':
            queryset = queryset.order_by('-views', '-created_at')
        elif sort == 'oldest':
            queryset = queryset.order_by('created_at')
        else:  # newest
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', 'all')
        context['current_sort'] = self.request.GET.get('sort', 'newest')
        context['page_title'] = 'All Questions'
        return context


class QuestionDetailView(DetailView):
    """
    Display question detail with answers.
    """
    model = Question
    template_name = 'questions/detail.html'
    context_object_name = 'question'

    def get_object(self):
        question = super().get_object()
        
        # Track view
        user = self.request.user if self.request.user.is_authenticated else None
        ip_address = self.get_client_ip()
        
        view, created = QuestionView.objects.get_or_create(
            question=question,
            user=user,
            ip_address=ip_address
        )
        
        if created:
            question.increment_views()
        
        return question

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        
        # Get answers ordered by votes and acceptance
        answers = Answer.objects.filter(question=question).select_related(
            'created_by'
        ).order_by('-is_accepted', '-vote_score', '-created_at')
        
        context['answers'] = answers
        context['answer_form'] = AnswerForm()
        context['can_edit'] = (
            self.request.user.is_authenticated and 
            (self.request.user == question.created_by or self.request.user.is_staff)
        )
        return context


class QuestionCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new question.
    """
    model = Question
    form_class = QuestionForm
    template_name = 'questions/ask.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Question posted successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Ask a Question'
        return context


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    """
    Edit an existing question.
    """
    model = Question
    form_class = QuestionForm
    template_name = 'questions/edit.html'

    def dispatch(self, request, *args, **kwargs):
        question = self.get_object()
        if request.user != question.created_by and not request.user.is_staff:
            messages.error(request, "You can only edit your own questions.")
            return redirect('questions:detail', pk=question.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Question updated successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Edit Question'
        return context


class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete a question.
    """
    model = Question
    template_name = 'questions/delete.html'
    success_url = reverse_lazy('questions:list')

    def dispatch(self, request, *args, **kwargs):
        question = self.get_object()
        if request.user != question.created_by and not request.user.is_staff:
            messages.error(request, "You can only delete your own questions.")
            return redirect('questions:detail', pk=question.pk)
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Question deleted successfully!")
        return super().delete(request, *args, **kwargs)


class QuestionsByTagView(ListView):
    """
    List questions filtered by tag.
    """
    model = Question
    template_name = 'questions/by_tag.html'
    context_object_name = 'questions'
    paginate_by = 20

    def get_queryset(self):
        tag_name = self.kwargs['tag']
        return Question.objects.filter(
            tags__name__iexact=tag_name
        ).select_related('created_by').prefetch_related('tags').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_name = self.kwargs['tag']
        try:
            tag = Tag.objects.get(name__iexact=tag_name)
            context['tag'] = tag
            context['page_title'] = f'Questions tagged "{tag.name}"'
        except Tag.DoesNotExist:
            raise Http404("Tag not found")
        return context
