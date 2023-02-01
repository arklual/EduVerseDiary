from aiogram import types

def main():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Оценки")
    keyboard.add("Домашнее задание")
    keyboard.add("Расписание звонков")
    keyboard.add("Конспекты")
    return keyboard