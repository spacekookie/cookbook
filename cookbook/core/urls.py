from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^recipe/(?P<id>[0-9]+)/$', views.recipe, name='recipe'),
  url(r'^dish/(?P<id>[0-9]+)/$', views.dish, name='dish'),
  url(r'^collection/(?P<id>[0-9]+)/$', views.collection, name='collection'),

  url(r'^register/$', views.register, name='register'),
  url(r'^register/(?P<id>[0-9]+)/$', views.register_confirm, name='register_confirm'),

  url(r'^login/$', views.login, name='login'),
  url(r'^logout/$', views.logout, name='logout'),

  url(r'^user/(?P<id>[0-9]+)/$', views.profile, name='profile'),
  url(r'^user/(?P<id>[0-9]+)/edit/$', views.profile_edit, name='profile_edit'),

  # List views
  url(r'^users/$', views.list_view_users, name='list_users'),
  url(r'^dishes/$', views.list_view_dishes, name='list_dishes'),
  url(r'^ingredients/$', views.list_view_ingredients, name='list_ingredients'),
]