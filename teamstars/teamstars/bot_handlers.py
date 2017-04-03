from telegrambot.bot_views.generic import TemplateCommandView
from telegrambot.handlers import command

import logging
logger = logging.getLogger(__name__)


class StartView(TemplateCommandView):
    logger.debug("Incoming start view!")
    template_text = "bot/messages/command_start_text.txt"

urlpatterns = [
    command('start', StartView.as_command_view()),
]
