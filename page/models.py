from word.models import Word
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class Page(Word):
    class Meta:
        proxy = True
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')

    def get_absolute_url(self):
        return reverse('page', kwargs={"tax": self.slug})
