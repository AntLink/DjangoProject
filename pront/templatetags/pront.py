import re, json
from django import template
from appearance.models import Menu, Widget
from word.models import Word, Taxonomy
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


# start navbar tag
@register.inclusion_tag('layout/navbar.html')
def navbar(data=None, default_menu_parent=None):
    if data == None and default_menu_parent == None:
        try:
            Menu.objects.get(menu_type='navbar')
        except Menu.DoesNotExist:
            pass
        else:
            p = Menu.objects.get(menu_type='navbar')
            data = Menu.objects.filter(root=p.id, parent_id=p.id).order_by('position')
            default_menu_parent = p.id
            return {
                'data': data,
                'default': default_menu_parent,
                'leng': 0
            }
    else:
        return {
            'data': data,
            'default': default_menu_parent,
            'leng': 0
        }


@register.filter
def count_nav(id):
    return Menu.objects.filter(parent_id=id).count()


@register.filter
def load_nav_by_parent_id(id):
    return Menu.objects.filter(parent_id=id).order_by('position')


@register.filter
def load_post_by_nav_1(slug):
    from django.core.paginator import Paginator, EmptyPage, InvalidPage
    nav = Menu.objects.get(type='category', slug=slug)
    post = Word.objects.filter(relationships=nav.id).order_by('-created_at')
    paging = Paginator(post, 1)
    try:
        p = paging.page(1)
    except (EmptyPage, InvalidPage):
        p = []
    return p


@register.filter
def load_post_by_nav_2(slug):
    from django.core.paginator import Paginator, EmptyPage, InvalidPage
    nav = Menu.objects.get(type='category', slug=slug)
    post = Word.objects.filter(relationships=nav.id).order_by('-created_at')
    paging = Paginator(post, 3)
    try:
        p = paging.page(1)
    except (EmptyPage, InvalidPage):
        p = []
    return p


@register.filter
def load_post_by_nav_3(slug):
    from django.core.paginator import Paginator, EmptyPage, InvalidPage
    nav = Menu.objects.get(type='category', slug=slug)
    post = Word.objects.filter(relationships=nav.id).order_by('-created_at')
    paging = Paginator(post, 3)
    try:
        p = paging.page(2)
    except (EmptyPage, InvalidPage):
        p = []
    return p


@register.filter
def load_post_by_nav_4(slug):
    from django.core.paginator import Paginator, EmptyPage, InvalidPage
    nav = Menu.objects.get(type='category', slug=slug)
    post = Word.objects.filter(relationships=nav.id).order_by('-created_at')
    paging = Paginator(post, 3)
    try:
        p = paging.page(3)
    except (EmptyPage, InvalidPage):
        p = []
    return p


# end navbar tag

# start topbar tag
@register.inclusion_tag('layout/topbar_list.html')
def topbar(data=None, default_menu_parent=None):
    if data == None and default_menu_parent == None:
        try:
            Menu.objects.get(menu_type='topbar')
        except Menu.DoesNotExist:
            pass
        else:
            p = Menu.objects.get(menu_type='topbar')
            data = Menu.objects.filter(root=p.id, parent_id=p.id).order_by('position')
            default_menu_parent = p.id
            return {
                'data': data,
                'default': default_menu_parent
            }
    else:
        return {
            'data': data,
            'default': default_menu_parent
        }


@register.filter
def count_topbar(id):
    return Menu.objects.filter(parent_id=id).count()


@register.filter
def load_topbar_by_parent_id(id):
    return Menu.objects.filter(parent_id=id).order_by('position')


# end topbar tag

# start footer tag
@register.inclusion_tag('layout/footer_list.html')
def footer(data=None, default_menu_parent=None):
    if data == None and default_menu_parent == None:
        try:
            Menu.objects.get(menu_type='footer')
        except Menu.DoesNotExist:
            pass
        else:
            p = Menu.objects.get(menu_type='footer')
            data = Menu.objects.filter(root=p.id, parent_id=p.id).order_by('position')
            default_menu_parent = p.id
            return {
                'data': data,
                'default': default_menu_parent
            }
    else:
        return {
            'data': data,
            'default': default_menu_parent
        }


@register.filter
def count_footer(id):
    return Menu.objects.filter(parent_id=id).count()


@register.filter
def load_footer_by_parent_id(id):
    return Menu.objects.filter(parent_id=id).order_by('position')


# end footer tag


# start widget
@register.inclusion_tag('layout/widget/sidebar_list.html')
def widget_sidebar(data=None, default_menu_parent=None):
    data = Widget.objects.filter(type='sidebar').order_by('position')
    return {
        'widget': data
    }


