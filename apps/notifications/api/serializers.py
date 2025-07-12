from rest_framework import serializers
from ..models import Notification
from apps.users.api.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    """
    Notification serializer.
    """
    sender = UserSerializer(read_only=True)
    related_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'title', 'message', 'sender',
            'related_object_id', 'related_object_type', 'related_url',
            'is_read', 'read_at', 'created_at'
        ]

    def get_related_url(self, obj):
        return obj.get_related_url()
