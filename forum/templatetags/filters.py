# filters.py

from django import template
from django.utils.dateformat import format

register = template.Library()

@register.filter
def custom_date_format(date):
    return format(date, 'jS, F Y')
