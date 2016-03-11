import copy
from django import forms
from django.conf import settings
from django.contrib.admin import ModelAdmin, helpers
from django.contrib.admin.views.main import ChangeList
from django.forms import ModelForm
from django.contrib import admin
from django.db import models
from suit.widgets import NumberInput, SuitSplitDateTimeWidget
from suit.compat import ct_admin
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.contrib.auth.models import User as MyUser, Group as MyGroup
from django.contrib.auth.apps import AuthConfig
from django.contrib.admin.templatetags.admin_static import static
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.forms import UserChangeForm
from setting.models import Setting
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.actions import delete_selected

AuthConfig.verbose_name = (_('Authorization'))

delete_selected.short_description = _("Delete selected %(verbose_name_plural)s")

from django.db import DatabaseError



try:
    Setting.objects.exists()
except DatabaseError:
    pass
else:
    st = Setting.objects.filter(value='site_language')[0]
    settings.LANGUAGE_CODE = st.content
    settings.REDACTOR_OPTIONS = {
        'plugins': [
            'video',
            'images',
            'fullscreen',
            'table',
        ],
        'lang': st.content
    }


def create_modeladmin(modeladmin, model, name=None, vname='Verbose Name', vnamep='Verbose Name Plural'):
    class Meta:
        proxy = True
        app_label = model._meta.app_label
        verbose_name = vname
        verbose_name_plural = vnamep

    attrs = {'__module__': '', 'Meta': Meta}
    newmodel = type(name, (model,), attrs)

    admin.site.register(newmodel, modeladmin)
    return modeladmin


class Admin(admin.ModelAdmin):
    def get_action_choices(self, request, default_choices=[('', _('Bulk Actions'))]):
        return super(Admin, self).get_action_choices(request, default_choices)

    def action_checkbox(self, obj):
        """
        A list_display column containing a checkbox widget.
        """
        return u'<label class="form-checkbox form-normal form-primary">%s</label>' % helpers.checkbox.render(
                helpers.ACTION_CHECKBOX_NAME, force_text(obj.pk))

    action_checkbox.short_description = mark_safe(
            '<label class="form-checkbox form-normal form-primary"><input type="checkbox" id="action-toggle" /></label>')
    action_checkbox.allow_tags = True


class MyGroupAdmin(GroupAdmin):
    list_display = ['name']

    def get_action_choices(self, request, default_choices=[('', _('Bulk Actions'))]):
        return super(MyGroupAdmin, self).get_action_choices(request, default_choices)

    def action_checkbox(self, obj):
        """
        A list_display column containing a checkbox widget.
        """
        return u'<label class="form-checkbox form-normal form-primary">%s</label>' % helpers.checkbox.render(
                helpers.ACTION_CHECKBOX_NAME, force_text(obj.pk))

    action_checkbox.short_description = mark_safe(
            '<label class="form-checkbox form-normal form-primary"><input type="checkbox" id="action-toggle" /></label>')
    action_checkbox.allow_tags = True


admin.site.unregister(MyGroup)
admin.site.register(MyGroup, MyGroupAdmin)


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = '__all__'
        widgets = {
            'last_login': SuitSplitDateTimeWidget(),
            'date_joined': SuitSplitDateTimeWidget,
        }


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active')

    def get_action_choices(self, request, default_choices=[('', _('Bulk Actions'))]):
        return super(MyUserAdmin, self).get_action_choices(request, default_choices)

    def action_checkbox(self, obj):
        """
        A list_display column containing a checkbox widget.
        """
        return u'<label class="form-checkbox form-normal form-primary">%s</label>' % helpers.checkbox.render(
                helpers.ACTION_CHECKBOX_NAME, force_text(obj.pk))

    action_checkbox.short_description = mark_safe(
            '<label class="form-checkbox form-normal form-primary"><input type="checkbox" id="action-toggle" /></label>')
    action_checkbox.allow_tags = True


admin.site.unregister(MyUser)
admin.site.register(MyUser, MyUserAdmin)


class SortableModelAdminBase(object):
    """
    Base class for SortableTabularInline and SortableModelAdmin
    """
    sortable = 'order'

    class Media:
        js = ('suit/js/sortables.js',)


class SortableListForm(ModelForm):
    """
    Just Meta holder class
    """

    class Meta:
        widgets = {
            'order': NumberInput(
                    attrs={'class': 'hide input-mini suit-sortable'})
        }


class SortableChangeList(ChangeList):
    """
    Class that forces ordering by sortable param only
    """

    def get_ordering(self, request, queryset):
        return [self.model_admin.sortable, '-' + self.model._meta.pk.name]


