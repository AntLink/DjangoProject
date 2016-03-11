from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class Taxonomy(MPTTModel):
    name = models.CharField(_('Name'), max_length=50, unique=False)
    parent = TreeForeignKey('self', verbose_name=_('Parent'), null=True, blank=True, db_index=True)
    slug = models.SlugField(_('Slug'), max_length=35, null=True, unique=False, help_text=_('A short label, generally used in URLs.'))
    status = models.BooleanField(_('Status'), max_length=1, default=True, help_text=_('Status is checked will be published.'))
    type = models.CharField(_('Type'), max_length=25)
    description = models.CharField(_('Description'), max_length=255, blank=True)
    position = models.IntegerField(_('Position'), blank=True, null=True)
    menu_type = models.CharField(_('Menu Type'), max_length=25, null=True, blank=True)
    root = models.IntegerField(_('Root'), blank=True, null=True)

    class Meta:
        db_table = 'ant_taxonomy'

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     super(Taxonomy, self).save(*args, **kwargs)

    def images(self):
        return u'<div style="width:35px">%s</div>' % join(
                [u'<img style="width:35px" src="/media/image/thumbnail/100x100/%s"  />' % p.file for p in self.relationships.filter(type='i')[:4]]
        )

    images.allow_tags = True


class Word(models.Model):
    user = models.ForeignKey(User, verbose_name=_('Author'), blank=True, null=True)
    title = models.CharField(_('Title'), max_length=255)
    slug = models.SlugField(max_length=255, help_text=_('A short label, generally used in URLs.'))
    content = models.TextField(_('Content'), blank=True)
    image = models.CharField(_('Image'), max_length=255, blank=True, null=True)
    type = models.CharField(_('Type'), max_length=25)
    status = models.CharField(_('Status'), max_length=1, choices=(
        ('d', 'Draft'),
        ('p', 'Published'),
        ('t', 'Trash'),
    ))
    comment_status = models.BooleanField(max_length=1, default=False, verbose_name=_('Allow comments'), help_text=_('Is checked will be actived on prontand.'))
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    relationships = TreeManyToManyField(Taxonomy, verbose_name=_('Relationships'), blank=True, db_table='ant_word_relationships', db_column='word_id')
    self_relationships = models.ManyToManyField('self', verbose_name=_('Self Relationships'), blank=True, db_table='ant_self_relationships')
    page = models.TextField(blank=True, null=True)
    word_meta = models.TextField(blank=True, null=True)
    layout = models.CharField(_('Layout'), max_length=255, choices=(
        ('none', _('None')),
        ('right', _('Sidebar Right')),
        ('left', _('Sidebar Left')),
        ('pull', _('Pull'))
    ))

    class Meta:
        db_table = 'ant_word'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={"tax": self.get_category_slug_first(), "slug": self.slug})

    def categories(self):
        return ", ".join([str(p) for p in self.relationships.filter(type='category')])

    def tags(self):
        return ", ".join([str(p) for p in self.relationships.filter(type='tag')])

    def tags_with_pront_li_tag(self):
        return " ".join([u'<li><a href="%s">%s</a></li>' % (reverse('tags', kwargs={"tax": p.slug}), p.name) for p in self.relationships.filter(type='tag')])

    def categories_with_pront_url(self):
        return ",&nbsp;".join([u'<a href="%s">%s</a>' % (reverse('categories', kwargs={"tax": p.slug}), p.name) for p in self.relationships.filter(type='category')])

    def tags_with_pront_url(self):
        return ",&nbsp;".join([u'<a href="%s">%s</a>' % (reverse('tags', kwargs={"tax": p.slug}), p.name) for p in self.relationships.filter(type='tag')])

    def get_category_slug_first(self):
        tax = self.relationships.filter(type='category')
        if len(tax) == 0:
            return 'tax'
        else:
            cat = self.relationships.filter(type='category')[0]
            return cat.slug

    def get_category_name_first(self):
        tax = self.relationships.filter(type='category')
        if len(tax) == 0:
            return 'None'
        else:
            cat = self.relationships.filter(type='category')[0]
            return cat.name

    def get_category_name_with_url_first(self):
        tax = self.relationships.filter(type='category')
        if len(tax) == 0:
            return 'None'
        else:
            cat = self.relationships.filter(type='category')[0]
            return u'<a href="%s">%s</a>' % (reverse('tags', kwargs={"tax": cat.slug}), cat.name)

    tags.allow_tags = True
    tags.short_description = _('Tags')
    categories.allow_tags = True
    categories.short_description = _('Categories')
