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

def themes(subject, n):
    buttons = []
    for i in range(n):
        buttons.append(types.InlineKeyboardButton(i+1, callback_data=f'theme{i}|subject{subject}'))
    return types.InlineKeyboardMarkup().add(*buttons)