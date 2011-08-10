from django.conf.urls.defaults import *
from django.contrib import admin


urlpatterns = patterns('',
	url(r'^$', 'vineyard.views.index'),
)
