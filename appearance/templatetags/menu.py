from django import template
from appearance.models import Menu

register = template.Library()


@register.inclusion_tag('admin/menu/tree_menu_list.html')
def getTreeMenu(data):
    return {
        'data': data
    }


@register.filter
def count_menu(id):
    return Menu.objects.filter(parent_id=id).count()


@register.filter
def load_menu_by_parent_id(id):
    return Menu.objects.filter(parent_id=id).order_by('position')

@register.filter
def space(level):
    return (level * 16)
