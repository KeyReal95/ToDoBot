import datetime
from botapp.models import Task
from .sends import send_tasks
from .bot import bot


def create_task(message):
    task = Task.create(message.chat.id, message.text)

    message_text = f"Создана задача {task.name}"
    bot.send_message(chat_id=message.chat.id, text=message_text)

    message_text = "Хотите создать напоминание для задачи?\nНапиши 'Да' или 'Нет'"
    bot.send_message(chat_id=message.chat.id, text=message_text)

    bot.register_next_step_handler(message, check_notification, task.id)


def check_notification(message, task_id):
    message_text = message.text.lower()
    if message_text == "нет":
        send_tasks(message.chat.id)
    elif message_text == "да":
        message_text = "Отправь время: (например 12:31)"
        bot.send_message(message.chat.id, message_text)
        bot.register_next_step_handler(message, set_notification_time, task_id)


def set_notification_time(message, task_id):
    # TODO: сделать валидацию даты/времени
    hour, minute = message.text.split(":")
    notification_time = datetime.time(hour=int(hour), minute=int(minute), second=0)
    Task.update_notification_time(task_id, notification_time)