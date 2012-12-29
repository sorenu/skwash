from django.template import Library
import re
 
register = Library()

@register.filter
def placeholder(value, token):
    value.field.widget.attrs["placeholder"] = token
    return value