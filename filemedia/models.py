from django.db import models
from word.models import Taxonomy
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class Media(models.Model):
    class Meta:
        db_table = 'ant_media'

    relationships = models.ManyToManyField(Taxonomy, blank=True, verbose_name=_('Relationships'))
    name = models.CharField(_('Name'),max_length=255, blank=True)
    unique_name = models.CharField(_('Unique Name'),max_length=255)
    file = models.FileField(_('File'))
    type = models.CharField(_('Type'),max_length=1, blank=True, choices=(('i', _('Image')), ('f', _('File')), ('v', _('Video'))))
    description = models.CharField(_('Description'),max_length=255, blank=True)
    created_at = models.DateTimeField(_('Created At'),auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    def delete(self, *args, **kwargs):
        initial = super(Media, self).delete(*args, **kwargs)
        import os
        from django.conf import settings
        path = settings.MEDIA_ROOT
        os.remove(path + 'image/' + self.unique_name)
        os.remove(path + 'image/thumbnail/512x288/' + self.unique_name)
        os.remove(path + 'image/thumbnail/256x144/' + self.unique_name)
        os.remove(path + 'image/thumbnail/128x72/' + self.unique_name)
        os.remove(path + 'image/thumbnail/144x144/' + self.unique_name)
        os.remove(path + 'image/thumbnail/100x100/' + self.unique_name)
        return initial

    def thumbnail(self):
        if self.unique_name:
            return u'<label style="position: absolute; margin-top:10px; margin-left:4px; " class="form-checkbox form-normal form-primary form-text">' \
                   u'<input class="action-select" name="_selected_action" type="checkbox" value="%s">' \
                   u'</label>' \
                   u'<img src="/media/image/thumbnail/100x100/%s" alt="%s" />' % (self.pk, self.unique_name, self.name)

    thumbnail.allow_tags = True

    def images(self):
        if self.unique_name:
            name = u'<b style="padding:0 5px 0 5px">%s</b>' % self.name
            edit = u'<a href="%s">%s</a>' % (reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id]), _('Edit'))
            delete = u'<a href="%s">%s</a>' % (reverse('admin:%s_%s_delete' % (self._meta.app_label, self._meta.model_name), args=[self.id]), _('Delete'))
            return u'<img style="width:40px" src="/media/image/thumbnail/100x100/%s" alt="%s" />%s<br><small >%s &nbsp; %s</small>' % (self.unique_name, self.name, name, edit, delete)

    images.allow_tags = True
    images.short_description = _('Gambar')

    def __str__(self):
        return self.name

    def tags(self):
        return ",&nbsp;".join([u'<a href="%s">%s</a>' % (reverse('admin:%s_%s_tags' % (self._meta.app_label, self._meta.model_name), args=[p.pk, 'list']), p.name) for p in self.relationships.all()])

    tags.allow_tags = True
    tags.short_description = _('Tags')