from .models import *
from rest_framework import serializers
from datetime import timedelta


class MessageSerializer(serializers.ModelSerializer):
  
    sender = serializers.SerializerMethodField()
    def get_sender(self, obj):
        return obj.sender.username

    recipient = serializers.SerializerMethodField()
    def get_recipient(self, obj):
        return obj.recipient.username

    created = serializers.SerializerMethodField()
    def get_created(self, obj):
        return (obj.created + timedelta(hours=3)).strftime("%H:%M")

    image = serializers.SerializerMethodField()
    def get_image(self, obj):
        return obj.sender.userprofile.image.url

    messageID = serializers.SerializerMethodField()
    def get_messageID(self, obj):
        return obj.id

    class Meta:
            model = Message
            fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    
    user = serializers.SerializerMethodField()
    def get_user(self, obj):
        return obj.user.username

    last_seen = serializers.SerializerMethodField()
    def get_last_seen(self, obj):
        return (obj.last_seen + timedelta(hours=3)).strftime("%H:%M, %d %B %Y")
    
    class Meta:
            model = UserProfile
            fields = '__all__'
