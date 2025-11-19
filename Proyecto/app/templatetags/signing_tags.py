from django import template
from django.core import signing

register = template.Library()

@register.filter
def sign(value):
    return signing.dumps(value)
