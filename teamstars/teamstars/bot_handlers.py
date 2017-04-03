from django.core import serializers
from telegrambot.bot_views.decorators import login_required
from telegrambot.bot_views.generic import TemplateCommandView
from telegrambot.handlers import command

import logging
logger = logging.getLogger(__name__)


class StartView(TemplateCommandView):
    template_text = "bot_messages/command_start_text.txt"


class AuthView(TemplateCommandView):
    template_text = "bot_messages/command_auth_test.txt"
    context_object_name = "user"

    def get_context(self, bot, update, **kwargs):
        logging.debug("bot: {json}".format(json=serializers.serialize("json", bot, indent=2)))
        logging.debug("update: {json}".format(json=serializers.serialize("json", update, indent=2)))
        context = {self.context_object_name : 'user'}
        return context

urlpatterns = [
    command('start', StartView.as_command_view()),
    command('auth', login_required(AuthView.as_command_view())),
]
