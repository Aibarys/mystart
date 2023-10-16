from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter(name='as_date_input')
def as_date_input(bound_field):
    if bound_field.field.widget.input_type == 'text':
        return format_html('<input type="date" name="{}" value="{}" id="id_{}">', 
                           bound_field.html_name, 
                           bound_field.value(), 
                           bound_field.html_name)
    return bound_field
