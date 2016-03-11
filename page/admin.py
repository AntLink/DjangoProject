from suit.admin import Admin
from page.models import Page
from suit.admin import create_modeladmin
from django.utils.translation import ugettext_lazy as _
from .forms import PageForm


class PageAdmin(Admin):
    form = PageForm
    change_form_template = 'admin/page/change_form.html'
    search_fields = ['title', 'content', 'status']
    fieldsets = [
        (None, {'fields': ('title',)}),
        (None, {'classes': ('full-width',), 'fields': ('content',)}),
        ('Basic setting', {'fields': ('image', 'page', 'slug', 'user', 'status', 'comment_status')}),
    ]

    list_display = ('title', 'user', 'status', 'created_at')
    prepopulated_fields = {'slug': ('title',)}

    def get_list_filter(self, request):
        if request.user.is_superuser:
            self.list_filter = ['user', 'status', 'created_at']
        else:
            self.list_filter = ['status', 'created_at']
        return self.list_filter

    def get_queryset(self, request):
        if request.user.is_active and request.user.is_superuser:
            return self.model.objects.filter(type='page')
        else:
            return self.model.objects.filter(type='page', user_id=request.user.id)


create_modeladmin(PageAdmin, Page, 'Index', _('Page'), _('Pages'))
