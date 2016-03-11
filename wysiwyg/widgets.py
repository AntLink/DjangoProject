from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse_lazy
from django.conf import settings

from wysiwyg.utils import json_dumps

GLOBAL_OPTIONS = getattr(settings, 'REDACTOR_OPTIONS', {})


class RedactorWidget(widgets.Textarea):
    def __init__(self, *args, **kwargs):
        self.upload_to = kwargs.pop('upload_to', '')
        self.custom_options = kwargs.pop('redactor_options', {})
        self.allow_file_upload = kwargs.pop('allow_file_upload', False)
        self.allow_image_upload = kwargs.pop('allow_image_upload', False)
        self.allow_imagemanager_upload = kwargs.pop('allow_imagemanager_upload', False)
        self.allow_images_json = kwargs.pop('allow_images_json', False)
        self.allow_images_json_update = kwargs.pop('allow_images_json_update', True)
        self.allow_images_upload = kwargs.pop('allow_images_upload', False)
        super(RedactorWidget, self).__init__(*args, **kwargs)

    @property
    def options(self):
        options = GLOBAL_OPTIONS.copy()
        options.update(self.custom_options)
        if self.allow_file_upload:
            options['fileUpload'] = reverse_lazy(
                'redactor_upload_file',
                kwargs={'upload_to': self.upload_to}
            )
        if self.allow_image_upload:
            options['imageUpload'] = reverse_lazy(
                'redactor_upload_image',
                kwargs={'upload_to': self.upload_to}
            )
        if self.allow_imagemanager_upload:
            options['imageUpload'] = reverse_lazy(
                'redactor_upload_image',
                kwargs={'upload_to': self.upload_to}
            )
        if self.allow_images_json:
            options['imagesUrlLoadJson'] = reverse_lazy(
                'admin:filemedia_image_jsonload',
            )
        if self.allow_images_upload:
            options['imagesUrlupload'] = reverse_lazy(
                'admin:filemedia_image_upload',
            )
        if self.allow_images_json_update:
            options['imagesUrlJsonUpdate'] = reverse_lazy(
                'admin:filemedia_image_jsonupdate',
            )
        return options

    def render(self, name, value, attrs=None):
        if 'class' not in attrs.keys():
            attrs['class'] = ''

        attrs['class'] += ' redactor-box'

        attrs['data-redactor-options'] = json_dumps(self.options)

        html = super(RedactorWidget, self).render(name, value, attrs)

        return mark_safe(html)

    def _media(self):
        js = (
            'redactor/jquery.redactor.init.js',
            'redactor/redactor{0}.js'.format('' if settings.DEBUG else '.min'),
            'redactor/langs/{0}.js'.format(GLOBAL_OPTIONS.get('lang', 'en')),
        )

        if 'plugins' in self.options:
            plugins = self.options.get('plugins')
            for plugin in plugins:
                js = js + (
                    'redactor/plugins/{0}.js'.format(plugin),
                )

        css = {
            'all': (
                'redactor/redactor.css',
                # 'redactor/css/django_admin.css',
            )
        }
        return forms.Media(css=css, js=js)

    media = property(_media)
