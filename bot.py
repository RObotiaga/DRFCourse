from datetime import datetime, timedelta

import telebot
from telebot import types
from decouple import config
import requests
import json
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

bot = telebot.TeleBot(config('TELEBOT_API'))
api_url = 'http://localhost:8000'
user_input = {
    'Время выполнения': '00:02:00',
    'Периодичность': '00:20:00'
}
habits_id = []


def get_refresh_token(user_id):
    with open('users.json') as f:
        data = json.load(f).get(str(user_id))
        if data:
            return data
        else:
            raise ValueError('Не зарегистрирован')


def save_refresh_token(user_id, token):
    try:
        with open('users.json', 'r') as infile:
            data = json.load(infile)
    except FileNotFoundError:
        data = {}

    if user_id in data:
        data[user_id] = token
    else:
        data[user_id] = token

    with open('users.json', 'w') as outfile:
        json.dump(data, outfile)


@bot.message_handler(commands=['start', 'register'])
def handle_start(message):
    try:
        refresh = get_refresh_token(message.chat.id)
        response = requests.post(f'{api_url}/token/refresh/', data={'refresh': refresh})
        if response.status_code == 200:

            main_process(message)
        else:
            bot.send_message(message.chat.id, "Произошла ошибка, повторите позднее")
    except Exception as e:
        bot.send_message(message.chat.id, "Привет, придумай пароль и отправь его мне чтобы зарегистрироваться!")
        bot.register_next_step_handler(message, process_password_step)
        print(e)


def process_password_step(message):
    user_data = {
        'user_id': message.chat.id,
        'password': message.text,
    }
    response = requests.post(f'{api_url}/register/', data=user_data)
    print(response.content.decode('utf-8'))
    if response.status_code == 201:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        user_habit = types.KeyboardButton("Мои привычки")
        create_habit = types.KeyboardButton("Создать привычку")
        markup.add(user_habit, create_habit)
        bot.send_message(message.chat.id, "Вы зарегистрированы", reply_markup=markup)
        response = requests.post(f'{api_url}/token/', data=user_data)
        save_refresh_token(message.chat.id, response.json()['refresh'])
        main_process(message)
    elif response.json()['user_id'] == ['пользователь с таким ид пользователя уже существует.']:
        response = requests.post(f'{api_url}/token/', data=user_data)
        save_refresh_token(message.chat.id, response.json()['refresh'])
        main_process(message)
    else:
        print(response.json()['user_id'])
        bot.send_message(message.chat.id, "Произошла ошибка, повторите позднее")


def get_user_habit(user_id):
    refresh = get_refresh_token(user_id)
    refresh_response = requests.post(f'{api_url}/token/refresh/', data={'refresh': refresh})
    headers = {
        "Authorization": f"Bearer {refresh_response.json()['access']}",
    }
    access_response = requests.get(f'{api_url}/user/habits/', headers=headers)
    return access_response.json()


def main_process(message):
    habits_keyboard = types.InlineKeyboardMarkup(row_width=1)
    habits = get_user_habit(message.chat.id)['results']
    if habits:
        for habit in habits:
            time_str = habit['time']
            action = types.InlineKeyboardButton(text=habit['action'].capitalize(),
                                                callback_data=f"habit {habit['id']}")
            time_obj = datetime.fromisoformat(time_str[:-6]) - timedelta(hours=int(time_str[-6:][:3]),
                                                                         minutes=int(time_str[-6:][4:]))
            normal_time = time_obj.strftime('%Y-%m-%d %H:%M:%S')
            time = types.InlineKeyboardButton(text=normal_time, callback_data=f"habit {habit['id']}")
            habits_keyboard.row(action, time)
    else:
        no_habits = types.InlineKeyboardButton(text='Нет созданных привычек',
                                               callback_data="not clickable")
        habits_keyboard.add(no_habits)
    bot.send_message(message.chat.id, "Мои привычки:", reply_markup=habits_keyboard, )


