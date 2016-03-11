from django.contrib import admin
from suit.admin import Admin, create_modeladmin
from django.utils.translation import ugettext_lazy as _
from .models import Setting


class GeneralSettingAdmin(Admin):
    def get_queryset(self, request):
        return self.model.objects.filter(type="general")


class WritingSettingAdmin(Admin):
    def get_queryset(self, request):
        return self.model.objects.filter(type="writing")


class ReadingSettingAdmin(Admin):
    def get_queryset(self, request):
        return self.model.objects.filter(type="reading")


class DiscussionSettingAdmin(Admin):
    def get_queryset(self, request):
        return self.model.objects.filter(type="discussion")


class MediaSettingAdmin(Admin):
    def get_queryset(self, request):
        return self.model.objects.filter(type="media")


class PermalinkSettingAdmin(Admin):
    def get_queryset(self, request):
        return self.model.objects.filter(type="permalink")

class AdminSettingAdmin(Admin):
    def get_queryset(self, request):
        return self.model.objects.filter(type="admin")


create_modeladmin(GeneralSettingAdmin, Setting, 'General', _('General'), _('General'))
create_modeladmin(WritingSettingAdmin, Setting, 'Writing', _('Writing'), _('Writing'))
create_modeladmin(ReadingSettingAdmin, Setting, 'Reading', _('Reading'), _('Reading'))
create_modeladmin(DiscussionSettingAdmin, Setting, 'Discussion', _('Discussion'), _('Discussion'))
create_modeladmin(MediaSettingAdmin, Setting, 'Media', _('Media'), _('Media'))
create_modeladmin(PermalinkSettingAdmin, Setting, 'Permalink', _('Permalink'), _('Permalink'))
create_modeladmin(AdminSettingAdmin, Setting, 'Admin', _('Admin'), _('Admin'))
