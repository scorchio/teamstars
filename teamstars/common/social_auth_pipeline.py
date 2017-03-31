from datetime import datetime
from requests import request, HTTPError

from django.contrib import messages
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _

from django.core.files.base import ContentFile
from social_core.pipeline.partial import partial

from models import Profile

import logging
logger = logging.getLogger(__name__)


def save_fb_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook' and user:
        logger.debug('saving FB profile...')
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            logger.debug('no profile yet, creating one')
            profile = Profile.objects.create(user=user)

        profile.fb_link = response.get('link')
        profile.birth_date = datetime.strptime(response.get('birthday'), "%m/%d/%Y")
        profile.location = response.get('location').get('name')
        logger.debug('saving FB profile done!')
        profile.save()


def save_profile_picture(backend, user, response, details,
                         is_new=False, *args, **kwargs):

    if backend.name == 'facebook' and user:
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])

        try:
            response = request('GET', url, params={'type': 'large'})
            response.raise_for_status()
        except HTTPError:
            pass
        else:
            profile = user.profile
            profile.photo.delete()
            profile.photo.save('avatar_{0}.jpg'.format(user.id),
                               ContentFile(response.content))
            profile.save()


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
