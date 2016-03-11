from mptt.admin import MPTTAdminForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Menu
from mptt.forms import TreeNodeChoiceField
from word.widgets import TreeCheckboxSelectMultiple

from wysiwyg.widgets import RedactorWidget
from word.models import Taxonomy

class MenuForm(MPTTAdminForm):
    parent = TreeNodeChoiceField(
            Menu.objects.filter(type='menu'),
            required=False,
            label=_('Parent'),
    )

    categories = forms.ModelMultipleChoiceField(
            Menu.objects.filter(type='category'),
            widget=TreeCheckboxSelectMultiple(label_css_style='', css_class='category'),
            required=False,
            label=_('Select Categories'),
    )

    class Meta:
        widgets = {
            'menu_type': forms.Select(choices=((None, _('Select location')), ('navbar', 'Navbar'), ('topbar', 'Topbar'), ('footer', 'Footer'))),
            'name': forms.TextInput(),
            'slug': forms.TextInput()
        }

    def save(self, *args, **kwargs):
        instance = super(MenuForm, self).save(commit=False)
        instance.type = 'menu_parent'
        try:
            Menu.objects.get(menu_type=self.cleaned_data['menu_type'])
        except Menu.DoesNotExist:
            instance.menu_type = self.cleaned_data['menu_type']
        else:
            menu = Menu.objects.get(menu_type=self.cleaned_data['menu_type'])
            menu.menu_type = None
            menu.save()
        return instance


class WidgetForm(forms.ModelForm):
    class Meta:
        widgets = {
            'custom_name': forms.TextInput(),
            'type': forms.Select(choices=(('sidebar', 'Sidebar'), ('footer1', 'Footer 1'), ('footer2', 'Footer 2'), ('footer3', 'Footer 3'), ('footer4', 'Footer 4'))),
            'content': RedactorWidget(redactor_options={'plugins': ['images'], 'buttons': ['html', 'alignment', 'bold', 'italic', 'link']}, allow_images_upload=True, allow_images_json=True, attrs={'placeholder': _('Add content here')}),
        }


class TextForm(forms.Form):
    title = forms.CharField(required=True)
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={'style': 'resize: none; height: 200px'}))
    position = forms.CharField(required=False, widget=forms.Select(
            choices=(
                ('sidebar', 'Sidebar'),
                ('footer1', 'Footer 1'),
                ('footer2', 'Footer 2'),
                ('footer3', 'Footer 3'),
                ('footer4', 'Footer 4'),
                ('home_content', 'Home Content'),
                ('contact_sidebar', 'Contact Sidebar'),
            )
    ))
    show_title = forms.CharField(widget=forms.CheckboxInput(attrs={'value': 'yes'}))


class HtmlForm(forms.Form):
    title = forms.CharField(required=True)
    content = forms.CharField(widget=RedactorWidget(redactor_options={'plugins': ['images', 'fullscreen'], 'buttons': ['html', 'alignment', 'bold', 'italic', 'link', 'unorderedlist', 'orderedlist']}, allow_images_upload=True, allow_images_json=True, attrs={'placeholder': _('Add content here')}))
    position = forms.CharField(required=False, widget=forms.Select(
            choices=(
                ('sidebar', 'Sidebar'),
                ('footer1', 'Footer 1'),
                ('footer2', 'Footer 2'),
                ('footer3', 'Footer 3'),
                ('footer4', 'Footer 4'),
                ('home_content', 'Home Content'),
                ('contact_sidebar', 'Contact Sidebar'),
            )
    ))
    show_title = forms.CharField(widget=forms.CheckboxInput(attrs={'value': 'yes'}))


class TagForm(forms.Form):
    title = forms.CharField(required=True)
    taxonomy = forms.CharField(required=False, widget=forms.Select(
            choices=(
                ('tag', 'Tags'),
                ('category', 'Category')
            )
    ))
    position = forms.CharField(required=False, widget=forms.Select(
            choices=(
                ('sidebar', 'Sidebar'),
                ('footer1', 'Footer 1'),
                ('footer2', 'Footer 2'),
                ('footer3', 'Footer 3'),
                ('footer4', 'Footer 4'),
                ('home_content', 'Home Content'),
                ('contact_sidebar', 'Contact Sidebar'),
            )
    ))
    show_title = forms.CharField(widget=forms.CheckboxInput(attrs={'value': 'yes'}))

    display = forms.CharField(required=False, widget=forms.Select(
            choices=(
                ('cloud', _('Display as cloud')),
                ('list', _('Display as list')),
                ('home_content', _('Home content 1')),
                ('home_content_2', _('Home content 2')),
                ('home_content_3', _('Home content 3')),
                ('home_content_4', _('Home content 4')),
                ('home_content_5', _('Home content 5')),
            )
    ))
    limit = forms.CharField(required=True, widget=forms.TextInput(attrs={'type': 'number'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'style': 'resize: none; height: 200px'}))


