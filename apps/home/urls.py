from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^trips/new$', views.new_trip),
    url(r'^process_new_trip$', views.process_new_trip),
    url(r'^trips/edit/(?P<trip_id>\d+)$', views.edit_trip),
    url(r'^process_edit_trip/(?P<trip_id>\d+)$', views.process_edit_trip),
    url(r'^trips/(?P<trip_id>\d+)$', views.view_trip),
    url(r'^join/(?P<trip_id>\d+)$', views.join),
    url(r'^cancel/(?P<trip_id>\d+)$', views.cancel),
    url(r'^remove/(?P<trip_id>\d+)$', views.remove),
]