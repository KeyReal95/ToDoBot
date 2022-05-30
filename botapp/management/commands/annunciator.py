import time
import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from loguru import logger
from botapp.models import Task
from botapp.telegram.bot import send_notification

class Command(BaseCommand):
    # Класс позволяющий запускать модуль оповещения отдельно от django и бота
    help = '123'

    def __init__(self):
        self.interval = settings.ANNONCES_INTERVAL

    #
    def handle(self, *args, **options):
        while True:
            start_time, finish_time = self.get_time_range()
            tasks = Task.get_task_by_time_range(start_time, finish_time)
            logger.info(f'количество оповещений: {tasks.count()}')
            self.send_notifications(tasks)
            time.sleep(self.interval * 60)

    # Получение временного промежутка в котором нужно заслать уведомление
    def get_time_range(self):

        current_date = datetime.datetime.now()
        start_time = (current_date + datetime.timedelta(minutes=self.interval - 1)).time()
        finish_time = (current_date + datetime.timedelta(minutes=self.interval + 1)).time()
        return start_time, finish_time

    # Отправка уведомлений
    def send_notifications(self, tasks):
        for task in tasks:
            telegram_id = task.user.telegram_id
            task_name = task.name
            time_notification = task.time_notification.strftime("%H:%M")
            text = f'Горящая задача\n{task_name}\nВремя выполнения: {time_notification}'
            send_notification(telegram_id, text)
