from django import template
from pages.models import UnreadMessage

register = template.Library()


@register.simple_tag
def countUnread(otheruser, requestUser):
    numberOfMessages = UnreadMessage.objects.filter(sender2=otheruser, recipient2=requestUser).count()
    if numberOfMessages == 0:
        return False
    else:
        return numberOfMessages
    