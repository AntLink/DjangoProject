from django.contrib.admin import helpers
from .models import Taxonomy, Word
from .forms import PostForm, CategoryForm, TagForm
from django.core.exceptions import PermissionDenied
from mptt.admin import MPTTModelAdmin
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from suit.admin import Admin, create_modeladmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.utils import unquote
import json
from django.forms.formsets import all_valid


def make_published(self, request, queryset):
    opts = self.model._meta
    if request.user.has_perm("word.published_post"):
        rows_updated = queryset.update(status='p')
        if rows_updated == 1:
            message_bit = _("1 %(verbose_name)s") % {'verbose_name': opts.verbose_name}
        else:
            message_bit = "%s %s" % (rows_updated, _(opts.verbose_name))
        self.message_user(request, "%s %s" % (message_bit, _('successfully published.')))
    else:
        raise PermissionDenied


def make_draft(self, request, queryset):
    opts = self.model._meta
    if request.user.has_perm("word.draft_post"):
        rows_updated = queryset.update(status='d')
        if rows_updated == 1:
            message_bit = _("1 %(verbose_name)s") % {'verbose_name': opts.verbose_name}
        else:
            message_bit = "%s %s" % (rows_updated, _(opts.verbose_name))
        self.message_user(request, "%s %s" % (message_bit, _('successfully moved to draft.')))
    else:
        raise PermissionDenied


def make_trash(self, request, queryset):
    opts = self.model._meta
    if request.user.has_perm("word.trash_post"):
        rows_updated = queryset.update(status='t')
        if rows_updated == 1:
            message_bit = _("1 %(verbose_name)s") % {'verbose_name': opts.verbose_name}
        else:
            message_bit = "%s %s" % (rows_updated, _(opts.verbose_name))
        self.message_user(request, "%s %s" % (message_bit, _('successfully moved to trash.')))
    else:
        raise PermissionDenied


make_published.short_description = _("Publish %(verbose_name_plural)s selected")
make_draft.short_description = _("Move to archives %(verbose_name_plural)s selected")
make_trash.short_description = _("Move to trash %(verbose_name_plural)s selected")


