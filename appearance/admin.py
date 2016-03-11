from django.contrib import admin
import json
from django.http import HttpResponse
from suit.admin import Admin
from functools import update_wrapper
from .models import Menu, Widget
from django.utils.translation import ugettext_lazy as _
from .form import MenuForm, WidgetForm, TextForm, HtmlForm, TagForm, CategoryForm, RecentPostForm, LinksForm
from django.http import Http404
from django.shortcuts import redirect
from page.models import Page
from django.utils.html import strip_tags
from django.utils.datastructures import MultiValueDictKeyError
from django.template.response import TemplateResponse
from word.models import Taxonomy


class MenuAdmin(Admin):
    form = MenuForm
    fieldsets = [
        (None, {'fields': ('name', 'menu_type')}),
    ]

    change_form_template = 'admin/menu/menu.html'

    def get_urls(self):
        from django.conf.urls import url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        urlpatterns = [
            url(r'^$', wrap(self.changelist_view), name='%s_%s_changelist' % info),
            url(r'^add/$', wrap(self.add_view), name='%s_%s_add' % info),
            url(r'^add-custom-link-to-menu/$', wrap(self.add_custom_link_to_menu_view), name='%s_%s_add_custom_link_to_menu' % info),
            url(r'^add-cat-to-menu/$', wrap(self.add_cat_to_menu_view), name='%s_%s_add_cat_to_menu' % info),
            url(r'^add-page-to-menu/$', wrap(self.add_page_to_menu_view), name='%s_%s_add_page_to_menu' % info),
            url(r'^update-menu-structure/$', wrap(self.update_menu_structure_view), name='%s_%s_update_menu_structure' % info),
            url(r'^update-cat-in-menu/$', wrap(self.update_cat_in_menu_view), name='%s_%s_update_cat_in_menu' % info),
            url(r'^update-custom-link-in-menu/$', wrap(self.update_custom_link_in_menu_view), name='%s_%s_update_custom_link_in_menu' % info),
            url(r'^update-page-in-menu/$', wrap(self.update_page_in_menu_view), name='%s_%s_update_page_in_menu' % info),
            url(r'^delete-menu-structure/$', wrap(self.delete_menu_structure), name='%s_%s_delete_menu_structure' % info),
            url(r'^select/$', wrap(self.select_view), name='%s_%s_select' % info),
            url(r'^(.+)/history/$', wrap(self.history_view), name='%s_%s_history' % info),
            url(r'^(.+)/delete/$', wrap(self.delete_view), name='%s_%s_delete' % info),
            url(r'^(.+)/$', wrap(self.change_view), name='%s_%s_change' % info),
        ]
        return urlpatterns

    def select_view(self, request):
        if request.method == 'POST':
            id = request.POST['menu']
            if id != 'None':
                return redirect('admin:appearance_menu_change', id)
            else:
                return redirect('admin:appearance_menu_add')
        else:
            raise Http404(_('Page not found'))

    def update_menu_structure(self, data, parent):
        i = 0
        for v in data:
            i += 1
            model = Menu.objects.get(pk=v['id'])
            model.position = i
            model.parent_id = parent
            model.save()
            if 'children' in v:
                self.update_menu_structure(v['children'], v['id'])

    def update_menu_structure_view(self, request):
        if request.is_ajax():
            data = json.loads(request.POST['data'])
            parent = request.POST['parent']
            self.update_menu_structure(data, parent)
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            raise Http404(_('Page not found'))

    def add_cat_to_menu_view(self, request):
        if request.method == 'POST':
            try:
                parent = request.POST['parent']
            except MultiValueDictKeyError:
                return redirect('admin:appearance_menu_add')
            else:
                i = 0
                for id in request.POST.getlist('categories'):
                    i += 1
                    model = Menu()
                    menu = Menu.objects.get(pk=id)
                    model.name = menu.name
                    model.slug = menu.slug
                    model.description = menu.description
                    model.position = i
                    model.parent_id = int(parent)
                    model.root = int(request.POST['parent'])
                    model.type = 'menu_page'
                    model.menu_type = 'Category'
                    model.save()
                return redirect('admin:appearance_menu_change', parent)
        else:
            raise Http404(_('Page not found'))

    def update_cat_in_menu_view(self, request):
        if request.is_ajax():
            menu = Menu.objects.get(pk=request.POST['catid'])
            menu.name = request.POST['text']
            menu.type = request.POST['menutype']
            menu.save()
            return HttpResponse(json.dumps({'status': True}), content_type='application/json')
        else:
            raise Http404(_('Page not found'))

    def add_custom_link_to_menu_view(self, request):
        if request.method == 'POST':
            try:
                parent = request.POST['parent']
            except MultiValueDictKeyError:
                return redirect('admin:appearance_menu_add')
            else:
                model = Menu()
                model.name = request.POST['name']
                model.slug = request.POST['url']
                model.parent_id = int(parent)
                model.root = int(request.POST['parent'])
                model.menu_type = 'Custom link'
                model.type = 'menu_page'
                model.save()
                return redirect('admin:appearance_menu_change', parent)
        else:
            raise Http404(_('Page not found'))

    def update_custom_link_in_menu_view(self, request):
        if request.is_ajax():
            menu = Menu.objects.get(pk=request.POST['customid'])
            menu.name = request.POST['text']
            menu.slug = request.POST['url']
            menu.save()
            return HttpResponse(json.dumps({'status': True}), content_type='application/json')
        else:
            raise Http404(_('Page not found'))

    def add_page_to_menu_view(self, request):
        if request.method == 'POST':
            try:
                parent = request.POST['parent']
            except MultiValueDictKeyError:
                return redirect('admin:appearance_menu_add')
            else:
                i = 0
                for id in request.POST.getlist('pages'):
                    i += 1
                    model = Menu()
                    page = Page.objects.get(pk=id)
                    model.name = page.title
                    model.slug = page.slug
                    model.description = strip_tags(page.content)
                    model.position = i
                    model.parent_id = int(parent)
                    model.root = int(parent)
                    model.type = 'menu_page'
                    model.menu_type = 'Page'
                    model.save()
                    page.relationships.add(model.id)
                return redirect('admin:appearance_menu_change', parent)
        else:
            raise Http404(_('Page not found'))

    def update_page_in_menu_view(self, request):
        if request.is_ajax():
            menu = Menu.objects.get(pk=request.POST['pageid'])
            menu.name = request.POST['text']
            menu.save()
            return HttpResponse(json.dumps({'status': True}), content_type='application/json')
        else:
            raise Http404(_('Page not found'))

    def changelist_view(self, request, form_url='', extra_context=None):
        extra_context = {
            'id': 0,
            'title': _('Select %s to change' % self.opts.verbose_name),
            'menu_parent': Menu.objects.filter(type='menu_parent'),
            'category': Menu.objects.filter(type='category'),
            'page': Page.objects.filter(type='page'),
            'change_list': True
        }
        return self.changeform_view(request, None, form_url, extra_context)

    def delete_menu_structure(self, request):
        if request.is_ajax():
            menu = Menu.objects.get(pk=request.POST['id'])
            name = menu.name
            menu.delete()
            return HttpResponse(json.dumps({
                'status': True,
                'name': name
            }), content_type='application/json')
        else:
            raise Http404(_('Page not found'))

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = {
            'id': 0,
            'menu_parent': Menu.objects.filter(type='menu_parent'),
            'category': Menu.objects.filter(type='category'),
            'page': Page.objects.filter(type='page'),
        }
        return self.changeform_view(request, None, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = {
            'id': int(object_id),
            'menu_parent': Menu.objects.filter(type='menu_parent'),
            'page': Page.objects.filter(type='page'),
            'menu': Menu.objects.filter(root=object_id, parent_id=object_id).order_by('position'),
            'category': Menu.objects.filter(type='category'),
        }

        return self.changeform_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        return self.model.objects.filter(type='menu_parent')


class WidgetAdmin(Admin):
    form = WidgetForm
    change_form_template = 'admin/widget/widget.html'
    fieldsets = [
        (None, {'fields': ('name', 'custom_name', 'content', 'type')}),
    ]

    def get_urls(self):
        from django.conf.urls import url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        urlpatterns = [
            url(r'^$', wrap(self.changelist_view), name='%s_%s_changelist' % info),
            url(r'^add-text/$', wrap(self.add_text_view), name='%s_%s_add_text' % info),
            url(r'^add-html/$', wrap(self.add_html_view), name='%s_%s_add_html' % info),
            url(r'^add-tag/$', wrap(self.add_tag_view), name='%s_%s_add_tag' % info),
            url(r'^add-category/$', wrap(self.add_category_view), name='%s_%s_add_category' % info),
            url(r'^add-recent-post/$', wrap(self.add_recent_post_view), name='%s_%s_add_recent_post' % info),
            url(r'^update-sidebar-position/$', wrap(self.update_sidebar_position_view), name='%s_%s_update_sidebar_position' % info),
            url(r'^update-footer1-position/$', wrap(self.update_footer1_position_view), name='%s_%s_update_footer1_position' % info),
            url(r'^update-footer2-position/$', wrap(self.update_footer2_position_view), name='%s_%s_update_footer2_position' % info),
            url(r'^update-footer3-position/$', wrap(self.update_footer3_position_view), name='%s_%s_update_footer3_position' % info),
            url(r'^update-footer4-position/$', wrap(self.update_footer4_position_view), name='%s_%s_update_footer4_position' % info),
            url(r'^update-home-content-position/$', wrap(self.update_home_content_position_view), name='%s_%s_update_home_content_position' % info),
            url(r'^update-contact-sidebar-position/$', wrap(self.update_contact_sidebar_position_view), name='%s_%s_update_contact_sidebar_position' % info),
            url(r'^update-text/$', wrap(self.update_text_widget_view), name='%s_%s_update_text_widget' % info),
            url(r'^update-html/$', wrap(self.update_html_widget_view), name='%s_%s_update_html_widget' % info),
            url(r'^update-tag/$', wrap(self.update_tag_widget_view), name='%s_%s_update_tag_widget' % info),
            url(r'^update-category/$', wrap(self.update_cat_widget_view), name='%s_%s_update_category_widget' % info),
            url(r'^update-recent-post/$', wrap(self.update_post_widget_view), name='%s_%s_update_post_widget' % info),
            url(r'^delete-widget/$', wrap(self.delete_widget_view), name='%s_%s_delete_widget' % info),
            url(r'^(.+)/history/$', wrap(self.history_view), name='%s_%s_history' % info),
            url(r'^(.+)/delete/$', wrap(self.delete_view), name='%s_%s_delete' % info),
            # url(r'^(.+)/$', wrap(self.change_view), name='%s_%s_change' % info),
        ]
        return urlpatterns

    def changelist_view(self, request):
        opts = self.model._meta
        htmlform = HtmlForm()
        context = {
            'title': _('Select %s to change' % self.opts.verbose_name),
            'change_list': True,
            'widget_sidebar': Widget.objects.filter(type='sidebar').order_by('position'),
            'widget_footer1': Widget.objects.filter(type='footer1').order_by('position'),
            'widget_footer2': Widget.objects.filter(type='footer2').order_by('position'),
            'widget_footer3': Widget.objects.filter(type='footer3').order_by('position'),
            'widget_footer4': Widget.objects.filter(type='footer4').order_by('position'),
            'home_content': Widget.objects.filter(type='home_content').order_by('position'),
            'contact_sidebar': Widget.objects.filter(type='contact_sidebar').order_by('position'),
            'textform': TextForm(),
            'htmlform': HtmlForm(),
            'tagform': TagForm(),
            'app_label': opts.app_label,
            'opts': opts,
            'category': Taxonomy.objects.filter(type='category'),
            'media': htmlform.media,
            'catform': CategoryForm(),
            'postform': RecentPostForm(),
            'linkform': LinksForm(),
        }
        return TemplateResponse(request, self.change_form_template, context)

    def add_text_view(self, request):
        opts = self.model._meta
        htmlform = HtmlForm()
        if request.method == 'POST':
            form = TextForm(request.POST)
            if form.is_valid():
                data = {
                    'show_title': request.POST.get('show_title', 'no'),
                    'title': request.POST.get('title', 'None'),
                    'position': request.POST.get('position', 'sidebar'),
                    'display': 'html',
                }
                model = Widget()
                model.name = 'Text'
                model.custom_name = request.POST['title']
                model.content = request.POST['content']
                model.type = request.POST['position']
                model.setting = json.dumps(data)
                model.save()
                return redirect('admin:appearance_widget_changelist')
        else:
            form = TextForm()
        context = {
            'title': _('Select %s to change' % self.opts.verbose_name),
            'widget_sidebar': Widget.objects.filter(type='sidebar').order_by('position'),
            'widget_footer1': Widget.objects.filter(type='footer1').order_by('position'),
            'widget_footer2': Widget.objects.filter(type='footer2').order_by('position'),
            'widget_footer3': Widget.objects.filter(type='footer3').order_by('position'),
            'widget_footer4': Widget.objects.filter(type='footer4').order_by('position'),
            'home_content': Widget.objects.filter(type='home_content').order_by('position'),
            'contact_sidebar': Widget.objects.filter(type='contact_sidebar').order_by('position'),
            'app_label': opts.app_label,
            'opts': opts,
            'htmlform': htmlform,
            'tagform': TagForm(),
            'textform': form,
            'category': Taxonomy.objects.filter(type='category'),
            'catform': CategoryForm(),
            'media': htmlform.media,
            'postform': RecentPostForm(),
        }
        return TemplateResponse(request, self.change_form_template, context)

    def add_html_view(self, request):
        opts = self.model._meta
        if request.method == 'POST':
            form = HtmlForm(request.POST)
            if form.is_valid():
                data = {
                    'show_title': request.POST.get('show_title', 'no'),
                    'title': request.POST.get('title', 'None'),
                    'position': request.POST.get('position', 'sidebar'),
                    'display': 'html',
                }
                model = Widget()
                model.name = 'HTML'
                model.custom_name = request.POST['title']
                model.content = request.POST['content']
                model.type = request.POST['position']
                model.setting = json.dumps(data)
                model.save()
                return redirect('admin:appearance_widget_changelist')
        else:
            form = HtmlForm()
        context = {
            'title': _('Select %s to change' % self.opts.verbose_name),
            'widget_sidebar': Widget.objects.filter(type='sidebar').order_by('position'),
            'widget_footer1': Widget.objects.filter(type='footer1').order_by('position'),
            'widget_footer2': Widget.objects.filter(type='footer2').order_by('position'),
            'widget_footer3': Widget.objects.filter(type='footer3').order_by('position'),
            'widget_footer4': Widget.objects.filter(type='footer4').order_by('position'),
            'home_content': Widget.objects.filter(type='home_content').order_by('position'),
            'contact_sidebar': Widget.objects.filter(type='contact_sidebar').order_by('position'),
            'app_label': opts.app_label,
            'opts': opts,
            'textform': TextForm(),
            'tagform': TagForm(),
            'catform': CategoryForm(),
            'htmlform': form,
            'category': Taxonomy.objects.filter(type='category'),
            'media': form.media,
            'postform': RecentPostForm(),
        }
        return TemplateResponse(request, self.change_form_template, context)

    def add_tag_view(self, request):
        opts = self.model._meta
        htmlform = HtmlForm()
        if request.method == 'POST':
            form = TagForm(request.POST)
            if form.is_valid():
                data = {
                    'title': request.POST.get('title', 'None'),
                    'show_title': request.POST.get('show_title', 'no'),
                    'taxonomy': request.POST.get('taxonomy', ''),
                    'display': request.POST.get('display', ''),
                    'position': request.POST.get('position', 'sidebar'),
                    'limit': request.POST.get('limit', 0),
                    'description': request.POST.get('description', ''),
                }
                model = Widget()
                model.name = 'Tag'
                model.custom_name = request.POST['title']
                model.type = request.POST['position']
                model.setting = json.dumps(data)
                model.save()
                return redirect('admin:appearance_widget_changelist')
        else:
            form = TagForm()
        context = {
            'title': _('Select %s to change' % self.opts.verbose_name),
            'widget_sidebar': Widget.objects.filter(type='sidebar').order_by('position'),
            'widget_footer1': Widget.objects.filter(type='footer1').order_by('position'),
            'widget_footer2': Widget.objects.filter(type='footer2').order_by('position'),
            'widget_footer3': Widget.objects.filter(type='footer3').order_by('position'),
            'widget_footer4': Widget.objects.filter(type='footer4').order_by('position'),
            'home_content': Widget.objects.filter(type='home_content').order_by('position'),
            'contact_sidebar': Widget.objects.filter(type='contact_sidebar').order_by('position'),
            'app_label': opts.app_label,
            'opts': opts,
            'textform': TextForm(),
            'tagform': form,
            'htmlform': htmlform,
            'media': htmlform.media,
            'category': Taxonomy.objects.filter(type='category'),
            'catform': CategoryForm(),
            'postform': RecentPostForm(),
        }
        return TemplateResponse(request, self.change_form_template, context)

    def add_category_view(self, request):
        opts = self.model._meta
        htmlform = HtmlForm()
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                data = {
                    'title': request.POST.get('title', 'None'),
                    'show_title': request.POST.get('show_title', 'no'),
                    'display': request.POST.get('display', ''),
                    'position': request.POST.get('position', 'sidebar'),
                    'limit': request.POST.get('limit', 0),
                    'description': request.POST.get('description', ''),
                }
                model = Widget()
                model.name = 'Category'
                model.custom_name = request.POST['title']
                model.type = request.POST['position']
                model.setting = json.dumps(data)
                model.save()
                return redirect('admin:appearance_widget_changelist')
        else:
            form = CategoryForm()
        context = {
            'title': _('Select %s to change' % self.opts.verbose_name),
            'widget_sidebar': Widget.objects.filter(type='sidebar').order_by('position'),
            'widget_footer1': Widget.objects.filter(type='footer1').order_by('position'),
            'widget_footer2': Widget.objects.filter(type='footer2').order_by('position'),
            'widget_footer3': Widget.objects.filter(type='footer3').order_by('position'),
            'widget_footer4': Widget.objects.filter(type='footer4').order_by('position'),
            'home_content': Widget.objects.filter(type='home_content').order_by('position'),
            'contact_sidebar': Widget.objects.filter(type='contact_sidebar').order_by('position'),
            'app_label': opts.app_label,
            'opts': opts,
            'textform': TextForm(),
            'tagform': TagForm(),
            'catform': form,
            'htmlform': htmlform,
            'category': Taxonomy.objects.filter(type='category'),
            'media': htmlform.media,
            'postform': RecentPostForm(),
        }
        return TemplateResponse(request, self.change_form_template, context)

    def add_recent_post_view(self, request):
        opts = self.model._meta
        htmlform = HtmlForm()
        if request.method == 'POST':
            form = RecentPostForm(request.POST)
            if form.is_valid():
                data = {
                    'title': request.POST.get('title', 'None'),
                    'show_title': request.POST.get('show_title', 'no'),
                    'display': request.POST.get('display', ''),
                    'limit': request.POST.get('limit', 0),
                    'category': request.POST.get('category', 'all'),
                    'border_color': request.POST.get('border_color', 'all'),
                    'position': request.POST.get('position', 'sidebar'),
                    'description': request.POST.get('description', ''),
                }
                model = Widget()
                model.name = 'Recent Post'
                model.custom_name = request.POST['title']
                model.type = request.POST['position']
                model.setting = json.dumps(data)
                model.save()
                return redirect('admin:appearance_widget_changelist')
        else:
            form = RecentPostForm()
        context = {
            'title': _('Select %s to change' % self.opts.verbose_name),
            'widget_sidebar': Widget.objects.filter(type='sidebar').order_by('position'),
            'widget_footer1': Widget.objects.filter(type='footer1').order_by('position'),
            'widget_footer2': Widget.objects.filter(type='footer2').order_by('position'),
            'widget_footer3': Widget.objects.filter(type='footer3').order_by('position'),
            'widget_footer4': Widget.objects.filter(type='footer4').order_by('position'),
            'home_content': Widget.objects.filter(type='home_content').order_by('position'),
            'contact_sidebar': Widget.objects.filter(type='contact_sidebar').order_by('position'),
            'app_label': opts.app_label,
            'opts': opts,
            'textform': TextForm(),
            'tagform': TagForm(),
            'catform': CategoryForm(),
            'htmlform': htmlform,
            'postform': form,
            'category': Taxonomy.objects.filter(type='category'),
            'media': htmlform.media,
        }
        return TemplateResponse(request, self.change_form_template, context)

    def update_widget_position(self, data, type):
        i = 0
        for v in data:
            i += 1
            model = Widget.objects.get(pk=v['id'])
            model.position = i
            model.type = type
            model.save()
            if 'children' in v:
                self.update_widget_position(v['children'], type)

    def update_sidebar_position_view(self, request):
        if request.is_ajax():
            data = json.loads(request.POST['data'])
            self.update_widget_position(data, type='sidebar')
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            raise Http404(_('Page not found'))

    def update_footer1_position_view(self, request):
        if request.is_ajax():
            data = json.loads(request.POST['data'])
            self.update_widget_position(data, type='footer1')
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            raise Http404(_('Page not found'))

    def update_footer2_position_view(self, request):
        if request.is_ajax():
            data = json.loads(request.POST['data'])
            self.update_widget_position(data, type='footer2')
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            raise Http404(_('Page not found'))

    def update_footer3_position_view(self, request):
        if request.is_ajax():
            data = json.loads(request.POST['data'])
            self.update_widget_position(data, type='footer3')
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            raise Http404(_('Page not found'))

    def update_footer4_position_view(self, request):
        if request.is_ajax():
            data = json.loads(request.POST['data'])
            self.update_widget_position(data, type='footer4')
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            raise Http404(_('Page not found'))

    def update_home_content_position_view(self, request):
        if request.is_ajax():
            data = json.loads(request.POST['data'])
            self.update_widget_position(data, type='home_content')
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            raise Http404(_('Page not found'))

    def update_contact_sidebar_position_view(self, request):
        if request.is_ajax():
            data = json.loads(request.POST['data'])
            self.update_widget_position(data, type='contact_sidebar')
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            raise Http404(_('Page not found'))

    def update_text_widget_view(self, request):
        if request.is_ajax():
            model = Widget.objects.get(pk=request.POST['id'])
            data = {
                'show_title': request.POST.get('show_title', 'no'),
                'title': request.POST.get('title', 'no'),
                'display': 'html',
            }
            model.setting = json.dumps(data)
            model.custom_name = request.POST['title']
            model.content = request.POST['content']
            model.save()
            return HttpResponse(json.dumps({'status': True, 'data': request.POST}), content_type='application/json')
        else:
            raise Http404(_('Page not found'))

    def update_html_widget_view(self, request):
        if request.is_ajax():
            model = Widget.objects.get(pk=request.POST['id'])
            data = {
                'show_title': request.POST.get('show_title', 'no'),
                'title': request.POST.get('title', 'no'),
                'display': 'html',
            }
            model.setting = json.dumps(data)
            model.custom_name = request.POST['title']
            model.content = request.POST['content']
            model.save()
            return HttpResponse(json.dumps({'status': True, 'data': request.POST}), content_type='application/json')
        else:
            raise Http404(_('Page not found'))

    def update_tag_widget_view(self, request):
        if request.is_ajax():
            model = Widget.objects.get(pk=request.POST['id'])
            data = {
                'title': request.POST.get('title', 'None'),
                'show_title': request.POST.get('show_title', 'no'),
                'taxonomy': request.POST.get('taxonomy', ''),
                'display': request.POST.get('display', 'list'),
                'limit': request.POST.get('limit', 5),
                'description': request.POST.get('description', ''),
            }
            model.custom_name = request.POST['title']
            model.setting = json.dumps(data)
            model.save()
            return HttpResponse(json.dumps({'status': True, 'data': request.POST}), content_type='application/json')
        else:
            raise Http404(_('Page not found'))

    def update_cat_widget_view(self, request):
        if request.is_ajax():
            model = Widget.objects.get(pk=request.POST['id'])
            data = {
                'title': request.POST.get('title', 'None'),
                'show_title': request.POST.get('show_title', 'no'),
                'display': request.POST.get('display', 'list'),
                'limit': request.POST.get('limit', 5),
                'description': request.POST.get('description', ''),
            }
            model.custom_name = request.POST['title']
            model.setting = json.dumps(data)
            model.save()
            return HttpResponse(json.dumps({'status': True, 'data': request.POST}), content_type='application/json')
        else:
            raise Http404(_('Page not found'))

    def update_post_widget_view(self, request):
        if request.is_ajax():
            model = Widget.objects.get(pk=request.POST['id'])
            data = {
                'title': request.POST.get('title', 'None'),
                'show_title': request.POST.get('show_title', 'no'),
                'limit': request.POST.get('limit', 0),
                'display': request.POST.get('display', ''),
                'category': request.POST.get('category', 'all'),
                'border_color': request.POST.get('border_color', '#333'),
                'description': request.POST.get('description', ''),
            }
            model.custom_name = request.POST['title']
            model.setting = json.dumps(data)
            model.save()
            return HttpResponse(json.dumps({'status': True, 'data': request.POST}), content_type='application/json')
        else:
            raise Http404(_('Page not found'))

    def delete_widget_view(self, request):
        if request.is_ajax():
            model = Widget.objects.get(pk=request.POST['id'])
            name = model.custom_name
            model.delete()
            return HttpResponse(json.dumps({
                'status': True,
                'name': name
            }), content_type='application/json')
        else:
            raise Http404(_('Page not found'))


admin.site.register(Menu, MenuAdmin)
admin.site.register(Widget, WidgetAdmin)
