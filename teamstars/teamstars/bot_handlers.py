from telegrambot.bot_views.generic import TemplateCommandView
from telegrambot.handlers import command


class StartView(TemplateCommandView):
    template_text = "bot/messages/command_start_text.txt"

urlpatterns = [
    command('start', StartView.as_command_view()),
]
