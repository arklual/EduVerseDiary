from aiogram import types
import datetime

def subjects(notes):
    buttons = []
    subjects = []
    for note in notes:
        subject = note.subject
        if subject not in subjects:
            subjects.append(subject)
            buttons.append(types.InlineKeyboardButton(subject, callback_data=f'subject{subject}'))
    return types.InlineKeyboardMarkup().add(*buttons)