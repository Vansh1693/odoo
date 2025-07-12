from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .models import UserProfile
from .forms import UserProfileForm

User = get_user_model()


class ProfileView(DetailView):
    """
    Display user profile with their questions and answers.
    """
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        
        context['recent_questions'] = user.question_set.select_related().order_by('-created_at')[:5]
        context['recent_answers'] = user.answer_set.select_related('question').order_by('-created_at')[:5]
        context['total_questions'] = user.question_set.count()
        context['total_answers'] = user.answer_set.count()
        context['accepted_answers'] = user.answer_set.filter(is_accepted=True).count()
        
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """
    Edit user profile.
    """
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user:
            messages.error(request, "You can only edit your own profile.")
            return redirect('users:profile', username=user.username)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'username': self.object.username})


class LeaderboardView(ListView):
    """
    Display users ranked by reputation.
    """
    model = User
    template_name = 'users/leaderboard.html'
    context_object_name = 'users'
    paginate_by = 50

    def get_queryset(self):
        return User.objects.filter(is_active=True, is_banned=False).order_by('-reputation')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Leaderboard'
        return context
