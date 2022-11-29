from bs4 import BeautifulSoup
from subject import Subject


class Student:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.subjects = []
        self.english_group = 0
        self.math_group = 0

    def __str__(self) -> str:
        return f'{self.name}'

    def __lt__(self, other):
        return int(self.name.split('.')[0]) < int(other.name.split('.')[0])


def add_marks(session, subjects, students):
    for subject in subjects:
        cookies = {
            'class_id': '3962',
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
        response = session.get('http://93.181.225.54/educ_proc/ep_marks/',
                               headers=headers, cookies=cookies, verify=False)

        soup = BeautifulSoup(response.text)
        marks = soup.find_all('div', {'class': 'mark-row'})
        if(len(marks) > 26):
            for i in range(len(students)):
                sub = Subject(marks[i].text.strip(), subject['name'])
                students[i].subjects.append(sub)
                marks_row = marks[i+26].text.strip().split('\n')
                for m in marks_row:
                    if m == '1' or m == '2' or m == '3' or m == '4' or m == '5':
                        sub.marks.append(int(m))
    return students


def add_english_group(session, students):
    students_en = []
    cookies = {
        'class_id': '4278',
        'period': 'p_114',
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
    response = session.get('http://93.181.225.54/educ_proc/ep_marks/',
                           headers=headers, cookies=cookies, verify=False)
    soup = BeautifulSoup(response.text)
    user_rows = soup.find_all('div', {'id': 'user-rows'})
    users = user_rows[1].find_all('div')
    for user in users:
        students_en.append(Student(user.text.strip(), user.get('name')[1:]))
    for i in range(len(students)):
        for en in students_en:
            if students[i].id == en.id:
                students[i].english_group = 1
    return students


def add_math_group(session, students):
    students_math = []
    cookies = {
        'class_id': '4331',
        'period': 'p_114',
        'group_type_id': '1',
        'csrftoken': 'yryiF3SDU9Ubj3WCXsQmayNnTNR6zRWINmaAajUgek0JNq2rqlpXyr2QPQ8StUhj',
        'subject_id': '29',
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
        students_math.append(Student(user.text.strip(), user.get('name')[1:]))
    for i in range(len(students)):
        for math in students_math:
            if students[i].id == math.id:
                students[i].math_group = 1
    return students


def add_english_info_marks(session, subjects_1, subjects_2, students):
    students_en_1 = []
    students_en_2 = []
    for student in students:
        if student.english_group == 1:
            students_en_1.append(student)
        elif student.english_group == 0:
            students_en_2.append(student)

    for subject in subjects_2:
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
        response = session.get('http://93.181.225.54/educ_proc/ep_marks/',
                               headers=headers, cookies=cookies, verify=False)
        soup = BeautifulSoup(response.text)
        marks = soup.find_all('div', {'class': 'mark-row'})
        if(len(marks) > 5):
            for i in range(len(students_en_2)):
                sub = Subject(marks[i].text.strip(), subject['name'])
                students_en_2[i].subjects.append(sub)
                marks_row = marks[i+13].text.strip().split('\n')
                for m in marks_row:
                    if m == '1' or m == '2' or m == '3' or m == '4' or m == '5':
                        sub.marks.append(int(m))

    for subject in subjects_1:
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
        response = session.get('http://93.181.225.54/educ_proc/ep_marks/',
                               headers=headers, cookies=cookies, verify=False)
        soup = BeautifulSoup(response.text)
        marks = soup.find_all('div', {'class': 'mark-row'})
        if(len(marks) > 5):
            for i in range(len(students_en_1)):
                sub = Subject(marks[i].text.strip(), subject['name'])
                students_en_1[i].subjects.append(sub)
                marks_row = marks[i+13].text.strip().split('\n')
                for m in marks_row:
                    if m == '1' or m == '2' or m == '3' or m == '4' or m == '5':
                        sub.marks.append(int(m))

    students = sorted(students_en_1+students_en_2)
    return students


def add_math_marks(session, subjects_1, subjects_2, students):
    students_math_1 = []
    students_math_2 = []
    for student in students:
        if student.math_group == 1:
            students_math_1.append(student)
        elif student.math_group == 0:
            students_math_2.append(student)
    for subject in subjects_2:
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
        response = session.get('http://93.181.225.54/educ_proc/ep_marks/',
                               headers=headers, cookies=cookies, verify=False)

        soup = BeautifulSoup(response.text)
        marks = soup.find_all('div', {'class': 'mark-row'})
        if(len(marks) > 5):
            for i in range(len(students_math_2)):
                sub = Subject(marks[i].text.strip(), subject['name'])
                students_math_2[i].subjects.append(sub)
                marks_row = marks[i+21].text.strip().split('\n')
                for m in marks_row:
                    if m == '1' or m == '2' or m == '3' or m == '4' or m == '5':
                        sub.marks.append(int(m))

    for subject in subjects_1:
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
        response = session.get('http://93.181.225.54/educ_proc/ep_marks/',
                               headers=headers, cookies=cookies, verify=False)
        soup = BeautifulSoup(response.text)
        marks = soup.find_all('div', {'class': 'mark-row'})
        if(len(marks) > 5):
            for i in range(len(students_math_1)):
                sub = Subject(marks[i].text.strip(), subject['name'])
                students_math_1[i].subjects.append(sub)
                marks_row = marks[i+17].text.strip().split('\n')
                for m in marks_row:
                    if m == '1' or m == '2' or m == '3' or m == '4' or m == '5':
                        sub.marks.append(int(m))

    students = sorted(students_math_1+students_math_2)
    return students
