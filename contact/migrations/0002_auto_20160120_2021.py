# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'verbose_name': 'Message', 'verbose_name_plural': 'Message'},
        ),
        migrations.AddField(
            model_name='contact',
            name='parent',
            field=models.ForeignKey(verbose_name='Parent', blank=True, to='contact.Contact', null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='status',
            field=models.BooleanField(default=True, help_text='Status is checked will be published.', max_length=1, verbose_name='Status'),
        ),
    ]
