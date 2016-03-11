from django.contrib import admin
from django.contrib.admin import helpers
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.core.exceptions import PermissionDenied
from functools import update_wrapper
from .models import Media
from .forms import ImageForm, ImageCategoryForm
from .views import UploadView
from word.models import Taxonomy
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.utils.translation import ungettext, ugettext_lazy as _
from django.contrib import messages
from suit.admin import Admin, create_modeladmin


class ImageCategoryAdmin(Admin):
    form = ImageCategoryForm
    # change_form_template = 'admin/album/change_form.html'
    # change_list_template = 'admin/album/change_list.html'
    list_display = ['name', 'images']

    def get_queryset(self, request):
        return self.model.objects.filter(type='image')

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
            url(r'^json-load/$', wrap(self.load_image_by_ajax_response), name='%s_%s_jsonload' % info),
            url(r'^upload/(?P<upload_to>.*)', UploadView.as_view(form_class=ImageForm), name='%s_%s_upload' % info),
            url(r'^(?P<tax>[0-9]+)/mode/(?P<mode>.*)$', wrap(self.image_list_view_by_tax_id),
                name='%s_%s_images' % info),
            url(r'^(.+)/history/$', wrap(self.history_view), name='%s_%s_history' % info),
            url(r'^(.+)/delete/$', wrap(self.delete_view), name='%s_%s_delete' % info),
            url(r'^(.+)/$', wrap(self.change_view), name='%s_%s_change' % info),
        ]
        return urlpatterns



