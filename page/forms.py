from django import forms
from django.utils.translation import ugettext_lazy as _
from word.widgets import TitleTextInput, UserSelectInput, ImageHideInput
from wysiwyg.widgets import RedactorWidget


class PageForm(forms.ModelForm):
    class Meta:
        widgets = {
            'title': TitleTextInput(attrs={'placeholder': _('Add title here'), 'style': 'font-size: 20px;height: 40px;'}),
            'content': RedactorWidget(allow_images_upload=True, allow_images_json=True, attrs={'placeholder': _('Add content here')}),
            'user': UserSelectInput,
            'image': ImageHideInput,
            'page': forms.Select(choices=(
                (None, 'None'),
                ('home','Home'),
                ('contact','Contact'),
                ('privacy','Privacy'),
                ('company_profile','Company profile'),
                ('user_profile','User profile'),
            ))
        }

    def save(self, *args, **kwargs):
        instance = super(PageForm, self).save(commit=False)
        # update post and relation tag and category
        instance.type = 'page'
        return instance
