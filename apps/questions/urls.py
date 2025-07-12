from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='list'),
    path('ask/', views.QuestionCreateView.as_view(), name='ask'),
    path('<int:pk>/', views.QuestionDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.QuestionUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='delete'),
    path('tag/<str:tag>/', views.QuestionsByTagView.as_view(), name='by_tag'),
]
