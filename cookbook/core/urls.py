from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^recipe/(?P<id>[0-9]+)/$', views.recipe, name='recipe'),
    url(r'^dish/(?P<id>[0-9]+)/$', views.dish, name='dish'),
    url(r'^collection/(?P<id>[0-9]+)/$', views.collection, name='collection'),
]