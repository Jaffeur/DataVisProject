from django.conf.urls import patterns, url
from worldvis import views


urlpatterns = patterns('',
    url(r'^$', views.world_map, name='world_map'),
)