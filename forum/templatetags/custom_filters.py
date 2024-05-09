# templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def is_post(value):
    return value.__class__.__name__ == 'Post'

@register.filter
def is_question(value):
    return value.__class__.__name__ == 'Question'
