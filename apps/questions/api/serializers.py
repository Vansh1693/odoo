from rest_framework import serializers
from taggit.serializers import TagListSerializerField
from ..models import Question
from apps.users.api.serializers import UserSerializer


class QuestionSerializer(serializers.ModelSerializer):
    """
    Basic question serializer.
    """
    created_by = UserSerializer(read_only=True)
    tags = TagListSerializerField()
    
    class Meta:
        model = Question
        fields = [
            'id', 'title', 'content', 'tags', 'created_by',
            'views', 'answer_count', 'vote_score', 'has_accepted_answer',
            'is_closed', 'created_at', 'updated_at'
        ]
        read_only_fields = ['views', 'answer_count', 'vote_score', 'has_accepted_answer']


class QuestionDetailSerializer(QuestionSerializer):
    """
    Detailed question serializer with answers.
    """
    answers = serializers.SerializerMethodField()
    
    class Meta(QuestionSerializer.Meta):
        fields = QuestionSerializer.Meta.fields + ['answers']

    def get_answers(self, obj):
        from apps.answers.api.serializers import AnswerSerializer
        answers = obj.answers.select_related('created_by').order_by(
            '-is_accepted', '-vote_score', '-created_at'
        )
        return AnswerSerializer(answers, many=True).data
