from aiogram import types
import datetime

def main():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Оценки")
    keyboard.add("Домашнее задание")
    keyboard.add("Расписание звонков")
    keyboard.add("Конспекты")
    return keyboard

def week():
    WEEKDAYS = [
        'Понедельник',
        'Вторник',
        'Среда',
        'Четверг',
        'Пятница',
        'Суббота',
        'Воскресенье',
    ]

    weekday = datetime.date.today().weekday()
    buttons = []
    if weekday != 6:
        buttons.append(types.InlineKeyboardButton('Сегодня', callback_data=f'homework{weekday}'))
    if weekday == 5 or weekday == 6:
        for i in range(6):
            buttons.append(types.InlineKeyboardButton(WEEKDAYS[i], callback_data=f'homework{i}'))
    else:
        for i in range(weekday+1, 6):
            buttons.append(types.InlineKeyboardButton(WEEKDAYS[i], callback_data=f'homework{i}'))
    inline_kb1 = types.InlineKeyboardMarkup().add(*buttons)
    return inline_kb1