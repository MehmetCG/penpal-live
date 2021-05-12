from django.contrib import admin
from .models import UserProfile, Message, LatestSearch, LatestMessage, UnreadMessage
# Register your models here.

class MessageAdmin(admin.ModelAdmin):
    list_display = ( "sender", "recipient", "messageText", "created")
    list_filter = ("sender", "recipient", "created")



admin.site.register(UserProfile)
admin.site.register(Message, MessageAdmin)
admin.site.register(LatestSearch)
admin.site.register(LatestMessage)
admin.site.register(UnreadMessage)