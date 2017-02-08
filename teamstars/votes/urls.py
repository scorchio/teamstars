from django.conf.urls import url

from . import views

urlpatterns = [
   url(r'^$', views.index, name='vote_index'),
   url(r'logout/', views.logout_view, name='logout_redirect')
]
