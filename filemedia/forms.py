from django import forms
from .models import Media as Image
from word.widgets import TagFilteredSelectMultiple
from word.models import Taxonomy
from .search import BaseSearchForm
from django.utils.translation import ugettext_lazy as _


class ImageCategoryForm(forms.ModelForm):
    def save(self, *args, **kwargs):
        instance = super(ImageCategoryForm, self).save(commit=False)
        instance.type = 'image'
        return instance


class ImageForm(BaseSearchForm):
    description = forms.CharField(
        label=_('Description'),
        widget=forms.Textarea,
        required=False,
        max_length=255,
        help_text=_('Maximum can be entered is 255 text characters')
    )
    relationships = forms.ModelMultipleChoiceField(
        Taxonomy.objects.filter(type='image'),
        widget=TagFilteredSelectMultiple(_('Tags'), True),
        required=False,
        label=_('Select Tags'),
    )

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Image
        fields = ['file', 'name', 'description', 'relationships']
        base_qs = Image.objects
        search_fields = ('name', 'description')
        fulltext_indexes = (
            ('name', 2),  # name matches are weighted higher
            ('name,description,id', 1),
        )
