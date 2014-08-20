from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.urlresolvers import reverse
from pycountry import languages as l
import re

from django.contrib.auth import get_user_model
User = get_user_model()


# Managers
class ContributionMixin(object):
    def by_author(self, user):
        kwargs = {'is_deleted': False,
                  'author': user}
        return self.filter(**kwargs)

    def published(self):
        kwargs = {'is_deleted': False,
                  'is_published': True,
                  'published_on__lte': timezone.now()}
        return self.filter(**kwargs)


class ContributionQuerySet(QuerySet, ContributionMixin):
    pass


class ContributionManager(models.Manager, ContributionMixin):
    def get_query_set(self):
        return ContributionQuerySet(self.model, using=self._db)


class PublishedContributionsManager(models.Manager):
    """Filters out all unpublished items and items with a publication date in the future."""
    def get_queryset(self):
        kwargs = {'is_deleted': False,
                  'is_published': True,
                  'published_on__lte': timezone.now()}
        return super(PublishedContributionsManager, self).get_query_set().filter(**kwargs)


class Contribution(models.Model):
    # CHOICES Definitions #####################################################
    DCTERMS_ABSTRACT_LANG_CHOICES = filter(lambda x: x[0] and x[1],
                                           map(lambda x: (getattr(x, 'alpha2', None),
                                                          getattr(x, 'name', None)),
                                               l))
    # Metadata fields #########################################################
    #dc_type
    #vcard_category
    dc_identifier = models.AutoField(
        _("dc:identifier"),
        primary_key=True)
    dc_title = models.CharField(
        _("dc:title"),
        max_length=100)
    dc_date = models.DateTimeField(
        _("dc:date"), )
    dc_relation = models.CharField(
        _("dc:relation"),
        max_length=200,
        blank=True)
    #vcard_logo
    dc_publisher = models.CharField(
        _("dc:publisher"),
        max_length=200,
        blank=True)
    #dcterms_spatial
    dc_coverage = models.CharField(
        _("dc:coverage"),
        max_length=200,
        blank=True)
    #vcard_organization
    dc_subject = models.CharField(
        _("dc:subject"),
        max_length=50,
        blank=True)
    dcterms_abstract = models.TextField(
        _("dcterms:abstract"),
        blank=True)
    dcterms_abstract_lang = models.CharField(
        _("dcterms:abstract lang"),
        max_length=2,
        choices=DCTERMS_ABSTRACT_LANG_CHOICES,
        default='en')
    dc_description = models.TextField(
        _("dc:description"),
        blank=True)
    #sioc_topic
    #sioc_has_scope
    dc_creator = models.ManyToManyField(
        'DcCreator',
        _("dc:creator"),
        blank=True,
        null=True)
    dc_contributor = models.ManyToManyField(
        'DcContributor',
        _("dc:contributor"),
        blank=True,
        null=True)

    # Meta-Metadata fields ####################################################
    author = models.ForeignKey(
        User,
        verbose_name=_('author'),
        editable=False,
        blank=True,
        null=True)
    is_published = models.BooleanField(
        _('is published?'),
        default=False)
    published_on = models.DateTimeField(
        _('published on'),
        blank=True,
        null=True)
    last_modified_on = models.DateTimeField(
        _('last modified on'),
        default=timezone.now,
        editable=False)
    is_deleted = models.BooleanField(
        _('is deleted?'),
        default=False,
        editable=False)

    # Managers ################################################################
    objects = ContributionManager()
    published = PublishedContributionsManager()

    def __unicode__(self):
        return self.dc_title

    def get_absolute_url(self):
        return reverse('dariah_contributions:detail', kwargs={'pk': self.pk})

    def attrs(self):
        patt = re.compile('_id$')
        for attr, value in self.__dict__.iteritems():
            if not attr.startswith('_'):  # Extract private attributes
                yield self._meta.get_field(patt.sub('', attr)).verbose_name, value

    def has_owner(self, user):
        return self.author == user

    class Meta:
        ordering = ['-published_on', ]
        get_latest_by = 'published_on'
        verbose_name = _('contribution')
        verbose_name_plural = _('contributions')

    def save(self, *args, **kwargs):
        """Add publication date is now if published is True but no date was selected"""
        if self.is_published and not self.published_on:
            self.published_on = timezone.now()
        """ Always add last_modified_on date """
        self.last_modified_on = timezone.now()
        super(Contribution, self).save(*args, **kwargs)


class Person(models.Model):
    foaf_person = models.CharField(max_length=50, blank=True)
    foaf_name = models.CharField(max_length=50, blank=True)
    foaf_publications = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return self.foaf_name

    class Meta:
        abstract = True


class DcCreator(Person):
    class Meta:
        verbose_name = 'dc:creator'
        verbose_name_plural = 'dc:creator'


class DcContributor(Person):
    class Meta:
        verbose_name = 'dc:contributor'
        verbose_name_plural = 'dc:contributor'
