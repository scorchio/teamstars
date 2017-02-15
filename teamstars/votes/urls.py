from django.conf.urls import url

from . import views

urlpatterns = [
   url(r'^$', views.index, name='vote_index'),
   url(r'add/', views.add, name='vote_add'),
   url(r'logout/', views.logout_view, name='logout_redirect')
]
