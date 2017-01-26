from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import routers

from serializers import UserViewSet, VoteViewSet, VoteTypeViewSet

from api_views import LeaderboardViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'votes', VoteViewSet)
router.register(r'votes-types', VoteTypeViewSet)
router.register(r'leaderboard', LeaderboardViewSet, base_name='list')

urlpatterns = [
   url(r'^admin/', include(admin.site.urls)),
   url(r'^api/', include(router.urls)),
   url(r'^api-auth/', include('rest_framework.urls')),
   url(r'^votes/', include('votes.urls')),
   url('', include('social_django.urls', namespace='social'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
