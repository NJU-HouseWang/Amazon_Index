from django.conf.urls import patterns, include, url
from Amazon_Index.views import *

urlpatterns = patterns(
    '',
    url(r'^$', index),
    url(r'^category/$', category),
    url(r'^commodity/$', commodity),
)