class CategoryForm(forms.Form):
    title = forms.CharField(required=True)

    position = forms.CharField(required=False, widget=forms.Select(
            choices=(
                ('sidebar', 'Sidebar'),
                ('footer1', 'Footer 1'),
                ('footer2', 'Footer 2'),
                ('footer3', 'Footer 3'),
                ('footer4', 'Footer 4'),
                ('home_content', 'Home Content'),
                ('contact_sidebar', 'Contact Sidebar'),
            )
    ))
    show_title = forms.CharField(widget=forms.CheckboxInput(attrs={'value': 'yes'}))

    display = forms.CharField(required=False, widget=forms.Select(
            choices=(
                ('tree', _('Display as tree')),
                ('list', _('Display as list')),
                ('home_content', _('Home content 1')),
                ('home_content_2', _('Home content 2')),
                ('home_content_3', _('Home content 3')),
                ('home_content_4', _('Home content 4')),
                ('home_content_5', _('Home content 5')),
            )
    ))
    limit = forms.CharField(required=True, widget=forms.TextInput(attrs={'type': 'number'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'style': 'resize: none; height: 200px'}))


class RecentPostForm(forms.Form):
    title = forms.CharField(required=True)

    position = forms.CharField(required=False, widget=forms.Select(
            choices=(
                ('sidebar', 'Sidebar'),
                ('footer1', 'Footer 1'),
                ('footer2', 'Footer 2'),
                ('footer3', 'Footer 3'),
                ('footer4', 'Footer 4'),
                ('home_content', 'Home Content'),
                ('contact_sidebar', 'Contact Sidebar'),
            )
    ))
    show_title = forms.CharField(widget=forms.CheckboxInput(attrs={'value': 'yes'}))

    display = forms.CharField(required=False, widget=forms.Select(
            choices=(
                ('media', _('Display as media')),
                ('list', _('Display as list')),
                ('home_content', _('Home content 1')),
                ('home_content_2', _('Home content 2')),
                ('home_content_3', _('Home content 3')),
                ('home_content_4', _('Home content 4')),
                ('home_content_5', _('Home content 5')),
                ('contact_sidebar', 'Contact Sidebar'),
            )
    ))

    border_color = forms.CharField()

    limit = forms.CharField(required=True, widget=forms.TextInput(attrs={'type': 'number'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'style': 'resize: none; height: 200px'}))


class LinksForm(forms.Form):
    title = forms.CharField(required=True)

    position = forms.CharField(required=False, widget=forms.Select(
            choices=(
                ('sidebar', 'Sidebar'),
                ('footer1', 'Footer 1'),
                ('footer2', 'Footer 2'),
                ('footer3', 'Footer 3'),
                ('footer4', 'Footer 4'),
                ('home_content', 'Home Content'),
                ('contact_sidebar', 'Contact Sidebar'),
            )
    ))
    show_title = forms.CharField(widget=forms.CheckboxInput(attrs={'value': 'yes'}))

    display = forms.CharField(required=False, widget=forms.Select(
            choices=(
                ('media', _('Display as media')),
                ('list', _('Display as list')),
                ('home_content', _('Home content 1')),
                ('home_content_2', _('Home content 2')),
                ('home_content_3', _('Home content 3')),
                ('home_content_4', _('Home content 4')),
                ('home_content_5', _('Home content 5')),
                ('contact_sidebar', 'Contact Sidebar'),
            )
    ))

    categories = forms.ModelMultipleChoiceField(
            Taxonomy.objects.filter(type='category'),
            widget=TreeCheckboxSelectMultiple(label_css_style='', css_class='category'),
            required=False,
            label=_('Select Categories'),
    )
