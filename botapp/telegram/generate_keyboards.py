from telebot import types
from loguru import logger

#В данный модуль вынесена генерация различных меню, кнопок, задач
def generate_announce_menu():
    yes_button = types.InlineKeyboardButton("Да", callback_data="YES")
    no_button = types.InlineKeyboardButton("Нет", callback_data="NO")
    markup = types.InlineKeyboardMarkup()
    markup.row(yes_button, no_button)
    return markup


def generate_start_menu():
    create_task_btn = types.InlineKeyboardButton("Создать задачу", callback_data="create")
    show_tasks_btn = types.InlineKeyboardButton("Просмотреть задачи", callback_data="show")
    markup = types.InlineKeyboardMarkup()
    markup.row(create_task_btn, show_tasks_btn)
    return markup


def generate_menu_task(tasks: list):
    markup_tasks = types.InlineKeyboardMarkup()
    for task in tasks:
        button = types.InlineKeyboardButton(task.name, callback_data=f"closetask#{task.id}", )
        markup_tasks.add(button)
    logger.info("сформирован список задач")
    return markup_tasks