# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
            ],
            options={
                'verbose_name': 'Page',
                'proxy': True,
                'verbose_name_plural': 'Pages',
            },
            bases=('word.word',),
        ),
        migrations.CreateModel(
            name='Index',
            fields=[
            ],
            options={
                'verbose_name': 'Page',
                'proxy': True,
                'verbose_name_plural': 'Pages',
            },
            bases=('page.page',),
        ),
    ]
