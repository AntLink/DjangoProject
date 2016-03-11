from django.contrib import admin
from suit.admin import Admin, create_modeladmin
from .forms import ContactForm
from .models import Contact


class ContactAdmin(Admin):
    form = ContactForm
    search_fields = ['name', 'email', 'subject', 'message']
    list_display = ('name', 'email', 'subject','status','created_at')


create_modeladmin(ContactAdmin, Contact, 'Message', 'Message', 'Message')
