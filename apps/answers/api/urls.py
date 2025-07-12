from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnswerViewSet

router = DefaultRouter()
router.register(r'', AnswerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
