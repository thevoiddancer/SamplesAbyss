from django import template
from urllib.parse import unquote #python3
register = template.Library()

@register.filter
def decode(value):
    return unquote(value)