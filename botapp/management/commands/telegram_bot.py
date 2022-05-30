from django.core.management.base import BaseCommand
from botapp.telegram import bot


class Command(BaseCommand):

    # Запускаем бота

    def handle(self, *args, **options):
        bot.start_bot()
