import json
from django import template

register = template.Library()


@register.filter
def show_meta_value(data, value):
    v = json.loads(data.value)
    return v['%s' % value]


@register.filter
def get_value(widget, data, value):
    if widget == 'wordmetahideinput':
        v = json.loads(data)
        return v['%s' % value]


@register.inclusion_tag("admin/post/images.html")
def images_gallery(data):
    if data != '':
        images = data.split(',')
        return {
            'data': images
        }
