from rest_framework import serializers
from ..models import Answer
from apps.users.api.serializers import UserSerializer


class AnswerSerializer(serializers.ModelSerializer):
    """
    Answer serializer.
    """
    created_by = UserSerializer(read_only=True)
    question_title = serializers.CharField(source='question.title', read_only=True)
    
    class Meta:
        model = Answer
        fields = [
            'id', 'question', 'question_title', 'content', 'created_by',
            'is_accepted', 'vote_score', 'created_at', 'updated_at'
        ]
        read_only_fields = ['is_accepted', 'vote_score']
