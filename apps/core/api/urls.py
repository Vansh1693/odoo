from django.urls import path, include

urlpatterns = [
    path('users/', include('apps.users.api.urls')),
    path('questions/', include('apps.questions.api.urls')),
    path('answers/', include('apps.answers.api.urls')),
    path('votes/', include('apps.votes.api.urls')),
    path('notifications/', include('apps.notifications.api.urls')),
]
