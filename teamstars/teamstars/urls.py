from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework import routers
from rest_framework.authtoken import views

from serializers import UserViewSet, VoteViewSet, VoteTypeViewSet

from api_views import LeaderboardViewSet
from common import views as common_views
import settings as app_settings

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'votes', VoteViewSet)
router.register(r'votes-types', VoteTypeViewSet)
router.register(r'leaderboard', LeaderboardViewSet, base_name='list')

urlpatterns = [
   url(r'^$', common_views.index),
   url(r'^admin/', include(admin.site.urls)),
   url(r'^api/', include(router.urls)),
   url(r'^api/token-auth/', views.obtain_auth_token),
   url(r'^user/', include('common.urls')),
   url('', include('social_django.urls', namespace='social')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if app_settings.votes_enabled():
    urlpatterns += url(r'^votes/', include('votes.urls')),

if app_settings.calendar_enabled():
    urlpatterns += url(r'^calendar/', include('calendstar.urls')),

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
