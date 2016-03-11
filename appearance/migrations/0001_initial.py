# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Widget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('custom_name', models.CharField(max_length=255, verbose_name='Custom Name')),
                ('type', models.CharField(max_length=25, verbose_name='Type')),
                ('content', models.TextField(verbose_name='Content', blank=True)),
                ('position', models.IntegerField(null=True, verbose_name='Position', blank=True)),
                ('setting', models.TextField(verbose_name='Setting', blank=True)),
            ],
            options={
                'db_table': 'ant_widget',
                'verbose_name': 'Widget',
                'verbose_name_plural': 'Widgets',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
            ],
            options={
                'verbose_name': 'Menu',
                'proxy': True,
                'verbose_name_plural': 'Menus',
            },
            bases=('word.taxonomy',),
        ),
    ]
