from django.conf.urls import url

from . import views

urlpatterns = [
   url(r'^$', views.index, name='index'),
   url(r'event/(?P<event_id>\d+)$', views.single, name='single'),
]
