from django.conf.urls import patterns, include, url
from amazonIndex.views import *

urlpatterns = patterns('',
    url(r'^$',index),
    url(r'^category/$', category),
    url(r'^commodity/$', commodity),
    url(r'^hello/$',hello),
    url(r'^meta/$',meta),
)
