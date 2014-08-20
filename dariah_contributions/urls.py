from django.conf.urls import patterns, url

from .views import ContributionCreate
from .views import ContributionDelete
from .views import ContributionUpdate
from .views import ContributionRDF
from .views import MyContributions
from .views import ContributionDetail
from .views import ContributionList


urlpatterns = patterns('',
    url(r'^(all/)?$', ContributionList.as_view(), name='list'),
    # example: /contribution/
    # example: /contribution/all/
    url(r'^mine/$', MyContributions.as_view(), name='mine'),
    url(r'^add/$', ContributionCreate.as_view(), name='add'),
    # example: /contribution/add/
    url(r'^(?P<pk>\d+)/update/$', ContributionUpdate.as_view(), name='update'),
    # example: /contribution/5/update/
    url(r'^(?P<pk>\d+)/delete/$', ContributionDelete.as_view(), name='delete'),
    # example: /contribution/5/delete/
    url(r'^(?P<pk>\d+)\.xml$', ContributionRDF.as_view(), name='detail_rdf'),
    # example: /contribution/detail_rdf/5/
    url(r'^(?P<pk>\d+)/$', ContributionDetail.as_view(), name='detail'),
    # example: /contribution/5/
)
