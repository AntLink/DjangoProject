from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message','status']
        search_fields = ('name', 'email', 'subject', 'message')
        widgets = {
            'message': forms.Textarea()
        }
