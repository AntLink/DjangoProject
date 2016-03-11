from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from wysiwyg.widgets import RedactorWidget
from .models import Taxonomy, Word
from .widgets import (
    TreeCheckboxSelectMultiple,
    TitleTextInput,
    UserSelectInput,
    TagFilteredSelectMultiple,
    ImageHideInput,
    ImageGalleryHideInput,
    PriceInput,
    LatitudeInput,
    LongitudeInput,
    WordMetaHideInput,
    StarInput,
    AddressTextInput,
    SidebarInput,
    LayoutSelectInput,
)
from django.utils.translation import ugettext_lazy as _
import json, random, string


class PostForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
            Taxonomy.objects.filter(type='category'),
            widget=TreeCheckboxSelectMultiple(label_css_style='', css_class='category'),
            required=False,
            label=_('Select Categories'),
    )

    tags = forms.ModelMultipleChoiceField(
            Taxonomy.objects.filter(type='tag'),
            widget=TagFilteredSelectMultiple(_('Tags'), True),
            required=False,
            label=_('Select Tags'),
    )

    self_relationships = forms.ModelMultipleChoiceField(
            Word.objects.filter(type='post'),
            widget=FilteredSelectMultiple(_('Post'), True),
            required=False,
            label=_('Self Relationships'),
    )

    page = forms.CharField(
            widget=forms.Select(choices=(
                ('post', _('Informasi')),
                ('hotel', _('Hotel')),
                ('tour_package', _('Tour Package')),
                ('rentcar', _('Car Rental')),
                ('cruiser', _('Cruiser')),
                ('umrah', _('Umrah')),
            )),
            label=_('Post type'),
            required=False,
    )

    price = forms.CharField(
            widget=PriceInput(),
            label=_('Price'),
            required=False
    )
    gallery = forms.CharField(
            widget=ImageGalleryHideInput(),
            label=_('Gallery'),
            required=False
    )

    latitude = forms.CharField(
            widget=LatitudeInput(),
            label=_('Latitude'),
            required=False,
            help_text=_('Used to mark the location map.'),
    )
    longitude = forms.CharField(
            widget=LongitudeInput(),
            label=_('Longitude'),
            required=False,
            help_text=_('Used to mark the location map.'),

    )

    star = forms.CharField(
            widget=StarInput(),
            label=_('Star'),
            required=False,
            help_text=_('How many star hotels?'),
            max_length=1,

    )

    boking_code = forms.CharField(
            widget=forms.HiddenInput(),
            label=_('Boking Code'),
            required=False,
    )

    address = forms.CharField(
            widget=AddressTextInput,
            label=_('Address'),
            required=False,
    )

    sidebar = forms.CharField(
            widget=SidebarInput,
            label=_('Enable Sidebar'),
            required=False
    )

    class Meta:
        widgets = {
            'title': TitleTextInput(attrs={'placeholder': _('Add title here'), 'style': 'font-size: 20px;height: 40px;'}),
            'content': RedactorWidget(allow_images_upload=True, allow_images_json=True, attrs={'placeholder': _('Add content here')}),
            # 'created_at': SuitSplitDateTimeWidget,
            'user': UserSelectInput,
            'image': ImageHideInput,
            'word_meta': WordMetaHideInput
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # self.fields['user_id'].queryset = Post.objects.filter(user_id=2)
        if self.instance.pk:
            self.initial['categories'] = self.instance.relationships.values_list('pk', flat=True)
            self.initial['tags'] = self.instance.relationships.values_list('pk', flat=True)

    def str_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def save(self, *args, **kwargs):
        instance = super(PostForm, self).save(commit=False)
        # update post and relation tag and category
        instance.type = 'post'

        if self.cleaned_data['star'] == '':
            star = 0
        else:
            star = self.cleaned_data['star']

        if self.cleaned_data['price'] == '':
            price = 0
        else:
            price = self.cleaned_data['price']

        if self.cleaned_data['page'] != 'post':
            boking_code = self.str_generator()
        else:
            boking_code = ''

        data = {
            'price': price,
            'latitude': self.cleaned_data['latitude'],
            'longitude': self.cleaned_data['longitude'],
            'gallery': self.cleaned_data['gallery'],
            'star': star,
            'address': self.cleaned_data['address'],
            'boking_code': boking_code,
            'sidebar': self.cleaned_data['sidebar'],
        }
        instance.word_meta = json.dumps(data)
        if instance.pk:
            # we remove tax cat and tag which have been unselected
            for tax in instance.relationships.all():
                if tax not in self.cleaned_data['categories'] or not self.cleaned_data['tags']:
                    instance.relationships.remove(tax)
            # we add newly selected tax cat
            for tax in self.cleaned_data['categories']:
                if tax not in instance.relationships.all():
                    instance.relationships.add(tax)
            # we add newly selected tax tag
            for tag in self.cleaned_data['tags']:
                if tag not in instance.relationships.all():
                    # we add newly selected books
                    instance.relationships.add(tag)
        else:
            # add post and relation tag and category

            instance.save()
            for tax in self.cleaned_data['categories']:
                if tax not in instance.relationships.all():
                    instance.relationships.add(tax)
            # we add newly selected tax tag
            for tag in self.cleaned_data['tags']:
                if tag not in instance.relationships.all():
                    # we add newly selected books
                    instance.relationships.add(tag)
        return instance


class CategoryForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, required=False, max_length=255, help_text=_('Maximum can be entered is 255 text characters'))

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        # access object through self.instance...
        self.fields['parent'].queryset = Taxonomy.objects.filter(type='category')

    # class Meta:
    #     widget = {}

    def save(self, *args, **kwargs):
        instance = super(CategoryForm, self).save(commit=False)
        instance.type = 'category'
        return instance


class TagForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, required=False, max_length=255, help_text=_('Maximum can be entered is 255 text characters'))

    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)

        # access object through self.instance...

    def save(self, *args, **kwargs):
        instance = super(TagForm, self).save(commit=False)
        # update post and relation tag and category
        instance.type = 'tag'
        return instance
