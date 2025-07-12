from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Answer
from apps.questions.models import Question
from .serializers import AnswerSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Answer model.
    """
    queryset = Answer.objects.select_related('created_by', 'question')
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def accept(self, request, pk=None):
        """Accept an answer."""
        answer = self.get_object()
        
        if request.user != answer.question.created_by:
            return Response(
                {'error': 'Only question owner can accept answers'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if request.user == answer.created_by:
            return Response(
                {'error': 'You cannot accept your own answer'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        answer.accept()
        
        return Response({'message': 'Answer accepted successfully!'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unaccept(self, request, pk=None):
        """Unaccept an answer."""
        answer = self.get_object()
        
        if request.user != answer.question.created_by:
            return Response(
                {'error': 'Only question owner can unaccept answers'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        answer.unaccept()
        
        return Response({'message': 'Answer unaccepted successfully!'})
