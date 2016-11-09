from django.conf.urls import patterns, url

from .views_v2 import (
    AgreementListAPIView,
    AgreementDetailAPIView,
)

urlpatterns = (
    url(r'^partners/(?P<partner_pk>\d+)/agreements/$', view=AgreementListAPIView.as_view(), name='parter-agreement-list'),
    url(r'^partners/(?P<partner_pk>\d+)/agreements/(?P<pk>\d+)/$', view=AgreementDetailAPIView.as_view(), name='partner-agreement-detail'),
)