def create_habit_edit_menu(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    fields = ["Время", "Место", "Действие", "Приятная привычка", "Связанная привычка", "Периодичность",
              "Вознаграждение", "Время выполнения", "Публичность", "Приятность"]
    for field in fields:
        name = types.InlineKeyboardButton(text=field.capitalize(), callback_data=field)
        value = types.InlineKeyboardButton(text=user_input.get(field, ''), callback_data=field)
        keyboard.row(name, value)
    save = types.InlineKeyboardButton(text='Сохранить', callback_data='save_habit')
    keyboard.row(save)
    bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id,
                                  reply_markup=keyboard)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text("Введите время формата HH:MM",
                              c.message.chat.id,
                              c.message.message_id)
        bot.register_next_step_handler(c.message, lambda msg: save_user_time_input(msg, 'Время', c, result))


@bot.message_handler(content_types=['text'])
def func(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_habit = types.KeyboardButton("Мои привычки")
    create_habit = types.KeyboardButton("Создать привычку")
    markup.add(user_habit, create_habit)
    if message.text == 'Мои привычки':
        habits_keyboard = types.InlineKeyboardMarkup(row_width=2)
        habits = get_user_habit(message.chat.id)['results']

        for habit in habits:
            time_str = habit['time']
            action = types.InlineKeyboardButton(text=habit['action'].capitalize(),
                                                callback_data=f"habit {habit['id']}")
            time_obj = datetime.fromisoformat(time_str[:-6]) - timedelta(hours=int(time_str[-6:][:3]),
                                                                         minutes=int(time_str[-6:][4:]))
            normal_time = time_obj.strftime('%Y-%m-%d %H:%M:%S')
            time = types.InlineKeyboardButton(text=normal_time, callback_data='not clickable')
            habits_keyboard.row(action, time)
        bot.send_message(message.chat.id, "Выберите поле для ввода:", reply_markup=habits_keyboard)
    elif message.text == 'Создать привычку':
        habits = get_user_habit(message.chat.id)['results']
        for i in habits:
            habits_id.append(i['id'])
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        fields = ["Время", "Место", "Действие", "Приятная привычка", "Связанная привычка", "Периодичность",
                  "Вознаграждение", "Время выполнения", "Публичность", "Приятность"]
        for field in fields:
            name = types.InlineKeyboardButton(text=field.capitalize(), callback_data=field)
            value = types.InlineKeyboardButton(text=user_input.get(field, ''), callback_data=field)
            keyboard.row(name, value)
        save = types.InlineKeyboardButton(text='Сохранить', callback_data='save_habit')
        keyboard.row(save)

        bot.send_message(message.chat.id, "Выберите поле для ввода:", reply_markup=keyboard)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        user_habit = types.KeyboardButton("Мои привычки")
        create_habit = types.KeyboardButton("Создать привычку")
        markup.add(user_habit, create_habit)
        bot.send_message(message.chat.id, "Вы зарегистрированы", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    field = call.data
    if call.data in ['Место', 'Действие', 'Вознаграждение']:
        bot.answer_callback_query(callback_query_id=call.id, text=f"Введите значение для поля {field.capitalize()}:")
        bot.register_next_step_handler(call.message, lambda msg: save_user_text_input(msg, field, call))
    elif call.data in ['Периодичность', 'Время выполнения']:
        bot.answer_callback_query(callback_query_id=call.id, text="Введите значение для поля HH:MM:SS")
        bot.register_next_step_handler(call.message, lambda msg: save_user_duration_input(msg, field, call))
    elif call.data == 'Публичность':
        keyboard2 = types.InlineKeyboardMarkup(row_width=2)
        fields = ["Публичная", "Непубличная"]
        for inline_field in fields:
            button = types.InlineKeyboardButton(text=inline_field.capitalize(), callback_data=inline_field)
            keyboard2.add(button)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=keyboard2)
    elif call.data in ['Публичная', 'Непубличная']:
        user_input['Публичность'] = call.data
        create_habit_edit_menu(call.message)
    elif call.data == 'Приятность':
        keyboard2 = types.InlineKeyboardMarkup(row_width=2)
        fields = ["Приятная", "Обычная"]
        for inline_field in fields:
            button = types.InlineKeyboardButton(text=inline_field.capitalize(), callback_data=inline_field)
            keyboard2.add(button)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=keyboard2)
    elif call.data in ['Приятная', 'Обычная']:
        user_input['Приятность'] = call.data
        create_habit_edit_menu(call.message)
    elif call.data in ['Приятная привычка', 'Связанная привычка']:

        habits_keyboard = types.InlineKeyboardMarkup(row_width=2)
        habits = get_user_habit(call.from_user.id)['results']

        for habit in habits:
            time_str = habit['time']
            action = types.InlineKeyboardButton(text=habit['action'].capitalize(),
                                                callback_data=f"choose {habit['id']} {call.data}")
            time_obj = datetime.fromisoformat(time_str[:-6]) - timedelta(hours=int(time_str[-6:][:3]),
                                                                         minutes=int(time_str[-6:][4:]))
            normal_time = time_obj.strftime('%Y-%m-%d %H:%M:%S')
            time = types.InlineKeyboardButton(text=normal_time, callback_data='not clickable')
            habits_keyboard.row(action, time)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=habits_keyboard)
    elif 'choose' in call.data:
        habit_id = call.data.split()[1]
        habit_type_call = f'{call.data.split()[2]} {call.data.split()[3]}'
        user_input[habit_type_call] = habit_id
        bot.answer_callback_query(callback_query_id=call.id, text="Значение поля сохранено")
        create_habit_edit_menu(call.message)
    elif call.data == 'Время':
        calendar, step = DetailedTelegramCalendar().build()
        bot.edit_message_text(f"Select {LSTEP[step]}", chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=calendar)
    elif call.data == 'save_habit':
        if not user_input.get('Время', ) or not user_input.get('Место', ) or not user_input.get('Действие', ):
            bot.send_message(call.message.chat.id, 'Есть незаполненные поля')
            return
        refresh = get_refresh_token(call.message.chat.id)
        refresh_response = requests.post(f'{api_url}/token/refresh/', data={'refresh': refresh})
        headers = {
            "Authorization": f"Bearer {refresh_response.json()['access']}",
        }
        user_data = {
            'time': datetime.strptime(user_input.get('Время', ), "%H:%M %Y-%m-%d").strftime("%Y-%m-%dT%H:%M"),
            'place': user_input.get('Место', ),
            'action': user_input.get('Действие', ),
            'treasure': user_input.get('Вознаграждение', ),
            'public': user_input.get('Публичность', ),
            'duration': user_input.get('Время выполнения', ),
            'pleasant_habit': user_input.get('Приятная привычка', ),
            'frequency': user_input.get('Периодичность', ),
            'pleasantness': user_input.get('Приятность', ),
            'related_habit': user_input.get('Связанная привычка', ),
        }
        response = requests.post(f'{api_url}/habits/', data=user_data, headers=headers)
        if response.status_code == 201:
            bot.send_message(call.message.chat.id, 'Привычка создана')
        print(json.loads(response.content.decode('utf-8')))


