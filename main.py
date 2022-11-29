import requests
from bs4 import BeautifulSoup
from settings import *
from student import *
import telebot

def sign_in():
    cookies = {
        'csrftoken': 'FWMzTtfR8HLWYpVPocTgTZabxfztyUoanUrKdk6yBuGy85YKuvJ0SyYAbLzP2lLM',
        'class_id': '3962',
        'period': 'p_114',
        'subject_id': '272',
        'group_type_id': '1',
    }
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'http://93.181.225.54',
        'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://93.181.225.54/accounts/login/?next=/',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'csrftoken=FWMzTtfR8HLWYpVPocTgTZabxfztyUoanUrKdk6yBuGy85YKuvJ0SyYAbLzP2lLM; class_id=3962; period=p_114; subject_id=272; group_type_id=1',
    }
    data = {
        'csrfmiddlewaretoken': 'W2IsoDfkAYxbL5NgnoBwLYDHgaR86JqhE0nDIu613LsNVLQbtHrgKxr6UGRuAaNT',
        'next': '/',
        'username': '03326174',
        'password': '747698',
        'submit': '\u0412\u043E\u0439\u0442\u0438',
    }
    ses = requests.session()
    ses.post('http://93.181.225.54/accounts/login/', headers=headers,
             cookies=cookies, data=data, verify=False)
    return ses


def get_students(session):
    students = []
    cookies = {
        'class_id': '3962',
        'period': 'p_114',
        'group_type_id': '1',
        'csrftoken': 'yryiF3SDU9Ubj3WCXsQmayNnTNR6zRWINmaAajUgek0JNq2rqlpXyr2QPQ8StUhj',
        'subject_id': '3',
    }
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://93.181.225.54/educ_proc/ep_marks/',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    response = session.get('http://93.181.225.54/educ_proc/ep_marks/',
                           headers=headers, cookies=cookies, verify=False)
    soup = BeautifulSoup(response.text)
    user_rows = soup.find_all('div', {'id': 'user-rows'})
    users = user_rows[1].find_all('div')
    for user in users:
        students.append(Student(user.text.strip(), user.get('name')[1:]))
    return students

bot = telebot.TeleBot("5099099475:AAHNWwVNOoPR6oPELEntSy3UMlv8y2EZTTI", parse_mode='HTML')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Добро пожаловать. Для получения оценок введите /marks')
    
@bot.message_handler(commands=['marks'])
def get_lastname(message):
    msg1 = bot.send_message(message.chat.id, 'Введите вашу фамилию')
    bot.register_next_step_handler(msg1, send_marks)

def send_marks(message):
    last_name = message.text
    bot.send_message(message.chat.id, 'Загружаем Ваши отметки, подождите(процесс может занять 1 минуту)')
    session = sign_in()
    students = get_students(session)
    students = add_english_group(session, students)
    students = add_math_group(session, students)
    students = add_marks(session, SUBJECTS, students)
    students = add_english_info_marks(
        session, SUBJECTS_ENGLISH_1, SUBJECTS_ENGLISH_2, students)
    students = add_math_marks(session, SUBJECTS_MATH_1, SUBJECTS_MATH_2, students)
    
    for st in students:
        if st.name.split(' ')[1] == last_name:
            bot.send_message(message.chat.id, 'Ваши оценки:')
            for subject in st.subjects:
                bot.send_message(message.chat.id, f'{subject.name} {subject.average_mark} {subject.marks}')

bot.polling(none_stop=True, interval=0)