import requests
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from edutypes import Mark
from backend.databases.database import Database
from progress.bar import Bar
CLASS_ID = '4180'
PERIOD_ID = 'p_119'
USERNAME = '0339434'
PASSWORD = '181230'

class EduDiaryAPI:
    def __init__(self, login=USERNAME, password=PASSWORD) -> None:
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
        }
        data = {
            'csrfmiddlewaretoken': 'W2IsoDfkAYxbL5NgnoBwLYDHgaR86JqhE0nDIu613LsNVLQbtHrgKxr6UGRuAaNT',
            'next': '/',
            'username': login,
            'password': password,
            'submit': '\u0412\u043E\u0439\u0442\u0438',
        }
        session.post('http://93.181.225.54/accounts/login/',
                     headers=headers, data=data, cookies=cookies)
        self.__cookies__ = session.cookies.get_dict()

    async def get_marks_in_subject(self, students, subject, class_id=CLASS_ID):
        async with ClientSession(cookies=self.__cookies__) as ses:
            cookies = {
                'class_id': str(class_id),
                'period': str(PERIOD_ID),
                'group_type_id': '1',
                'csrftoken': 'yryiF3SDU9Ubj3WCXsQmayNnTNR6zRWINmaAajUgek0JNq2rqlpXyr2QPQ8StUhj',
                'subject_id': str(subject.id),
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
                soup = BeautifulSoup(await r.text(), features='html.parser')
                marks = soup.find_all('div', {'class': 'mark-row'})
                result = []
                petrov = list(filter(lambda x: x.last_name == 'Петров', students))
                if class_id != CLASS_ID and petrov != []:
                    students.remove(petrov[0])
                    students.append(petrov[0])
                if (len(marks) > len(students)):
                    for i in range(len(students)):
                        marks_row = marks[i+len(students)].text.strip().split('\n')
                        for m in marks_row:
                            if m == '1' or m == '2' or m == '3' or m == '4' or m == '5' or m == '+':
                                mark = Mark(students[i], mark=m, subject=subject)
                                result.append(mark)
                return result
            
async def update_marks():
    db = await Database.setup()
    subjects = await db.get_subjects()
    students = await db.get_students()
    bar = Bar('Getting marks', max=len(subjects))
    marks = []
    for subject in subjects:
        api = EduDiaryAPI()
        if subject.id == '202':
            sts = sorted(students, key=lambda x: x.english_group)
            first = sts[0].english_group
            second = sts[len(sts)-1].english_group
            first = list(filter(lambda x: x.english_group == first, sts))
            second = list(filter(lambda x: x.english_group == second, sts))
            marks.append(await api.get_marks_in_subject(students=first, subject=subject, class_id=first[0].english_group))
            marks.append(await api.get_marks_in_subject(students=second, subject=subject, class_id=second[0].english_group))
        elif subject.id == '31':
            sts = sorted(students, key=lambda x: x.info_group)
            first = sts[0].info_group
            second = sts[len(sts)-1].info_group
            first = list(filter(lambda x: x.info_group == first, sts))
            second = list(filter(lambda x: x.info_group == second, sts))
            marks.append(await api.get_marks_in_subject(students=first, subject=subject, class_id=first[0].info_group))
            marks.append(await api.get_marks_in_subject(students=second, subject=subject, class_id=second[0].info_group))
        elif subject.id == '32':
            sts = sorted(students, key=lambda x: x.gender)
            first = sts[0].gender
            second = sts[len(sts)-1].gender
            first = list(filter(lambda x: x.gender == first, sts))
            second = list(filter(lambda x: x.gender == second, sts))
            marks.append(await api.get_marks_in_subject(students=first, subject=subject, class_id=first[0].gender))
            marks.append(await api.get_marks_in_subject(students=second, subject=subject, class_id=second[0].gender))
        else:
            marks.append(await api.get_marks_in_subject(students=students, subject=subject))
        bar.next()
    bar.finish()
    await db.remove_marks()
    await db.reset_marks_ids()
    bar = Bar('Appending new marks', max=len(marks))
    for mark_row in marks:
        for mark in mark_row:
            await db.add_mark(mark, commit=False)
        bar.next()
    await db.commit()
    bar.finish()
    await db.close_connection()
    return marks