from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class WordConfig(AppConfig):
    name = 'word'
    verbose_name = _("Words")
