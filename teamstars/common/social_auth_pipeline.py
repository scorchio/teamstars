from datetime import datetime

import requests
from requests import request

from django.contrib import messages
from django.core.files.base import ContentFile
from django.utils.translation import ugettext as _

from models import Profile

import logging
logger = logging.getLogger(__name__)


def save_fb_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook' and user:
        logger.debug('Saving/updating FB profile.')
        Profile.objects.update_or_create(
            user=user,
            defaults={
                'fb_link': response.get('link'),
                'birthday': datetime.strptime(response.get('birthday'), "%m/%d/%Y") if 'birthday' in response else None,
                'location': response.get('location').get('name', '') if 'location' in response else None,
            })


def save_profile_picture(backend, user, response, details,
                         is_new=False, *args, **kwargs):

    if backend.name == 'facebook' and user:
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])

        response = request('GET', url, params={'type': 'large'})
        if response.status_code == requests.codes.ok:
            profile = user.profile
            profile.photo.delete()
            profile.photo.save('avatar_{0}.jpg'.format(user.id),
                               ContentFile(response.content), save=True)


def handle_errors(strategy, details, user=None, *args, **kwargs):
    if not user:
        messages.info(strategy.request,
                      _("We couldn't find your user. There might be two reasons: either you're not registered yet, or "
                      "the email address that we know about doesn't match your email address in Facebook. Please contact "
                      "the site administrator to fix this."))


# @partial
#def pick_username(backend, details, response, is_new=False, *args, **kwargs):
#     if backend.name == 'facebook': # and is_new:
#        return render_to_response('pick_username.html')
