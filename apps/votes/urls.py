# apps/votes/urls.py
from django.urls import path
from .views import VoteView

app_name = "votes"

urlpatterns = [
    path('', VoteView.as_view(), name='vote'),
]
