from loguru import logger
from botapp.models import Task
from .bot import bot
from .generate_keyboards import generate_start_menu, generate_menu_task


# Генерируем стартовое меню и шлём его в сообщении
def send_start_menu(chat_id: int):
    start_menu = generate_start_menu(chat_id)
    bot.send_message(chat_id=chat_id, text="Выберите нужный пункт:", reply_markup=start_menu)

# Отправляем уведомление о необходимости выполнения задачи
def send_notification(telegram_id: int, text: str):
    bot.send_message(telegram_id, text)


# Закрываем/завершаем задачу
def close_task(task_id: int):
    Task.close_task(task_id)


# Отправляем список задач по юзеру
def send_tasks(chat_id: int):
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
