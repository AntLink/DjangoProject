# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name', blank=True)),
                ('unique_name', models.CharField(max_length=255, verbose_name='Unique Name')),
                ('file', models.FileField(upload_to=b'', verbose_name='File')),
                ('type', models.CharField(blank=True, max_length=1, verbose_name='Type', choices=[(b'i', 'Image'), (b'f', 'File'), (b'v', 'Video')])),
                ('description', models.CharField(max_length=255, verbose_name='Description', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('relationships', models.ManyToManyField(to='word.Taxonomy', verbose_name='Relationships', blank=True)),
            ],
            options={
                'db_table': 'ant_media',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
            ],
            options={
                'verbose_name': 'File',
                'proxy': True,
                'verbose_name_plural': 'Files',
            },
            bases=('filemedia.media',),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
            ],
            options={
                'verbose_name': 'Image',
                'proxy': True,
                'verbose_name_plural': 'Images',
            },
            bases=('filemedia.media',),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
            ],
            options={
                'verbose_name': 'Video',
                'proxy': True,
                'verbose_name_plural': 'Videos',
            },
            bases=('filemedia.media',),
        ),
    ]