@register.inclusion_tag('layout/widget/footer1_list.html')
def widget_footer1():
    widget = Widget.objects.filter(type='footer1').order_by('position')
    return {
        'widget': widget
    }


@register.inclusion_tag('layout/widget/footer2_list.html')
def widget_footer2(data=None, default_menu_parent=None):
    data = Widget.objects.filter(type='footer2').order_by('position')
    return {
        'widget': data
    }


@register.inclusion_tag('layout/widget/footer3_list.html')
def widget_footer3(data=None, default_menu_parent=None):
    data = Widget.objects.filter(type='footer3').order_by('position')
    return {
        'widget': data
    }


@register.inclusion_tag('layout/widget/footer4_list.html')
def widget_footer4(data=None, default_menu_parent=None):
    data = Widget.objects.filter(type='footer4').order_by('position')
    return {
        'widget': data
    }


@register.inclusion_tag('layout/widget/tag_widget.html')
def tag_widget(data, position=None):
    v = json.loads(data)
    type = v['taxonomy']
    tax = Taxonomy.objects.filter(type=type).order_by('?')[:v['limit']]
    return {
        'taxs': tax,
        'display': v['display'],
        'show_title': v['show_title'],
        'title': v['title'],
        'position': position
    }


@register.inclusion_tag('layout/widget/category_widget.html')
def category_widget(data, position=None):
    v = json.loads(data)
    if (v['display'] == 'tree'):
        tax = Taxonomy.objects.filter(type='category')[:v['limit']]
    else:
        tax = Taxonomy.objects.filter(type='category').order_by('?')[:v['limit']]

    return {
        'taxs': tax,
        'display': v['display'],
        'show_title': v['show_title'],
        'title': v['title'],
        'position': position
    }


@register.inclusion_tag('layout/widget/html_widget.html')
def html_widget(content, setting, position=None):
    v = json.loads(setting)
    return {
        'content': content,
        'show_title': v['show_title'],
        'title': v['title'],
        'position': position
    }


@register.inclusion_tag('layout/widget/text_widget.html')
def text_widget(content, setting, position=None):
    v = json.loads(setting)
    return {
        'content': content,
        'show_title': v['show_title'],
        'title': v['title'],
        'position': position
    }


@register.inclusion_tag('layout/widget/recent_post_widget.html')
def recent_post_widget(setting, position=None):
    v = json.loads(setting)
    if (v['category'] == 'all'):
        data = Word.objects.filter(type='post').order_by('?')[:v['limit']]
    else:
        tax = Taxonomy.objects.filter(slug=v['category'], type='category')[:1].get()
        data = Word.objects.filter(type='post', relationships=tax.id).order_by('?')[:v['limit']]
    return {
        'data': data,
        'show_title': v['show_title'],
        'title': v['title'],
        'category': v['category'],
        'position': position,
        'display': v['display'],
    }


@register.filter
def count_cat_tree(level):
    return (level * 16)


# end widget

# start Home
@register.inclusion_tag('layout/widget/home_content.html')
def home_content():
    data = Widget.objects.filter(type='home_content').order_by('position')
    return {
        'widget': data
    }


@register.inclusion_tag('pront/home_slider.html')
def home_slider():
    data = Word.objects.filter(type='post', status='p').order_by('?')[:6]
    return {
        'post': data
    }

@register.inclusion_tag('pront/home_slider2.html')
def home_slider2():
    data = Word.objects.filter(type='post', status='p').order_by('?')[:6]
    return {
        'post': data
    }


@register.filter
def post_data(category, limit):
    tax = Menu.objects.filter(slug=category, type='category')[:1].get()
    v = json.loads(limit)
    l = v['limit']
    return Word.objects.filter(relationships=tax.id).order_by('?')[:l]


# end Home

# start Contact
@register.inclusion_tag('layout/widget/contact_sidebar_list.html')
def widget_contact_sidebar(data=None, default_menu_parent=None):
    data = Widget.objects.filter(type='contact_sidebar').order_by('position')
    return {
        'widget': data
    }


# start Contact
@register.filter
def fine_url(url):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)
    return urls.__len__()


@register.filter
def get_range(value):
    """
      Filter - returns a list containing range made from given value
      Usage (in template):

      <ul>{% for i in 3|get_range %}
        <li>{{ i }}. Do something</li>
      {% endfor %}</ul>

      Results with the HTML:
      <ul>
        <li>0. Do something</li>
        <li>1. Do something</li>
        <li>2. Do something</li>
      </ul>

      Instead of 3 one may use the variable set in the views
    """
    r = int(value)
    return range(r)


@register.inclusion_tag("pront/images_gallery.html")
def images_gallery(data, title):
    if data != '':
        images = data.split(',')
        return {
            'data': images,
            'title': title,
        }