class PostAdmin(Admin):
    form = PostForm
    search_fields = ['title', 'content', 'status', 'relationships__name', 'relationships__description']
    fieldsets = [
        (None, {'fields': ('title',)}),
        (None, {'classes': ('full-width',), 'fields': ('content',)}),
        (_('Post Type'), {'fields': ('page', 'price', 'star', 'address', 'latitude', 'longitude', 'word_meta',)}),
        (_('Basic setting'), {'fields': ('image', 'slug', 'user', 'gallery', 'status','layout', 'comment_status','sidebar', 'tags', 'categories',)}),
        (_('Post Relationship'), {'fields': ('self_relationships',)}),
    ]

    list_display = ('title', 'user', 'status', 'categories', 'tags', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    actions = [make_draft, make_published, make_trash]
    change_form_template = 'admin/post/change_form.html'
    gallery = ''
    latitude = ''
    longitude = ''
    price = ''
    star = ''
    address = ''
    sidebar = ''


    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        # super(PostAdmin, self).changeform_view()
        to_field = request.POST.get('_to_field', request.GET.get('_to_field'))
        if to_field and not self.to_field_allowed(request, to_field):
            raise DisallowedModelAdminToField("The field %s cannot be referenced." % to_field)

        model = self.model
        opts = model._meta
        add = object_id is None

        if add:
            if not self.has_add_permission(request):
                raise PermissionDenied
            obj = None

        else:
            obj = self.get_object(request, unquote(object_id), to_field)

            if not self.has_change_permission(request, obj):
                raise PermissionDenied

            if obj is None:
                raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {
                    'name': force_text(opts.verbose_name), 'key': escape(object_id)})

            if request.method == 'POST' and "_saveasnew" in request.POST:
                return self.add_view(request, form_url=reverse('admin:%s_%s_add' % (
                    opts.app_label, opts.model_name),
                                                               current_app=self.admin_site.name))

        ModelForm = self.get_form(request, obj)
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form_validated = True
                new_object = self.save_form(request, form, change=not add)
            else:
                form_validated = False
                new_object = form.instance
            formsets, inline_instances = self._create_formsets(request, new_object, change=not add)
            if all_valid(formsets) and form_validated:
                self.save_model(request, new_object, form, not add)
                self.save_related(request, form, formsets, not add)
                if add:
                    self.log_addition(request, new_object)
                    return self.response_add(request, new_object)
                else:
                    change_message = self.construct_change_message(request, form, formsets)
                    self.log_change(request, new_object, change_message)
                    return self.response_change(request, new_object)
        else:
            if add:
                initial = self.get_changeform_initial_data(request)
                form = ModelForm(initial=initial)
                formsets, inline_instances = self._create_formsets(request, self.model(), change=False)
            else:
                form = ModelForm(instance=obj)
                formsets, inline_instances = self._create_formsets(request, obj, change=True)

        adminForm = helpers.AdminForm(
                form,
                list(self.get_fieldsets(request, obj)),
                self.get_prepopulated_fields(request, obj),
                self.get_readonly_fields(request, obj),
                model_admin=self)
        media = self.media + adminForm.media

        inline_formsets = self.get_inline_formsets(request, formsets, inline_instances, obj)
        for inline_formset in inline_formsets:
            media = media + inline_formset.media
        if (object_id != None):
            word_meta = json.loads(self.model.objects.get(pk=object_id).word_meta)
            self.gallery = word_meta['gallery']
            self.price = word_meta['price']
            self.latitude = word_meta['latitude']
            self.longitude = word_meta['longitude']
            self.star = word_meta['star']
            self.address = word_meta['address']
            self.sidebar = word_meta['sidebar']
        else:
            self.gallery = ''
            self.price = ''
            self.latitude = ''
            self.longitude = ''
            self.star = ''
            self.address = ''
            self.sidebar = False
        context = dict(self.admin_site.each_context(request),
                       title=(_('Add %s') if add else _('Change %s')) % force_text(opts.verbose_name),
                       adminform=adminForm,
                       object_id=object_id,
                       original=obj,
                       is_popup=('_popup' in request.POST or
                                 '_popup' in request.GET),
                       to_field=to_field,
                       media=media,
                       gallery=self.gallery,
                       price=self.price,
                       lat=self.latitude,
                       long=self.longitude,
                       star=self.star,
                       address=self.address,
                       sidebar=self.sidebar,
                       inline_admin_formsets=inline_formsets,
                       errors=helpers.AdminErrorList(form, formsets),
                       preserved_filters=self.get_preserved_filters(request),
                       )

        context.update(extra_context or {})

        return self.render_change_form(request, context, add=add, change=not add, obj=obj, form_url=form_url)

    def get_list_filter(self, request):
        if request.user.is_superuser:
            self.list_filter = ['user', 'status', 'created_at']
        else:
            self.list_filter = ['status', 'created_at']
        return self.list_filter

    def get_queryset(self, request):
        if request.user.is_active and request.user.is_superuser:
            return self.model.objects.filter(type='post')
        else:
            return self.model.objects.filter(type='post', user_id=request.user.id)


class CategoryAdmin(Admin):
    form = CategoryForm
    search_fields = ['name', 'slug', 'status']
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'status')
    list_filter = ['status']
    fieldsets = [
        (None, {'fields': ('name', 'slug', 'parent', 'description', 'status')}),
    ]

    change_list_template = 'admin/category/category_change_list.html'

    def get_queryset(self, request):
        return self.model.objects.filter(type='category')

    # def get_action_choices(self, request, default_choices=[('', _('Bulk Actions'))]):
    #     return super(CategoryAdmin, self).get_action_choices(request, default_choices)

    def action_checkbox(self, obj):
        return u'<label class="form-checkbox form-normal form-primary">%s</label>' % helpers.checkbox.render(helpers.ACTION_CHECKBOX_NAME, force_text(obj.pk))

    action_checkbox.short_description = mark_safe(u'<label class="form-checkbox form-normal form-primary"><input type="checkbox" id="action-toggle" /></label>')
    action_checkbox.allow_tags = True


class TagAdmin(Admin):
    form = TagForm
    search_fields = ['name', 'slug', 'status', 'description', ]
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'description', 'status')
    list_filter = ['status']
    fieldsets = [
        (None, {'fields': ('name', 'slug', 'description', 'status')}),
    ]

    def get_queryset(self, request):
        return self.model.objects.filter(type='tag')


create_modeladmin(PostAdmin, Word, 'Post', _('Post'), _('Posts'))
create_modeladmin(CategoryAdmin, Taxonomy, 'Category', _('Category'), _('Categories'))
create_modeladmin(TagAdmin, Taxonomy, 'Tag', _('Tag'), _('Tags'))
