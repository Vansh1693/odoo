from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Answer
from .forms import AnswerForm
from apps.questions.models import Question


class AnswerCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new answer for a question.
    """
    model = Answer
    form_class = AnswerForm
    template_name = 'answers/create.html'

    def dispatch(self, request, *args, **kwargs):
        self.question = get_object_or_404(Question, pk=kwargs['question_pk'])
        if self.question.is_closed:
            messages.error(request, "This question is closed and cannot accept new answers.")
            return redirect('questions:detail', pk=self.question.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.question = self.question
        form.instance.created_by = self.request.user
        messages.success(self.request, "Answer posted successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return self.question.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = self.question
        context['page_title'] = f'Answer: {self.question.title}'
        return context


class AnswerUpdateView(LoginRequiredMixin, UpdateView):
    """
    Edit an existing answer.
    """
    model = Answer
    form_class = AnswerForm
    template_name = 'answers/edit.html'

    def dispatch(self, request, *args, **kwargs):
        answer = self.get_object()
        if request.user != answer.created_by and not request.user.is_staff:
            messages.error(request, "You can only edit your own answers.")
            return redirect('questions:detail', pk=answer.question.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Answer updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.question.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = self.object.question
        context['page_title'] = 'Edit Answer'
        return context


class AnswerDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete an answer.
    """
    model = Answer
    template_name = 'answers/delete.html'

    def dispatch(self, request, *args, **kwargs):
        answer = self.get_object()
        if request.user != answer.created_by and not request.user.is_staff:
            messages.error(request, "You can only delete your own answers.")
            return redirect('questions:detail', pk=answer.question.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.object.question.get_absolute_url()

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Answer deleted successfully!")
        return super().delete(request, *args, **kwargs)


class AcceptAnswerView(LoginRequiredMixin, View):
    """
    Accept an answer (AJAX view).
    """
    def post(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        
        # Only question owner can accept answers
        if request.user != answer.question.created_by:
            return JsonResponse({'error': 'Only question owner can accept answers'}, status=403)
        
        # Cannot accept own answer
        if request.user == answer.created_by:
            return JsonResponse({'error': 'You cannot accept your own answer'}, status=400)
        
        answer.accept()
        
        return JsonResponse({
            'success': True,
            'message': 'Answer accepted successfully!'
        })


class UnacceptAnswerView(LoginRequiredMixin, View):
    """
    Unaccept an answer (AJAX view).
    """
    def post(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        
        # Only question owner can unaccept answers
        if request.user != answer.question.created_by:
            return JsonResponse({'error': 'Only question owner can unaccept answers'}, status=403)
        
        answer.unaccept()
        
        return JsonResponse({
            'success': True,
            'message': 'Answer unaccepted successfully!'
        })
