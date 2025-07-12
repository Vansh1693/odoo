from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from .models import Vote
from apps.questions.models import Question
from apps.answers.models import Answer


class VoteView(LoginRequiredMixin, View):
    """
    Handle voting on questions and answers via AJAX.
    """
    def post(self, request):
        content_type_name = request.POST.get('content_type')
        object_id = request.POST.get('object_id')
        vote_value = int(request.POST.get('value'))  # 1 for upvote, -1 for downvote
        
        if content_type_name not in ['question', 'answer']:
            return JsonResponse({'error': 'Invalid content type'}, status=400)
        
        if vote_value not in [1, -1]:
            return JsonResponse({'error': 'Invalid vote value'}, status=400)
        
        # Check if user has enough reputation to vote
        if not request.user.can_vote():
            return JsonResponse({
                'error': 'You need at least 15 reputation to vote'
            }, status=403)
        
        # Get the content object
        if content_type_name == 'question':
            content_object = get_object_or_404(Question, pk=object_id)
        else:
            content_object = get_object_or_404(Answer, pk=object_id)
        
        # Prevent voting on own content
        if content_object.created_by == request.user:
            return JsonResponse({'error': 'You cannot vote on your own content'}, status=400)
        
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
                return JsonResponse({
                    'success': True,
                    'action': 'removed',
                    'new_score': content_object.vote_score
                })
            else:
                # Change vote
                existing_vote.value = vote_value
                existing_vote.save()
                return JsonResponse({
                    'success': True,
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
            return JsonResponse({
                'success': True,
                'action': 'created',
                'new_score': content_object.vote_score
            })
