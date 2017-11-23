from django import template

register = template.Library()

@register.filter(name='fixDuration')
def fix_duration(value):
    return value.split('M')[0] + ' Minutes'

