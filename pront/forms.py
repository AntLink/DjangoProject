from django import forms
from filemedia.search import BaseSearchForm
from word.models import Word


class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(
            required=True,
            widget=forms.Textarea
    )


class SearchForm(BaseSearchForm):
    class Meta:
        model = Word
        fields = ['title', 'content', 'status', 'relationships']
        base_qs = Word.objects
        search_fields = ('title', 'content')
        fulltext_indexes = (
            ('title', 2),  # name matches are weighted higher
            ('title,content,id', 1),
        )


