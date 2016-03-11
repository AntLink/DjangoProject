# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Taxonomy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('slug', models.SlugField(help_text='A short label, generally used in URLs.', max_length=35, null=True, verbose_name='Slug')),
                ('status', models.BooleanField(default=True, help_text='Status is checked will be published.', max_length=1, verbose_name='Status')),
                ('type', models.CharField(max_length=25, verbose_name='Type')),
                ('description', models.CharField(max_length=255, verbose_name='Description', blank=True)),
                ('position', models.IntegerField(null=True, verbose_name='Position', blank=True)),
                ('menu_type', models.CharField(max_length=25, null=True, verbose_name='Menu Type', blank=True)),
                ('root', models.IntegerField(null=True, verbose_name='Root', blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(verbose_name='Parent', blank=True, to='word.Taxonomy', null=True)),
            ],
            options={
                'db_table': 'ant_taxonomy',
            },
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(help_text='A short label, generally used in URLs.', max_length=255)),
                ('content', models.TextField(verbose_name='Content', blank=True)),
                ('image', models.CharField(max_length=255, null=True, verbose_name='Image', blank=True)),
                ('type', models.CharField(max_length=25, verbose_name='Type')),
                ('status', models.CharField(max_length=1, verbose_name='Status', choices=[(b'd', b'Draft'), (b'p', b'Published'), (b't', b'Trash')])),
                ('comment_status', models.BooleanField(default=False, help_text='Is checked will be actived on prontand.', max_length=1, verbose_name='Allow comments')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('page', models.TextField(null=True, blank=True)),
                ('word_meta', models.TextField(null=True, blank=True)),
                ('relationships', mptt.fields.TreeManyToManyField(to='word.Taxonomy', db_table=b'ant_word_relationships', verbose_name='Relationships', db_column=b'word_id', blank=True)),
                ('self_relationships', models.ManyToManyField(related_name='self_relationships_rel_+', db_table=b'ant_self_relationships', verbose_name='Self Relationships', to='word.Word', blank=True)),
                ('user', models.ForeignKey(verbose_name='Author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'ant_word',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
            ],
            options={
                'verbose_name': 'Category',
                'proxy': True,
                'verbose_name_plural': 'Categories',
            },
            bases=('word.taxonomy',),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
            ],
            options={
                'verbose_name': 'Post',
                'proxy': True,
                'verbose_name_plural': 'Posts',
            },
            bases=('word.word',),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
            ],
            options={
                'verbose_name': 'Tag',
                'proxy': True,
                'verbose_name_plural': 'Tags',
            },
            bases=('word.taxonomy',),
        ),
    ]
