from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework import routers
from rest_framework.authtoken import views as authtoken_views

from common.api_views import UserViewSet
from votes.api_views import VoteViewSet, VoteTypeViewSet, LeaderboardViewSet
from calendstar.api_views import CalendarEventViewSet, CalendarEventResponseViewSet

from common import views as common_views

import settings as app_settings


urlpatterns = [
   url(r'^$', common_views.index),
   url(r'^admin/', include(admin.site.urls)),
   url(r'^user/', include('common.urls')),
   url('', include('social_django.urls', namespace='social')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

api_router = routers.DefaultRouter()
api_router.register(r'users', UserViewSet)

if app_settings.votes_enabled():
    urlpatterns += [url(r'^votes/', include('votes.urls'))]
    api_router.register(r'votes', VoteViewSet)
    api_router.register(r'votes-types', VoteTypeViewSet)
    api_router.register(r'leaderboard', LeaderboardViewSet, base_name='list')

if app_settings.calendar_enabled():
    urlpatterns += [url(r'^calendar/', include('calendstar.urls'))]
    api_router.register(r'events', CalendarEventViewSet)

urlpatterns += [
    url(r'^api/v1/', include(api_router.urls)),
    url(r'^api/v1/token-auth/', authtoken_views.obtain_auth_token)
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
