from django import template
from urllib.parse import unquote
register = template.Library()

@register.filter
def decode(value):
    return unquote(value)