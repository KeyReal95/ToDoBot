from botapp.models import User, Task
from .create_task import create_task
from .sends import send_start_menu, send_tasks, close_task
from .bot import bot


@bot.message_handler(commands=["start"])
def start_message(message):
    User.create(message.chat.id)
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