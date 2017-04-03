from django.core.management.base import BaseCommand

import kronos
from telegram import ParseMode
from telegrambot.models import Bot


@kronos.register('/1 * * * *')
class Command(BaseCommand):
    help = 'Sends updates to Telegram bot.'

    def handle(self, *args, **options):
        bot = Bot.objects.first()
        bot.send_message(chat_id=70371207, text="I'm still here ^^", reply_markup=None, parse_mode=ParseMode.MARKDOWN)

