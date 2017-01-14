from urllib.parse import quote_plus as qp
from django import template

register = template.Library()


@register.filter
def urlify(value):
    return qp(value)
