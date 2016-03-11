from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

class Setting(models.Model):
    name = models.CharField(max_length=35)
    value = models.CharField(max_length=25)
    content = models.TextField(default='AntCMS Content')
    type = models.CharField(max_length=25, blank=True, default='general')
    autoload = models.CharField(max_length=3, blank=True, default='yes')

    class Meta:
        verbose_name = _('Setting')
        db_table = 'ant_setting'

    def __str__(self):
        return self.name