class ImageAdmin(Admin):
    form = ImageForm
    # actions = None
    tax = None
    # change_form_template = 'admin/album/change_form.html'
    # change_grid_template = 'admin/image/change_list.html'
    change_list_template = 'admin/image/change_list.html'
    # list_display_links = ['albums']
    search_fields = ['name', 'description', 'relationships__name']
    # list_display = ['thumbnail','albums']
    list_display = ['images', 'tags', 'created_at']
    list_filter = ['created_at']
    fieldsets = [
        (None, {'fields': ('name', 'description', 'relationships')}),
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
            url(r'^mode/(?P<mode>.*)$', wrap(self.changelist_view), name='%s_%s_mode_changelist' % info),
            # url(r'^(?P<mode>.*)', wrap(self.changegrid_view), name='%s_%s_changegrid' % info),
            url(r'^add/$', wrap(self.add_view), name='%s_%s_add' % info),
            url(r'^test/$', wrap(self.load_image), name='%s_%s_test' % info),
            url(r'^json-load/$', wrap(self.load_image_by_ajax_response), name='%s_%s_jsonload' % info),
            url(r'^json-update/$', wrap(self.json_upadate), name='%s_%s_jsonupdate' % info),
            url(r'^upload/$', UploadView.as_view(form_class=ImageForm), name='%s_%s_upload' % info),
            url(r'^(?P<tax>[0-9]+)/mode/(?P<mode>.*)$', wrap(self.changelist_view), name='%s_%s_tags' % info),
            url(r'^(.+)/history/$', wrap(self.history_view), name='%s_%s_history' % info),
            url(r'^(.+)/delete/$', wrap(self.delete_view), name='%s_%s_delete' % info),
            url(r'^(.+)/$', wrap(self.change_view), name='%s_%s_change' % info),
        ]
        return urlpatterns

    def json_upadate(self, request):
        import json
        if request.is_ajax():
            img = Media.objects.get(pk=request.POST['id'])
            img.name = request.POST['name']
            img.description = request.POST['description']
            img.save()
            data = [
                {
                    'id': request.POST['id'],
                    'name': request.POST['name'],
                    'des': request.POST['description']
                }
            ]
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            raise Http404(_('Page not found'))

    def load_image(self, request, extra_context=None):
        from django.contrib.admin.views.main import ERROR_FLAG
        list_display = self.get_list_display(request)
        # list_display_links = self.get_list_display_links(request, list_display)
        list_display_links = None
        list_filter = self.get_list_filter(request)
        search_fields = self.get_search_fields(request)
        ChangeList = self.get_changelist(request)
        try:
            cl = ChangeList(request, self.model, list_display,
                            list_display_links, list_filter, self.date_hierarchy,
                            search_fields, self.list_select_related, self.list_per_page,
                            self.list_max_show_all, self.list_editable, self)

        except IncorrectLookupParameters:
            # Wacky lookup parameters were given, so redirect to the main
            # changelist page, without parameters, and pass an 'invalid=1'
            # parameter via the query string. If wacky parameters were given
            # and the 'invalid=1' parameter was already in the query string,
            # something is screwed up with the database, so display an error
            # page.
            if ERROR_FLAG in request.GET.keys():
                return SimpleTemplateResponse('admin/invalid_setup.html', {
                    'title': _('Database error'),
                })
            return HttpResponseRedirect(request.path + '?' + ERROR_FLAG + '=1')
        return HttpResponse(data)

    def changelist_view(self, request, extra_context=None, tax=None, mode=None):
        """
        The 'change list' admin view for this model.
        """
        from django.contrib.admin.views.main import ERROR_FLAG
        opts = self.model._meta
        self.tax = tax
        app_label = opts.app_label
        if not self.has_change_permission(request, None):
            raise PermissionDenied

        if mode == 'grid':
            self.list_display = ['thumbnail']
        else:
            self.list_display = ['images', 'tags', 'created_at']

        list_display = self.get_list_display(request)
        # list_display_links = self.get_list_display_links(request, list_display)
        list_display_links = None
        list_filter = self.get_list_filter(request)
        search_fields = self.get_search_fields(request)


        # Check actions to see if any are available on this changelist
        actions = self.get_actions(request)
        if actions and mode != 'grid':
            # Add the action checkboxes if there are any actions available.
            list_display = ['action_checkbox'] + list(list_display)

        ChangeList = self.get_changelist(request)
        try:
            cl = ChangeList(request, self.model, list_display,
                            list_display_links, list_filter, self.date_hierarchy,
                            search_fields, self.list_select_related, self.list_per_page,
                            self.list_max_show_all, self.list_editable, self)

        except IncorrectLookupParameters:
            # Wacky lookup parameters were given, so redirect to the main
            # changelist page, without parameters, and pass an 'invalid=1'
            # parameter via the query string. If wacky parameters were given
            # and the 'invalid=1' parameter was already in the query string,
            # something is screwed up with the database, so display an error
            # page.
            if ERROR_FLAG in request.GET.keys():
                return SimpleTemplateResponse('admin/invalid_setup.html', {
                    'title': _('Database error'),
                })
            return HttpResponseRedirect(request.path + '?' + ERROR_FLAG + '=1')

        # If the request was POSTed, this might be a bulk action or a bulk
        # edit. Try to look up an action or confirmation first, but if this
        # isn't an action the POST will fall through to the bulk edit check,
        # below.
        action_failed = False
        selected = request.POST.getlist(helpers.ACTION_CHECKBOX_NAME)

        # Actions with no confirmation
        if (actions and request.method == 'POST' and 'index' in request.POST and '_save' not in request.POST):
            if selected:
                response = self.response_action(request, queryset=cl.get_queryset(request))
                if response:
                    return response
                else:
                    action_failed = True
            else:
                msg = _("Items must be selected in order to perform "
                        "actions on them. No items have been changed.")
                self.message_user(request, msg, messages.WARNING)
                action_failed = True

        # Actions with confirmation
        if (actions and request.method == 'POST' and helpers.ACTION_CHECKBOX_NAME in request.POST and 'index' not in request.POST and '_save' not in request.POST):
            if selected:
                import os
                from django.conf import settings
                for id in selected:
                    file = Media.objects.get(id=id, type='i')
                    path = settings.MEDIA_ROOT
                    os.remove(path + 'image/' + file.unique_name)
                    os.remove(path + 'image/thumbnail/512x288/' + file.unique_name)
                    os.remove(path + 'image/thumbnail/256x144/' + file.unique_name)
                    os.remove(path + 'image/thumbnail/128x72/' + file.unique_name)
                    os.remove(path + 'image/thumbnail/144x144/' + file.unique_name)
                    os.remove(path + 'image/thumbnail/100x100/' + file.unique_name)
                    os.remove(path + 'image/thumbnail/848x309/' + file.unique_name)

                response = self.response_action(request, queryset=cl.get_queryset(request))
                if response:
                    return response
                else:
                    action_failed = True

        # If we're allowing changelist editing, we need to construct a formset
        # for the changelist given all the fields to be edited. Then we'll
        # use the formset to validate/process POSTed data.
        formset = cl.formset = None

        # Handle POSTed bulk-edit data.
        if (request.method == "POST" and cl.list_editable and
                    '_save' in request.POST and not action_failed):
            FormSet = self.get_changelist_formset(request)
            formset = cl.formset = FormSet(request.POST, request.FILES, queryset=cl.result_list)
            if formset.is_valid():
                changecount = 0
                for form in formset.forms:
                    if form.has_changed():
                        obj = self.save_form(request, form, change=True)
                        self.save_model(request, obj, form, change=True)
                        self.save_related(request, form, formsets=[], change=True)
                        change_msg = self.construct_change_message(request, form, None)
                        self.log_change(request, obj, change_msg)
                        changecount += 1

                if changecount:
                    if changecount == 1:
                        name = force_text(opts.verbose_name)
                    else:
                        name = force_text(opts.verbose_name_plural)
                    msg = ungettext("%(count)s %(name)s was changed successfully.",
                                    "%(count)s %(name)s were changed successfully.",
                                    changecount) % {'count': changecount,
                                                    'name': name,
                                                    'obj': force_text(obj)}
                    self.message_user(request, msg, messages.SUCCESS)

                return HttpResponseRedirect(request.get_full_path())

        # Handle GET -- construct a formset for display.
        elif cl.list_editable:
            FormSet = self.get_changelist_formset(request)
            formset = cl.formset = FormSet(queryset=cl.result_list)

        # Build the list of media to be used by the formset.
        if formset:
            media = self.media + formset.media
        else:
            media = self.media

        # Build the action form and populate it with available actions.
        if actions:
            action_form = self.action_form(auto_id=None)
            action_form.fields['action'].choices = self.get_action_choices(request)
        else:
            action_form = None

        selection_note_all = ungettext('%(total_count)s selected',
                                       'All %(total_count)s selected', cl.result_count)
        tax_name = ''
        if self.tax:
            tax_name = self.get_tax_name_by_id(tax)
        context = dict(
            self.admin_site.each_context(request),
            module_name=force_text(opts.verbose_name_plural),
            selection_note=_('0 of %(cnt)s selected') % {'cnt': len(cl.result_list)},
            selection_note_all=selection_note_all % {'total_count': cl.result_count},
            title=cl.title,
            is_popup=cl.is_popup,
            to_field=cl.to_field,
            cl=cl,
            media=media,
            has_add_permission=self.has_add_permission(request),
            opts=cl.opts,
            action_form=action_form,
            actions_on_top=self.actions_on_top,
            actions_on_bottom=self.actions_on_bottom,
            actions_selection_counter=self.actions_selection_counter,
            preserved_filters=self.get_preserved_filters(request),
            tax=self.tax,
            type=mode,
            tax_name=tax_name
        )
        context.update(extra_context or {})

        request.current_app = self.admin_site.name

        return TemplateResponse(request, self.change_list_template or [
            'admin/%s/%s/change_list.html' % (app_label, opts.model_name),
            'admin/%s/change_list.html' % app_label,
            'admin/change_list.html'
        ], context)

    def load_image_by_ajax_response(self, request):
        from django.conf import settings
        from django.core.paginator import Paginator, EmptyPage, InvalidPage
        import json
        if request.is_ajax():
            images = Media.objects.filter(type='i').values(
                'id',
                'name',
                'file',
                'description',
                'unique_name',
                'created_at'
            ).order_by('-created_at')
            paging = Paginator(images, 40)
            p = request.GET.get('page')
            try:
                img = paging.page(p)
            except (EmptyPage, InvalidPage):
                img = []

            data = []
            for image in img:
                data.append({
                    'imgid': image['id'],
                    "thumb": settings.MEDIA_URL + 'image/thumbnail/100x100/' + image['unique_name'],
                    "image": settings.MEDIA_URL + 'image/' + image['unique_name'],
                    "title": image['name'],
                    'description': image['description'],
                    'uniquename': image['unique_name'],
                })
            store = [{
                'store': data,
                'page': (int(p) + 1),
            }]
            return HttpResponse(json.dumps(store), content_type='application/json')
        else:
            raise Http404(_('Page not found'))

    def check_tax_id(self, id):
        if Taxonomy.objects.filter(pk=id, type='image'):
            return True
        else:
            return False

    def get_tax_name_by_id(self, id):
        return Taxonomy.objects.get(id=id).name

    def get_file_by_id(self, id):
        return Media.objects.get(id=id)

    def get_queryset(self, request):
        if self.tax:
            return self.model.objects.filter(type='i', relationships=self.tax)
        else:
            return self.model.objects.filter(type='i')


class VideoAdmin(Admin):
    def get_queryset(self, request):
        return self.model.objects.filter(type='video')


class FileAdmin(Admin):
    def get_queryset(self, request):
        return self.model.objects.filter(type='file')


def create_model_name(model, name=None):
    class Meta:
        proxy = True
        app_label = model._meta.app_label

    attrs = {'__module__': '', 'Meta': Meta}

    newmodel = type(name, (model,), attrs)
    return newmodel


create_modeladmin(ImageAdmin, Media, 'Image', _('Image'), _('Images'))
create_modeladmin(VideoAdmin, Media, 'Video', _('Video'), _('Videos'))
create_modeladmin(FileAdmin, Media, 'File', _('File'), _('Files'))
