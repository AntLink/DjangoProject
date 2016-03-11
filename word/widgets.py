from django import forms
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import FilteredSelectMultiple


class TitleTextInput(forms.TextInput): pass


class AddressTextInput(forms.TextInput): pass


class UserSelectInput(forms.Select): pass

class LayoutSelectInput(forms.Select): pass


class SidebarInput(forms.CheckboxInput): pass


class TagFilteredSelectMultiple(FilteredSelectMultiple): pass


class ImageGalleryHideInput(forms.HiddenInput): pass


class WordMetaHideInput(forms.HiddenInput): pass


class PriceInput(forms.NumberInput): pass


class StarInput(forms.NumberInput): pass


class LatitudeInput(forms.TextInput): pass


class LongitudeInput(forms.TextInput): pass


class ImageHideInput(forms.HiddenInput): pass


class SelfRelationships(forms.ModelMultipleChoiceField): pass


class TreeCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def __init__(self, css_class=None, label_css_style=None, value='pk', label='name', level='level', **kwargs):
        super(TreeCheckboxSelectMultiple, self).__init__(**kwargs)
        self.css_class = css_class
        self.label_css_style = label_css_style
        self.value = value
        self.label = label
        self.level = level

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)

        output = []
        if self.css_class:
            output.append(u'<ul class="%s">' % self.css_class)
        else:
            output.append(u'<ul>')

        str_values = set([force_unicode(v) for v in value])
        i = 0
        for tax in self.choices.queryset.values(self.value, self.label, self.level):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (
                    attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''

            cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_unicode(tax['%s' % self.value])
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_unicode(tax['%s' % self.label]))
            if tax['%s' % self.label] == 0:
                output.append(u'<li>')
            else:
                output.append(u'<li style="margin-left: %spx;">' % (tax['%s' % self.level] * 16))

            output.append(u'<div class="checkbox"><div class="form-cat form-checkbox form-normal  form-text" style="%s" %s>%s <span clas="text-muted">%s</div></label></div>' % (self.label_css_style, label_for, rendered_cb, option_label))

        # output.append(u'</li>')
        # output.append(u'</ul>')
        return mark_safe(u'\n'.join(output))
