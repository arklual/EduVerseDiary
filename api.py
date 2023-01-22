from aiohttp import ClientSession
import asyncio
import logging
import json
import requests
import requests.sessions
from settings import *
from bs4 import BeautifulSoup

class Student:
    def __init__(self, name):
        self.name = name
        self.subjects = []
        self.english_group = 0
        self.physical_edu_group = 0

    def __str__(self) -> str:
        return f'{self.name}'

    def __lt__(self, other):
        return int(self.name.split('.')[0]) < int(other.name.split('.')[0])

class Subject:
    def __init__(self, aver, name):
        self.average_mark = aver
        self.marks = []
        self.name = name

    def __str__(self) -> str:
        return f'{self.name} {self.average_mark} {self.marks}'


class EduDiaryAPI:
    def __init__(self, login, password, count_of_students) -> None:
        logging.basicConfig(level=logging.INFO, filename="api.log",filemode="w",\
        format="%(asctime)s %(levelname)s %(message)s")
        self.__sign_in__(login, password)

    def __sign_in__(self, login, password):
        session = requests.session()
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
            'username': login,
            'password': password,
            'submit': '\u0412\u043E\u0439\u0442\u0438',
        }
        r = session.post('http://93.181.225.54/accounts/login/', headers=headers, data=data, cookies=cookies)
        self.__cookies__ = session.cookies.get_dict()

    async def request(self, count_of_students, subject_id, class_id = CLASS_ID):
        subject_id = str(subject_id)
        async with ClientSession(cookies=self.__cookies__) as ses:
            cookies = {
            'class_id': str(class_id),
            'period': str(PERIOD_ID),
            'group_type_id': '1',
            'csrftoken': 'yryiF3SDU9Ubj3WCXsQmayNnTNR6zRWINmaAajUgek0JNq2rqlpXyr2QPQ8StUhj',
            'subject_id': str(subject_id),
            }
            headers = {
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Upgrade-Insecure-Requests': '1',
                'Origin': 'http://93.181.225.54',
                'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Referer': 'http://93.181.225.54/educ_proc/ep_marks/',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            }
            async with ses.get('http://93.181.225.54/educ_proc/ep_marks/', cookies=cookies, headers=headers) as r:
                pass

    async def __from_html_to_structure__(self, response, count_of_students):
        soup = BeautifulSoup(response.text, features='html.parser')
        marks = soup.find_all('div', {'class': 'mark-row'})
        if(len(marks) > count_of_students):
            for i in range(count_of_students):
                marks_row = marks[i+count_of_students].text.strip().split('\n')

                sub = Subject(marks[i].text.strip(), subject['name'])
                self.__students__[i].subjects.append(sub)
                for m in marks_row:
                    if m == '1' or m == '2' or m == '3' or m == '4' or m == '5':
                        sub.marks.append(int(m))
    
    async def __add_students__(self, response):
        soup = BeautifulSoup(response.text, features='html.parser')
        users = soup.find_all('div', {'id': 'user-rows'})[1].find_all('div')
        