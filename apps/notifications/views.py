from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from .models import Notification


class NotificationListView(LoginRequiredMixin, ListView):
    """
    Display user's notifications.
    """
    model = Notification
    template_name = 'notifications/list.html'
    context_object_name = 'notifications'
    paginate_by = 20

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        ).select_related('sender').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Notifications'
        context['unread_count'] = self.get_queryset().filter(is_read=False).count()
        return context


class MarkNotificationReadView(LoginRequiredMixin, View):
    """
    Mark a single notification as read and redirect to related object.
    """
    def get(self, request, pk):
        notification = get_object_or_404(
            Notification, 
            pk=pk, 
            recipient=request.user
        )
        
        notification.mark_as_read()
        
        # Redirect to related object or notifications list
        redirect_url = notification.get_related_url()
        if redirect_url != '#':
            return redirect(redirect_url)
        else:
            return redirect('notifications:list')


class MarkAllNotificationsReadView(LoginRequiredMixin, View):
    """
    Mark all notifications as read (AJAX view).
    """
    def post(self, request):
        notifications = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        )
        
        for notification in notifications:
            notification.mark_as_read()
        
        count = notifications.count()
        
        return JsonResponse({
            'success': True,
            'message': f'Marked {count} notifications as read'
        })