class SortableTabularInlineBase(SortableModelAdminBase):
    """
    Sortable tabular inline
    """

    def __init__(self, *args, **kwargs):
        super(SortableTabularInlineBase, self).__init__(*args, **kwargs)

        self.ordering = (self.sortable,)
        self.fields = self.fields or []
        if self.fields and self.sortable not in self.fields:
            self.fields = list(self.fields) + [self.sortable]

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == self.sortable:
            kwargs['widget'] = SortableListForm.Meta.widgets['order']
        return super(SortableTabularInlineBase, self).formfield_for_dbfield(
                db_field, **kwargs)


class SortableTabularInline(SortableTabularInlineBase, admin.TabularInline):
    pass


class SortableGenericTabularInline(SortableTabularInlineBase,
                                   ct_admin.GenericTabularInline):
    pass


class SortableStackedInlineBase(SortableModelAdminBase):
    """
    Sortable stacked inline
    """

    def __init__(self, *args, **kwargs):
        super(SortableStackedInlineBase, self).__init__(*args, **kwargs)
        self.ordering = (self.sortable,)

    def get_fieldsets(self, *args, **kwargs):
        """
        Iterate all fieldsets and make sure sortable is in the first fieldset
        Remove sortable from every other fieldset, if by some reason someone
        has added it
        """
        fieldsets = super(SortableStackedInlineBase, self).get_fieldsets(
                *args, **kwargs)

        sortable_added = False
        for fieldset in fieldsets:
            for line in fieldset:
                if not line or not isinstance(line, dict):
                    continue

                fields = line.get('fields')

                # Some use tuples for fields however they are immutable
                if isinstance(fields, tuple):
                    raise AssertionError(
                            "The fields attribute of your Inline is a tuple. "
                            "This must be list as we may need to modify it and "
                            "tuples are immutable."
                    )

                if self.sortable in fields:
                    fields.remove(self.sortable)

                # Add sortable field always as first
                if not sortable_added:
                    fields.insert(0, self.sortable)
                    sortable_added = True
                    break

        return fieldsets

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == self.sortable:
            kwargs['widget'] = copy.deepcopy(
                    SortableListForm.Meta.widgets['order'])
            kwargs['widget'].attrs['class'] += ' suit-sortable-stacked'
            kwargs['widget'].attrs['rowclass'] = ' suit-sortable-stacked-row'
        return super(SortableStackedInlineBase, self).formfield_for_dbfield(
                db_field, **kwargs)


class SortableStackedInline(SortableStackedInlineBase, admin.StackedInline):
    pass


class SortableGenericStackedInline(SortableStackedInlineBase,
                                   ct_admin.GenericStackedInline):
    pass


class SortableModelAdmin(SortableModelAdminBase, ModelAdmin):
    """
    Sortable tabular inline
    """
    list_per_page = 500

    def __init__(self, *args, **kwargs):
        super(SortableModelAdmin, self).__init__(*args, **kwargs)

        self.ordering = (self.sortable,)
        if self.list_display and self.sortable not in self.list_display:
            self.list_display = list(self.list_display) + [self.sortable]

        self.list_editable = self.list_editable or []
        if self.sortable not in self.list_editable:
            self.list_editable = list(self.list_editable) + [self.sortable]

        self.exclude = self.exclude or []
        if self.sortable not in self.exclude:
            self.exclude = list(self.exclude) + [self.sortable]

    def merge_form_meta(self, form):
        """
        Prepare Meta class with order field widget
        """
        if not getattr(form, 'Meta', None):
            form.Meta = SortableListForm.Meta
        if not getattr(form.Meta, 'widgets', None):
            form.Meta.widgets = {}
        form.Meta.widgets[self.sortable] = SortableListForm.Meta.widgets[
            'order']

    def get_changelist_form(self, request, **kwargs):
        form = super(SortableModelAdmin, self).get_changelist_form(request,
                                                                   **kwargs)
        self.merge_form_meta(form)
        return form

    def get_changelist(self, request, **kwargs):
        return SortableChangeList

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            max_order = obj.__class__.objects.aggregate(
                    models.Max(self.sortable))
            try:
                next_order = max_order['%s__max' % self.sortable] + 1
            except TypeError:
                next_order = 1
            setattr(obj, self.sortable, next_order)
        super(SortableModelAdmin, self).save_model(request, obj, form, change)


# Quite aggressive detection and intrusion into Django CMS
# Didn't found any other solutions though
if 'cms' in settings.INSTALLED_APPS:
    try:
        from cms.admin.forms import PageForm

        PageForm.Meta.widgets = {
            'publication_date': SuitSplitDateTimeWidget,
            'publication_end_date': SuitSplitDateTimeWidget,
        }
    except ImportError:
        pass
