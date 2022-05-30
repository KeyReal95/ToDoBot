from django.db import models
from loguru import logger


class User(models.Model):
    # Класс описывающий модель пользователя
    telegram_id = models.IntegerField(null=False, unique=True, primary_key=True, verbose_name="Идентификатор пользователя")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return str(self.telegram_id)

    @staticmethod
    def create(telegram_id: int):
        # Считываем есть ли уже такой пользователь, если нет, то создаём
        logger.info(f'создание пользователя {telegram_id}...')
        try:
            user = User.objects.get(telegram_id=telegram_id)
            logger.warning('пользователь уже существует')
            return user
        except User.DoesNotExist:
            user = User.objects.create(telegram_id=telegram_id)
            logger.info('пользователь создан')
            return user


class Task(models.Model):
    # Описываем модель заданий
    PROCESS = 'PR'
    DONE = 'DN'
    STATUSES = [
        (PROCESS, 'В процессе'),
        (DONE, 'Выполнена'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    name = models.CharField(max_length=200, null=False, verbose_name="Название")
    status = models.CharField(
        max_length=2,
        choices=STATUSES,
        default=PROCESS,
        verbose_name="Статус",
    )
    time_notification = models.TimeField(null=True, verbose_name="Время напоминания")

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.name

    @staticmethod
    def create(user_telegram_id: int, name: str):
        # Создаём задачу в БД
        user = User.objects.get(telegram_id=user_telegram_id)
        logger.info(f"создание задачи {name} в базе")
        return Task.objects.create(user=user, name=name)

    @staticmethod
    def get_tasks_by_user(user_telegram_id: int):
        # Получаем список задач по пользователю
        logger.info("получение задачи по пользователю")
        return Task.objects.filter(user__telegram_id=user_telegram_id, status=Task.PROCESS)

    @staticmethod
    def get_task_by_id(task_id: int):
        # Получение задачи по ID пользователя
        logger.info("получение задачи по ID задачи")
        return Task.objects.get(id=task_id)

    @staticmethod
    def close_task(task_id: int):
        # Завершение / закрытие задачи
        logger.info("зыавершение задачи")
        Task.objects.filter(id=task_id).update(status=Task.DONE)

    @staticmethod
    def get_task_by_time_range(start_time, finish_time):
        # Получение списка залач по временному промежту
        return Task.objects.filter(time_notification__gte=start_time, time_notification__lte=finish_time)

    @staticmethod
    def update_notification_time(task_id: int, time):
        # Заносим в базу время уведомления пользователя
        return Task.objects.filter(id=task_id).update(time_notification=time)
