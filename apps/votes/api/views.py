from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from ..models import Vote
from apps.questions.models import Question
from apps.answers.models import Answer


class VoteAPIView(APIView):
    """
    API endpoint for voting on questions and answers.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        content_type_name = request.data.get('content_type')
        object_id = request.data.get('object_id')
        vote_value = request.data.get('value')
        
        if content_type_name not in ['question', 'answer']:
            return Response({'error': 'Invalid content type'}, status=status.HTTP_400_BAD_REQUEST)
        
        if vote_value not in [1, -1]:
            return Response({'error': 'Invalid vote value'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user has enough reputation to vote
        if not request.user.can_vote():
            return Response({
                'error': 'You need at least 15 reputation to vote'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Get the content object
        if content_type_name == 'question':
            content_object = get_object_or_404(Question, pk=object_id)
        else:
            content_object = get_object_or_404(Answer, pk=object_id)
        
        # Prevent voting on own content
        if content_object.created_by == request.user:
            return Response({
                'error': 'You cannot vote on your own content'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        content_type = ContentType.objects.get_for_model(content_object)
        
        # Check if user already voted
        existing_vote = Vote.objects.filter(
            user=request.user,
            content_type=content_type,
            object_id=object_id
        ).first()
        
        if existing_vote:
            if existing_vote.value == vote_value:
                # Remove vote if clicking same vote
                existing_vote.delete()
                return Response({
                    'action': 'removed',
                    'new_score': content_object.vote_score
                })
            else:
                # Change vote
                existing_vote.value = vote_value
                existing_vote.save()
                return Response({
                    'action': 'changed',
                    'new_score': content_object.vote_score
                })
        else:
            # Create new vote
            Vote.objects.create(
                user=request.user,
                content_type=content_type,
                object_id=object_id,
                value=vote_value
            )
            return Response({
                'action': 'created',
                'new_score': content_object.vote_score
            })
