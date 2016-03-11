# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='layout',
            field=models.CharField(default=datetime.datetime(2016, 3, 10, 11, 30, 12, 548284, tzinfo=utc), max_length=255, verbose_name='Layout', choices=[(b'none', 'None'), (b'right', 'Sidebar Right'), (b'left', 'Sidebar Left'), (b'pull', 'Pull')]),
            preserve_default=False,
        ),
    ]
