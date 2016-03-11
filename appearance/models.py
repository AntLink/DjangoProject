from django.db import models
from word.models import Taxonomy
from django.utils.translation import ugettext_lazy as _


class Menu(Taxonomy):
    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _('Menus')
        proxy = True


class Widget(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    custom_name = models.CharField(_('Custom Name'), max_length=255)
    type = models.CharField(_('Type'), max_length=25)
    content = models.TextField(_('Content'), blank=True)
    position = models.IntegerField(_('Position'), blank=True, null=True)
    setting = models.TextField(_('Setting'), blank=True)

    class Meta:
        verbose_name = _('Widget')
        verbose_name_plural = _('Widgets')
        db_table = "ant_widget"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Widget, self).save(*args, **kwargs)
