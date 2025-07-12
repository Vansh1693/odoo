from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Basic user serializer.
    """
    display_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'display_name', 'avatar', 
            'reputation', 'date_joined'
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Detailed user serializer.
    """
    display_name = serializers.ReadOnlyField()
    total_questions = serializers.SerializerMethodField()
    total_answers = serializers.SerializerMethodField()
    accepted_answers = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'display_name',
            'email', 'bio', 'location', 'website', 'avatar', 'reputation',
            'github_username', 'twitter_username', 'linkedin_url',
            'total_questions', 'total_answers', 'accepted_answers',
            'date_joined'
        ]

    def get_total_questions(self, obj):
        return obj.question_set.count()

    def get_total_answers(self, obj):
        return obj.answer_set.count()

    def get_accepted_answers(self, obj):
        return obj.answer_set.filter(is_accepted=True).count()
