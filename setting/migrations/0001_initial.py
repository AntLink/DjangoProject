# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from setting.data import load_general_setting_stores


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
                name='Setting',
                fields=[
                    ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                    ('name', models.CharField(max_length=35)),
                    ('value', models.CharField(max_length=25)),
                    ('content', models.TextField(default=b'AntCMS Content')),
                    ('type', models.CharField(default=b'general', max_length=25, blank=True)),
                    ('autoload', models.CharField(default=b'yes', max_length=3, blank=True)),
                ],
                options={
                    'db_table': 'ant_setting',
                    'verbose_name': 'Setting',
                },
        ),
        migrations.CreateModel(
                name='Admin',
                fields=[
                ],
                options={
                    'verbose_name': 'Admin',
                    'proxy': True,
                    'verbose_name_plural': 'Admin',
                },
                bases=('setting.setting',),
        ),
        migrations.CreateModel(
                name='Discussion',
                fields=[
                ],
                options={
                    'verbose_name': 'Discussion',
                    'proxy': True,
                    'verbose_name_plural': 'Discussion',
                },
                bases=('setting.setting',),
        ),
        migrations.CreateModel(
                name='General',
                fields=[
                ],
                options={
                    'verbose_name': 'General',
                    'proxy': True,
                    'verbose_name_plural': 'General',
                },
                bases=('setting.setting',),
        ),
        migrations.CreateModel(
                name='Media',
                fields=[
                ],
                options={
                    'verbose_name': 'Media',
                    'proxy': True,
                    'verbose_name_plural': 'Media',
                },
                bases=('setting.setting',),
        ),
        migrations.CreateModel(
                name='Permalink',
                fields=[
                ],
                options={
                    'verbose_name': 'Permalink',
                    'proxy': True,
                    'verbose_name_plural': 'Permalink',
                },
                bases=('setting.setting',),
        ),
        migrations.CreateModel(
                name='Reading',
                fields=[
                ],
                options={
                    'verbose_name': 'Reading',
                    'proxy': True,
                    'verbose_name_plural': 'Reading',
                },
                bases=('setting.setting',),
        ),
        migrations.CreateModel(
                name='Writing',
                fields=[
                ],
                options={
                    'verbose_name': 'Writing',
                    'proxy': True,
                    'verbose_name_plural': 'Writing',
                },
                bases=('setting.setting',),
        ),
        migrations.RunPython(load_general_setting_stores),
    ]
