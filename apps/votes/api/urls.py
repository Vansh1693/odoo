from django.urls import path
from .views import VoteAPIView

urlpatterns = [
    path('vote/', VoteAPIView.as_view(), name='vote'),
]
