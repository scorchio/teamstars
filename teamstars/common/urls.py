from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.settings, name='settings'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'common/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
]
