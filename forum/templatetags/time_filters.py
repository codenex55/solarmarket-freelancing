from django import template
from django.utils.timezone import now
from datetime import timedelta

register = template.Library()

@register.filter
def humanize_timedelta(value):
    if not value:
        return ""
    
    delta = now() - value

    days = delta.days
    seconds = delta.seconds

    if days > 0:
        hours = seconds // 3600
        return f"{days} day{'s' if days != 1 else ''} and {hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds >= 3600:
        hours = seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds >= 60:
        minutes = seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    else:
        return "now"
