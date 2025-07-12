from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from taggit.models import Tag
from ..models import Question
from .serializers import QuestionSerializer, QuestionDetailSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Question model.
    """
    queryset = Question.objects.select_related('created_by').prefetch_related('tags')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QuestionDetailSerializer
        return QuestionSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def popular_tags(self, request):
        """Get most popular tags."""
        tags = Tag.objects.annotate(
            question_count=Count('taggit_taggeditem_items')
        ).order_by('-question_count')[:20]
        
        tag_data = [{'name': tag.name, 'count': tag.question_count} for tag in tags]
        return Response(tag_data)

    @action(detail=False, methods=['get'])
    def unanswered(self, request):
        """Get unanswered questions."""
        questions = self.get_queryset().filter(answer_count=0)
        page = self.paginate_queryset(questions)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(questions, many=True)
        return Response(serializer.data)
