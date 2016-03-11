from django.contrib.admin.filters import SimpleListFilter


class AuthorPublised(SimpleListFilter):
    title = 'Status'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('p', 'Published'),
            ('d', 'Draft'),
            ('t', 'Trash'),
        )

    def queryset(self, request, queryset):
        if self.value() is 'd':
            return queryset.filter(status='d')
            # if self.value() is 'p':
            #     return queryset.filter(status='p')
            # if self.value() is 't':
            #     return queryset.filter(status='t')
