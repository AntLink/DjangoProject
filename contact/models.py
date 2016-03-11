from django.db import models
from django.utils.translation import ugettext_lazy as _


class Contact(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    email = models.EmailField(_('Email'))
    subject = models.CharField(_('Subject'), max_length=100)
    message = models.TextField(_('Message'))
    parent = models.ForeignKey('self', verbose_name=_('Parent'), null=True, blank=True, db_index=True)
    status = models.BooleanField(_('Status'), max_length=1, default=True, help_text=_('Status is checked will be published.'))
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        db_table = 'ant_contact'

    def __str__(self):
        return self.name
