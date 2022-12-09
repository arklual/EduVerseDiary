from api.settings import *
import requests
from bs4 import BeautifulSoup

class Student:
    def __init__(self, name, id):
        self.name = name
        self.id = id
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


class School33Api:   
    def __init__(self, skip_update_marks=False):
        self.__session = self.__sign_in()
        self.__students = self.__get_students()
        self.__add_english_group()
        self.__add_physical_edu_group()
        if not skip_update_marks:
            self.__add_marks()
    
    @property
    def students(self):
        return self.__students

    def update_marks(self):
        for i in range(len(self.__students)):
            self.__students[i].subjects = []
        self.__session = self.__sign_in()
        self.__add_marks()

    def __sign_in(self):
        cookies = self.__get_cookies(csrf='FWMzTtfR8HLWYpVPocTgTZabxfztyUoanUrKdk6yBuGy85YKuvJ0SyYAbLzP2lLM', subject_id='272')
        data = {
            'csrfmiddlewaretoken': 'W2IsoDfkAYxbL5NgnoBwLYDHgaR86JqhE0nDIu613LsNVLQbtHrgKxr6UGRuAaNT',
            'next': '/',
            'username': USERNAME,
            'password': PASSWORD,
            'submit': '\u0412\u043E\u0439\u0442\u0438',
        }
        headers = self.__get_headers('http://93.181.225.54/accounts/login/?next=/')
        ses = requests.session()
        ses.post('http://93.181.225.54/accounts/login/', headers=headers,cookies=cookies, data=data, verify=False)
        return ses

    def __get_students(self):
        students = []
        cookies = self.__get_cookies(csrf = 'yryiF3SDU9Ubj3WCXsQmayNnTNR6zRWINmaAajUgek0JNq2rqlpXyr2QPQ8StUhj', subject_id='3')
        headers = self.__get_headers('http://93.181.225.54/educ_proc/ep_marks/')
        response = self.__session.get('http://93.181.225.54/educ_proc/ep_marks/',
                            headers=headers, cookies=cookies, verify=False)
        soup = BeautifulSoup(response.text, features='html.parser')
        print('Adding students')
        user_rows = soup.find_all('div', {'id': 'user-rows'})
        users = user_rows[1].find_all('div')
        for user in users:
            students.append(Student(user.text.strip(), user.get('name')[1:]))
        return students

    def __add_marks(self):
        for subject in SUBJECTS:
            cookies = self.__get_cookies(csrf='yryiF3SDU9Ubj3WCXsQmayNnTNR6zRWINmaAajUgek0JNq2rqlpXyr2QPQ8StUhj', subject_id=subject['id'])
            headers = self.__get_headers('http://93.181.225.54/educ_proc/ep_marks/')
            response = self.__session.get('http://93.181.225.54/educ_proc/ep_marks/',
                                headers=headers, cookies=cookies, verify=False)

            soup = BeautifulSoup(response.text, features='html.parser')
            print('Parsing', subject['name'])
            marks = soup.find_all('div', {'class': 'mark-row'})
            if(len(marks) > COUNT_OF_STUDENTS):
                for i in range(len(self.__students)):
                    sub = Subject(marks[i].text.strip(), subject['name'])
                    self.__students[i].subjects.append(sub)
                    marks_row = marks[i+COUNT_OF_STUDENTS].text.strip().split('\n')
                    for m in marks_row:
                        if m == '1' or m == '2' or m == '3' or m == '4' or m == '5':
                            sub.marks.append(int(m))
        self.__add_english_info_marks()
        self.__add_physical_edu_marks()

    def __add_english_group(self):
        students_en = []
        cookies = self.__get_cookies(csrf='yryiF3SDU9Ubj3WCXsQmayNnTNR6zRWINmaAajUgek0JNq2rqlpXyr2QPQ8StUhj', subject_id='202', class_id=SUBJECTS_ENGLISH_1[0]['class_id'])
        cookies['group_type_id'] = '10'
        headers = self.__get_headers('http://93.181.225.54/educ_proc/ep_marks/')
        response = self.__session.get('http://93.181.225.54/educ_proc/ep_marks/',
                            headers=headers, cookies=cookies, verify=False)
        soup = BeautifulSoup(response.text, features='html.parser')
        print('Adding english group')
        user_rows = soup.find_all('div', {'id': 'user-rows'})
        users = user_rows[1].find_all('div')
        for user in users:
            students_en.append(Student(user.text.strip(), user.get('name')[1:]))
        for i in range(len(self.__students)):
            for en in students_en:
                if self.__students[i].id == en.id:
                    self.__students[i].english_group = 1
    
    def __add_physical_edu_group(self):
        students_phys = []
        cookies = self.__get_cookies(csrf='lCpU6QYoV8eqoobwOthwm6n6G8IjzFdBL3jEXSuVFip83aVi02gUxI5WgchUvbJC', subject_id='32', class_id=SUBJECTS_PHYS_EDU_1['class_id'])
        cookies['group_type_id'] = '10'
        headers = self.__get_headers('http://93.181.225.54/educ_proc/ep_marks/')
        response = self.__session.get('http://93.181.225.54/educ_proc/ep_marks/',
                            headers=headers, cookies=cookies, verify=False)
        soup = BeautifulSoup(response.text, features='html.parser')
        print('Adding physical education group')
        user_rows = soup.find_all('div', {'id': 'user-rows'})
        users = user_rows[1].find_all('div')
        for user in users:
            students_phys.append(Student(user.text.strip(), user.get('name')[1:]))
        for i in range(len(self.__students)):
            for ph in students_phys:
                if self.__students[i].id == ph.id:
                    self.__students[i].physical_edu_group = 1

    def __add_english_info_marks(self):
        students_en_1 = []
        students_en_2 = []
        petrov = ''
        for student in self.__students:
            if student.english_group == 1 and 'Петров' not in student.name:
                students_en_1.append(student)
            elif student.english_group == 0:
                students_en_2.append(student)
            elif 'Петров' in student.name:
                petrov = student
        students_en_1.append(petrov)


        for subject in SUBJECTS_ENGLISH_2:
            cookies = self.__get_cookies(csrf = 'yryiF3SDU9Ubj3WCXsQmayNnTNR6zRWINmaAajUgek0JNq2rqlpXyr2QPQ8StUhj', class_id=subject["class_id"], subject_id=subject["id"])
            cookies['group_type_id'] = '10'
            headers = self.__get_headers(referer='http://93.181.225.54/educ_proc/ep_marks/')
            response = self.__session.get('http://93.181.225.54/educ_proc/ep_marks/',
                                headers=headers, cookies=cookies, verify=False)
            soup = BeautifulSoup(response.text, features='html.parser')
            print('Parsing', subject['name'])
            marks = soup.find_all('div', {'class': 'mark-row'})
            if(len(marks) >= len(students_en_2)+COUNT_OF_STUDENTS_IN_ENGLISH_GROUP_2):
                for i in range(len(students_en_2)):
                    sub = Subject(marks[i].text.strip(), subject['name'])
                    students_en_2[i].subjects.append(sub)
                    marks_row = marks[i+COUNT_OF_STUDENTS_IN_ENGLISH_GROUP_2].text.strip().split('\n')
                    for m in marks_row:
                        if m == '1' or m == '2' or m == '3' or m == '4' or m == '5':
                            sub.marks.append(int(m))

        for subject in SUBJECTS_ENGLISH_1:
            cookies = self.__get_cookies(csrf = 'yryiF3SDU9Ubj3WCXsQmayNnTNR6zRWINmaAajUgek0JNq2rqlpXyr2QPQ8StUhj', class_id=subject["class_id"], subject_id=subject["id"])
            cookies['group_type_id'] = '10'
            headers = self.__get_headers(referer='http://93.181.225.54/educ_proc/ep_marks/')
            response = self.__session.get('http://93.181.225.54/educ_proc/ep_marks/',
                                headers=headers, cookies=cookies, verify=False)
            soup = BeautifulSoup(response.text, features='html.parser')
            print('Parsing', subject['name'])
            marks = soup.find_all('div', {'class': 'mark-row'})
            if(len(marks) >= len(students_en_1)+COUNT_OF_STUDENTS_IN_ENGLISH_GROUP_1):
                for i in range(len(students_en_1)):
                    sub = Subject(marks[i].text.strip(), subject['name'])
                    students_en_1[i].subjects.append(sub)
                    marks_row = marks[i+COUNT_OF_STUDENTS_IN_ENGLISH_GROUP_1].text.strip().split('\n')
                    for m in marks_row:
                        if m == '1' or m == '2' or m == '3' or m == '4' or m == '5':
                            sub.marks.append(int(m))

        self.__students = sorted(students_en_1+students_en_2)

    def __add_physical_edu_marks(self):
        students_ph_1 = []
        students_ph_2 = []
        petrov = ''
        for student in self.__students:
            if student.physical_edu_group == 1:
                students_ph_1.append(student)
            elif student.physical_edu_group == 0 and 'Петров' not in student.name:
                students_ph_2.append(student)
            elif 'Петров' in student.name:
                petrov = student
        students_ph_2.append(petrov)

        subject = SUBJECTS_PHYS_EDU_2
        cookies = self.__get_cookies(csrf = 'yryiF3SDU9Ubj3WCXsQmayNnTNR6zRWINmaAajUgek0JNq2rqlpXyr2QPQ8StUhj', class_id=subject["class_id"], subject_id=subject["id"])
        cookies['group_type_id'] = '10'
        headers = self.__get_headers(referer='http://93.181.225.54/educ_proc/ep_marks/')
        response = self.__session.get('http://93.181.225.54/educ_proc/ep_marks/',
                            headers=headers, cookies=cookies, verify=False)
        soup = BeautifulSoup(response.text, features='html.parser')
        print('Parsing', subject['name'])
        marks = soup.find_all('div', {'class': 'mark-row'})
        if(len(marks) >= COUNT_OF_STUDENTS_IN_PHYS_EDU_GROUP_2+len(students_ph_2)):
            for i in range(len(students_ph_2)):
                sub = Subject(marks[i].text.strip(), subject['name'])
                students_ph_2[i].subjects.append(sub)
                marks_row = marks[i+COUNT_OF_STUDENTS_IN_PHYS_EDU_GROUP_2].text.strip().split('\n')
                for m in marks_row:
                    if m == '1' or m == '2' or m == '3' or m == '4' or m == '5':
                        sub.marks.append(int(m))

        subject = SUBJECTS_PHYS_EDU_1
        cookies = self.__get_cookies(csrf = 'yryiF3SDU9Ubj3WCXsQmayNnTNR6zRWINmaAajUgek0JNq2rqlpXyr2QPQ8StUhj', class_id=subject["class_id"], subject_id=subject["id"])
        cookies['group_type_id'] = '10'
        headers = self.__get_headers(referer='http://93.181.225.54/educ_proc/ep_marks/')
        response = self.__session.get('http://93.181.225.54/educ_proc/ep_marks/',
                            headers=headers, cookies=cookies, verify=False)
        soup = BeautifulSoup(response.text, features='html.parser')
        print('Parsing', subject['name'])
        marks = soup.find_all('div', {'class': 'mark-row'})
        if(len(marks) >= len(students_ph_1)+COUNT_OF_STUDENTS_IN_PHYS_EDU_GROUP_1):
            for i in range(len(students_ph_1)):
                sub = Subject(marks[i].text.strip(), subject['name'])
                students_ph_1[i].subjects.append(sub)
                marks_row = marks[i+COUNT_OF_STUDENTS_IN_PHYS_EDU_GROUP_1].text.strip().split('\n')
                for m in marks_row:
                    if m == '1' or m == '2' or m == '3' or m == '4' or m == '5':
                        sub.marks.append(int(m))

        self.__students = sorted(students_ph_1+students_ph_2)

    def __get_cookies(self, csrf, subject_id, class_id = CLASS_ID):
        cookies = {
            'class_id': str(class_id),
            'period': str(PERIOD_ID),
            'group_type_id': '1',
            'csrftoken': str(csrf),
            'subject_id': str(subject_id),
        }
        return cookies

    def __get_headers(self, referer):
        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'http://93.181.225.54',
            'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': str(referer),
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        return headers
