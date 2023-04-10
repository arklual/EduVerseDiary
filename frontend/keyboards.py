from aiogram import types

def main(is_admin = False):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("🧮 Оценки")
    keyboard.add("📚 Домашнее задание")
    keyboard.add("⏰ Расписание звонков")
    keyboard.add("📒 Конспекты")
    keyboard.add("📒 Зачёт (геометрия)")
    if is_admin:
        keyboard.add('Загрузить д/з')
    return keyboard