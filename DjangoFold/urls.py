from django.conf.urls import patterns, include, url
from django.contrib import admin
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

dajaxice_autodiscover()



urlpatterns = patterns('',
	url(r'^japan_tsunami/', include('japan_map.urls')),
	url(r'^worldvis/', include('worldvis.urls')),
	url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)

urlpatterns += staticfiles_urlpatterns()

