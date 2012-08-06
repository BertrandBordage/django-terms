from django.conf.urls.defaults import patterns, url
from .views import TermDetail

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$', TermDetail.as_view(), name='term'),
)
