from api.settings import *
import requests
from bs4 import BeautifulSoup

class Student:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.subjects = []
        self.english_group = 0

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


class School33Api:    
    def __init__(self):
        self.__session = self.__sign_in()
        self.__students = self.__get_students()
        self.__add_english_group()
        self.__add_marks()
    
    @property
    def students(self):
        return self.__students

    def update_marks(self):
        for i in range(len(self.__students)):
            self.__students[i].subjects = []
        self.__add_marks()

    def __sign_in(self):
        __cookies = {
            'csrftoken': 'FWMzTtfR8HLWYpVPocTgTZabxfztyUoanUrKdk6yBuGy85YKuvJ0SyYAbLzP2lLM',
            'class_id': CLASS_ID,
            'period': PERIOD_ID,
            'subject_id': '272',
            'group_type_id': '1',
        }
        __headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'http://93.181.225.54',
            'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'http://93.181.225.54/accounts/login/?next=/',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        __data = {
            'csrfmiddlewaretoken': 'W2IsoDfkAYxbL5NgnoBwLYDHgaR86JqhE0nDIu613LsNVLQbtHrgKxr6UGRuAaNT',
            'next': '/',
            'username': USERNAME,
            'password': PASSWORD,
            'submit': '\u0412\u043E\u0439\u0442\u0438',
        }
        ses = requests.session()
        ses.post('http://93.181.225.54/accounts/login/', headers=self.__headers,cookies=self.__cookies, data=self.__data, verify=False)
        return ses

    def __get_students(self):
        students = []
        cookies = {
            'class_id': CLASS_ID,
            'period': PERIOD_ID,
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
        response = self.__session.get('http://93.181.225.54/educ_proc/ep_marks/',
                            headers=headers, cookies=cookies, verify=False)
        soup = BeautifulSoup(response.text)
        user_rows = soup.find_all('div', {'id': 'user-rows'})
        users = user_rows[1].find_all('div')
        for user in users:
            students.append(Student(user.text.strip(), user.get('name')[1:]))
        return students

    def __add_marks(self):
        for subject in SUBJECTS:
            cookies = {
                'class_id': CLASS_ID,
                'period': PERIOD_ID,
                'group_type_id': '1',
                'csrftoken': 'yryiF3SDU9Ubj3WCXsQmayNnTNR6zRWINmaAajUgek0JNq2rqlpXyr2QPQ8StUhj',
                'subject_id': f'{subject["id"]}',
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
            response = self.__session.get('http://93.181.225.54/educ_proc/ep_marks/',
                                headers=headers, cookies=cookies, verify=False)

            soup = BeautifulSoup(response.text)
            marks = soup.find_all('div', {'class': 'mark-row'})
            if(len(marks) > COUNT_OF_STUDENTS):
                for i in range(len(self.__students)):
                    sub = Subject(marks[i].text.strip(), subject['name'])
                    self.__students[i].subjects.append(sub)
                    marks_row = marks[i+COUNT_OF_STUDENTS].text.strip().split('\n')
                    for m in marks_row:
                        if m == '1' or m == '2' or m == '3' or m == '4' or m == '5' or m == '+':
                            sub.marks.append(int(m))
            self.add_english_info_marks()

    def __add_english_group(self):
        students_en = []
        cookies = {
            'class_id': CLASS_ID,
            'period': PERIOD_ID,
            'group_type_id': '1',
            'csrftoken': 'yryiF3SDU9Ubj3WCXsQmayNnTNR6zRWINmaAajUgek0JNq2rqlpXyr2QPQ8StUhj',
            'subject_id': '202',
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
        response = self.__session.get('http://93.181.225.54/educ_proc/ep_marks/',
                            headers=headers, cookies=cookies, verify=False)
        soup = BeautifulSoup(response.text)
        user_rows = soup.find_all('div', {'id': 'user-rows'})
        users = user_rows[1].find_all('div')
        for user in users:
            students_en.append(Student(user.text.strip(), user.get('name')[1:]))
        for i in range(len(self.__students)):
            for en in students_en:
                if self.__students[i].id == en.id:
                    self.__students[i].english_group = 1

    def add_english_info_marks(self):
        students_en_1 = []
        students_en_2 = []
        for student in self.__students:
            if student.english_group == 1:
                students_en_1.append(student)
            elif student.english_group == 0:
                students_en_2.append(student)

        for subject in SUBJECTS_ENGLISH_2:
            cookies = {
                'class_id': f'{subject["class_id"]}',
                'period': 'p_114',
                'group_type_id': '1',
                'csrftoken': 'yryiF3SDU9Ubj3WCXsQmayNnTNR6zRWINmaAajUgek0JNq2rqlpXyr2QPQ8StUhj',
                'subject_id': f'{subject["id"]}',
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
            response = self.__session.get('http://93.181.225.54/educ_proc/ep_marks/',
                                headers=headers, cookies=cookies, verify=False)
            soup = BeautifulSoup(response.text)
            marks = soup.find_all('div', {'class': 'mark-row'})
            if(len(marks) > 5):
                for i in range(len(students_en_2)):
                    sub = Subject(marks[i].text.strip(), subject['name'])
                    students_en_2[i].subjects.append(sub)
                    marks_row = marks[i+COUNT_OF_STUDENTS_IN_ENGLISH_GROUP_2].text.strip().split('\n')
                    for m in marks_row:
                        if m == '1' or m == '2' or m == '3' or m == '4' or m == '5' or m == '+':
                            sub.marks.append(int(m))

        for subject in SUBJECTS_ENGLISH_1:
            cookies = {
                'class_id': f'{subject["class_id"]}',
                'period': 'p_114',
                'group_type_id': '1',
                'csrftoken': 'yryiF3SDU9Ubj3WCXsQmayNnTNR6zRWINmaAajUgek0JNq2rqlpXyr2QPQ8StUhj',
                'subject_id': f'{subject["id"]}',
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
            response = self.__session.get('http://93.181.225.54/educ_proc/ep_marks/',
                                headers=headers, cookies=cookies, verify=False)
            soup = BeautifulSoup(response.text)
            marks = soup.find_all('div', {'class': 'mark-row'})
            if(len(marks) > 5):
                for i in range(len(students_en_1)):
                    sub = Subject(marks[i].text.strip(), subject['name'])
                    students_en_1[i].subjects.append(sub)
                    marks_row = marks[i+COUNT_OF_STUDENTS_IN_ENGLISH_GROUP_1].text.strip().split('\n')
                    for m in marks_row:
                        if m == '1' or m == '2' or m == '3' or m == '4' or m == '5' or m == '+':
                            sub.marks.append(int(m))

        self.__students = sorted(students_en_1+students_en_2)


    