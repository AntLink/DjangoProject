import json
from django import template

register = template.Library()


@register.filter
def show_setting_value(data, value):
    v = json.loads(data)
    return v['%s' % value]


@register.filter
def show_title(data):
    title = json.loads(data)
    return title['show_title']


