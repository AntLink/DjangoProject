# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('subject', models.CharField(max_length=100, verbose_name='Subject')),
                ('message', models.TextField(verbose_name='Message')),
            ],
            options={
                'db_table': 'ant_contact',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
            ],
            options={
                'verbose_name': 'Message',
                'proxy': True,
                'verbose_name_plural': 'Verbose Name Plural',
            },
            bases=('contact.contact',),
        ),
    ]
