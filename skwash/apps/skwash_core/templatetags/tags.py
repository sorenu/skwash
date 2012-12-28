from django import template
import re

register = template.Library()

@register.simple_tag
def active(request, pattern):
    if re.search(pattern, request.path):
        return 'active'
    return ''

@register.simple_tag
def insert_if_match(request, pattern, insert_text):
    if re.search(pattern, request.path):
        return insert_text
    return ''
    
@register.simple_tag    
def insert_if_no_match(request, pattern, insert_text):
    if not re.search(pattern, request.path):
        return insert_text
    return ''
    