from django.conf.urls import url
from .views import TermDetail

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', TermDetail.as_view(), name='term'),
]
