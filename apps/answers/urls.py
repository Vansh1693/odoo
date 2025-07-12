from django.urls import path
from . import views

app_name = 'answers'

urlpatterns = [
    path('create/<int:question_pk>/', views.AnswerCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.AnswerUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.AnswerDeleteView.as_view(), name='delete'),
    path('<int:pk>/accept/', views.AcceptAnswerView.as_view(), name='accept'),
    path('<int:pk>/unaccept/', views.UnacceptAnswerView.as_view(), name='unaccept'),
]