def save_user_text_input(message, field, call):
    user_input[field] = message.text
    create_habit_edit_menu(call.message)


def save_user_duration_input(message, field, call):
    try:
        if field in ['Время выполнения', 'Периодичность']:
            delta_format = "%H:%M:%S" if field == 'Время выполнения' else "%d %H:%M:%S"
            time = datetime.strptime(message.text, delta_format)

            if (field == 'Время выполнения' and time.minute > 2) or (field == 'Периодичность' and time.day > 7):
                error_message = 'Длительность не может быть больше 2 минут' if field == 'Время выполнения' else 'Периодичность не может быть больше 7 дней'
                bot.send_message(message.chat.id, error_message)
                bot.register_next_step_handler(call.message, lambda msg: save_user_duration_input(msg, field, call))
                return
            else:
                user_input[field] = message.text
                create_habit_edit_menu(call.message)

    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Неверный формат времени, попробуйте еще раз')
        bot.register_next_step_handler(call.message, lambda msg: save_user_duration_input(msg, field, call))


def save_user_time_input(message, field, call, date):
    try:
        datetime.strptime(f'{message.text} {date}', "%H:%M %Y-%m-%d").strftime("%Y-%m-%dT%H:%M")
        user_input[field] = f'{message.text} {date}'
        create_habit_edit_menu(call.message)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Неверный формат времени, попробуйте еще раз')
        bot.register_next_step_handler(message, lambda msg: save_user_time_input(msg, field, call, date))
        return


bot.infinity_polling()
