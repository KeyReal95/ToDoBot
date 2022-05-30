import telebot
from django.conf import settings
from botapp.models import User, Task
from botapp.telegram.generate_keyboards import *
import datetime, time


bot = telebot.TeleBot(settings.BOT_TOKEN)


def send_start_menu(chat_id: int):
    # Генерируем стартовое меню и шлём его в сообщении
    start_menu = generate_start_menu()
    bot.send_message(chat_id=chat_id, text="Выберите нужный пункт:", reply_markup=start_menu)


def send_notification(telegram_id: int, text: str):
    # Отправляем уведомление о необходимости выполнения задачи
    bot.send_message(telegram_id, text)


def close_task(task_id: int):
    # Закрываем/завершаем задачу
    Task.close_task(task_id)


def send_tasks(chat_id: int):
    # Отправляем список задач по юзеру
    tasks = Task.get_tasks_by_user(chat_id)
    logger.info("формирование списка задач")
    if not tasks.exists():
        bot.send_message(
            chat_id=chat_id,
            text="У тебя нет невыполненных задач!",
        )
    else:
        bot.send_message(
            chat_id=chat_id,
            text="Твои задачи: \n(выбери чтобы пометить как выполненное)",
            reply_markup=generate_menu_task(tasks),
        )


def start_bot():
    @bot.message_handler(commands=["start"])
    def start_message(message):
        User.create(message.chat.id)
        send_start_menu(chat_id=message.chat.id)

    @bot.message_handler(commands=["menu"])
    def show_menu(message):
        send_start_menu(chat_id=message.chat.id)

    # Хендлер обрабатывающий callback от нажатия кнопок
    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        if call.data == "create":
            bot.send_message(call.message.chat.id, "Введи задачу которую хочешь выполнить")
            bot.register_next_step_handler(call.message, create_task)
        elif call.data == "show":
            send_tasks(call.message.chat.id)
        elif call.data.startswith("closetask"):
            number_of_task = int(call.data.split("#")[1])
            close_task(number_of_task)
            bot.send_message(call.message.chat.id, f"Вы выполнили задачу {Task.get_task_by_id(number_of_task)}")
            send_tasks(call.message.chat.id)
        elif call.data == "back":
            send_start_menu(call.message.chat.id)

    bot.polling(True, interval=0)


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
    bot.send_message(message.chat.id, f"Создана задача: {Task.get_task_by_id(task_id)} в {hour}:{minute}")
    send_tasks(message.chat.id)