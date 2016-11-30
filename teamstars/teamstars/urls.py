from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers

from serializers import UserViewSet, VoteViewSet, VoteTypeViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'votes', VoteViewSet)
router.register(r'votes-types', VoteTypeViewSet)

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^api/', include(router.urls)),
                       url(r'^api-auth/', include('rest_framework.urls')),
                       )
