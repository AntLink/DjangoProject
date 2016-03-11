try:
    from django.conf.urls import url, patterns
except ImportError:
    # for Django version less than 1.4
    from django.conf.urls.defaults import url, patterns

from wysiwyg.views import RedactorUploadView, json_view
from wysiwyg.forms import FileForm, ImageForm

urlpatterns = patterns(
    '',
    url(r'^upload/image/(?P<upload_to>.*)',
        RedactorUploadView.as_view(form_class=ImageForm),
        name='redactor_upload_image'),

    url(r'^upload/file/(?P<upload_to>.*)',
        RedactorUploadView.as_view(form_class=FileForm),
        name='redactor_upload_file'),

    url(r'^image/load/json', json_view, name='redactor_get_json'),
)
