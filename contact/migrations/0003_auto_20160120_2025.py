# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_auto_20160120_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 20, 12, 24, 56, 716411, tzinfo=utc), verbose_name='Created At', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contact',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 20, 12, 25, 9, 812249, tzinfo=utc), verbose_name='Updated At', auto_now=True),
            preserve_default=False,
        ),
    ]
