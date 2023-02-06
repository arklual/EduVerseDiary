import aiosqlite
import asyncio
from edutypes.student import Student, Gender, EnglishGroup

class Database:
    def __init__(self, conn) -> None:
        self.__conn__ = conn

    @staticmethod
    async def setup():
        conn = await aiosqlite.connect('./backend/databases/data.sqlite3')
        return Database(conn)
    
    async def close_db(self):
        self.__conn__.close()

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
    
    async def add_student(self, student):
        student = (student.telegram_id, student.first_name, student.last_name, student.gender.value, student.english_group.value)
        await self.__conn__.execute("INSERT INTO students (telegram_id, first_name, last_name, gender, english_group) VALUES(?, ?, ?, ?, ?);", student)
        await self.__conn__.commit()
    
    async def add_mark(self, mark):
        mark = (mark.student.telegram_id, mark.mark, mark.subject)
        await self.__conn__.execute("INSERT INTO marks (student, mark, subject) VALUES(?, ?, ?);", mark)
        await self.__conn__.commit()
    