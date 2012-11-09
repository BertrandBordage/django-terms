from django.conf.urls import patterns, url
from .views import TermDetail

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$', TermDetail.as_view(), name='term'),
)
