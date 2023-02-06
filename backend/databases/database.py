import aiosqlite
import asyncio
from edutypes.student import Student, Gender, EnglishGroup
from edutypes.mark import Mark

class Database:
    def __init__(self, conn) -> None:
        self.__conn__ = conn

    @staticmethod
    async def setup():
        conn = await aiosqlite.connect('./backend/databases/data.sqlite3')
        return Database(conn)
    
    async def close_db(self):
        await self.__conn__.close()

    async def get_students(self):
        cur = await self.__conn__.execute('SELECT * FROM students')
        sts = await cur.fetchall()
        await cur.close()
        students = []
        for student in sts:
            student = list(student)
            student = Student(telegram_id=student[0],
                            first_name=student[1], 
                            last_name=student[2], 
                            gender=Gender(student[3]), 
                            english_group=EnglishGroup(student[4]))
            students.append(student)
        return students
    
    async def get_student_by_id(self, telegram_id):
        cur = await self.__conn__.execute('SELECT * FROM students WHERE telegram_id = ?', (telegram_id,))
        student = await cur.fetchone()
        await cur.close()
        student = list(student)
        student = Student(telegram_id=student[0],
                        first_name=student[1], 
                        last_name=student[2], 
                        gender=Gender(student[3]), 
                        english_group=EnglishGroup(student[4]))
        return student
    
    async def add_student(self, student):
        student = (student.telegram_id, student.first_name, student.last_name, student.gender.value, student.english_group.value)
        await self.__conn__.execute("INSERT INTO students (telegram_id, first_name, last_name, gender, english_group) VALUES(?, ?, ?, ?, ?);", student)
        await self.__conn__.commit()
    
    async def add_mark(self, mark):
        mark = (mark.student.telegram_id, mark.mark, mark.subject)
        await self.__conn__.execute("INSERT INTO marks (student, mark, subject) VALUES(?, ?, ?);", mark)
        await self.__conn__.commit()
    
    async def get_students_marks(self, student):
        cur = await self.__conn__.execute('SELECT * FROM marks WHERE student = ?', (student.telegram_id,))
        mrks = await cur.fetchall()
        await cur.close()
        marks = []
        for mark in mrks:
            mark = list(mark)
            mark = Mark(student=mark[1], mark=mark[2], subject=mark[3])
            marks.append(mark)
        return marks
    
    async def get_students_marks_by(self, student, subject):
        cur = await self.__conn__.execute('SELECT * FROM marks WHERE student = ? AND subject = ?', (student.telegram_id, subject, ))
        mrks = await cur.fetchall()
        await cur.close()
        marks = []
        for mark in mrks:
            mark = list(mark)
            mark = Mark(student=mark[1], mark=mark[2], subject=mark[3])
            marks.append(mark)
        return marks