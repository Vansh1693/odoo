from django.http import JsonResponse
from django.views import View
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Vote
from django.db import models


@method_decorator(csrf_exempt, name='dispatch')
class VoteView(View):
    def post(self, request):
        content_type = request.POST.get('content_type')
        object_id = request.POST.get('object_id')
        value = request.POST.get('value')

        try:
            value = int(value)
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid vote value'}, status=400)

        try:
            model = ContentType.objects.get(model=content_type).model_class()
            obj = model.objects.get(pk=object_id)
        except Exception as e:
            return JsonResponse({'error': f'Invalid content: {e}'}, status=400)

        if not request.user.is_authenticated:
            return JsonResponse({'error': 'You must be logged in to vote'}, status=403)

        if obj.created_by == request.user:
            return JsonResponse({'error': 'You cannot vote on your own content'}, status=400)

        vote, created = Vote.objects.get_or_create(
            user=request.user,
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id,
            defaults={'value': value}
        )

        if not created:
            if vote.value == value:
                vote.delete()
            else:
                vote.value = value
                vote.save()

        # Calculate new vote score
        vote_score = Vote.objects.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id
        ).aggregate(score_sum=models.Sum('value'))['score_sum'] or 0

        return JsonResponse({'success': True, 'new_score': vote_score})
