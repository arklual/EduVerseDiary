import aiosqlite
from backend.databases import database
from edutypes import Student, Mark, Subject

class Database:
    def __init__(self, conn) -> None:
        self.__conn__ = conn

    @staticmethod
    async def setup():
        conn = await aiosqlite.connect('./backend/databases/data.sqlite3')
        return Database(conn)
    
    async def close_connection(self):
        await self.__conn__.close()

    async def get_students(self):
        cur = await self.__conn__.execute('SELECT telegram_id, first_name, last_name, gender, english_group, info_group FROM students ORDER BY last_name')
        sts = await cur.fetchall()
        await cur.close()
        students = []
        for student in sts:
            student = list(student)
            student = Student(telegram_id=str(student[0]),
                            first_name=student[1], 
                            last_name=student[2], 
                            gender=str(student[3]), 
                            english_group=str(student[4]),
                            info_group=str(student[5]))
            students.append(student)
        return students
    
    async def get_student_by_id(self, telegram_id):
        cur = await self.__conn__.execute('SELECT telegram_id, first_name, last_name, gender, english_group, info_group FROM students WHERE telegram_id = ?', (telegram_id,))
        student = await cur.fetchone()
        await cur.close()
        student = list(student)
        student = Student(telegram_id=str(student[0]),
                            first_name=student[1], 
                            last_name=student[2], 
                            gender=str(student[3]), 
                            english_group=str(student[4]),
                            info_group=str(student[5]))
        return student
    
    async def add_mark(self, mark, commit=True):
        mark = (mark.student.telegram_id, mark.mark, mark.subject.id)
        await self.__conn__.execute("INSERT INTO marks (student, mark, subject) VALUES(?, ?, ?);", mark)
        if commit:
            await self.__conn__.commit()
    
    async def get_students_marks(self, student):
        cur = await self.__conn__.execute('SELECT student, mark, subject FROM marks WHERE student = ?', (student.telegram_id,))
        mrks = await cur.fetchall()
        await cur.close()
        marks = []
        for mark in mrks:
            mark = list(mark)
            db = await database.Database.setup()
            mark = Mark(student=(await db.get_student_by_id(str(mark[0]))), mark=str(mark[1]), subject=Subject(id=str(mark[2]), name=(await db.get_subject_by_id(mark[2])).name))
            await db.close_connection()
            marks.append(mark)
        return marks
    
    async def get_students_marks_in(self, student, subject):
        cur = await self.__conn__.execute('SELECT student, mark, subject FROM marks WHERE student = ? AND subject = ?', (student.telegram_id, subject.id, ))
        mrks = await cur.fetchall()
        await cur.close()
        marks = []
        for mark in mrks:
            mark = list(mark)
            db = await database.Database.setup()
            mark = Mark(student=await(db.get_student_by_id(str(mark[0]))), mark=str(mark[1]), subject=Subject(id=str(mark[2]), name=(await db.get_subject_by_id(mark[2])).name))
            await db.close_connection()
            marks.append(mark)
        return marks

    async def remove_students_marks_in(self, student, subject):
        await self.__conn__.execute('DELETE FROM marks WHERE student = ? AND subject = ?', (student.telegram_id, subject.id, ))
        await self.__conn__.commit()
    
    async def remove_marks_in(self, subject):
        await self.__conn__.execute('DELETE FROM marks WHERE subject = ?', (subject.id, ))
        await self.__conn__.commit()
    
    async def remove_marks(self):
        await self.__conn__.execute('DELETE FROM marks')
        await self.__conn__.commit()

    async def reset_marks_ids(self):
        await self.__conn__.execute('DELETE FROM sqlite_sequence WHERE name="marks"')
        await self.__conn__.commit()

    async def get_subject_by_id(self, subject_id):
        cur = await self.__conn__.execute('SELECT name FROM subjects WHERE id = ?', (subject_id, ))
        subject = list(await cur.fetchone())[0]
        await cur.close()
        return Subject(str(subject_id), subject)
    
    async def get_subject_by_name(self, subject_name):
        cur = await self.__conn__.execute('SELECT id FROM subjects WHERE name = ?', (subject_name, ))
        id = list(await cur.fetchone())[0]
        await cur.close()
        return Subject(str(id), subject_name)
    
    async def get_subjects(self):
        cur = await self.__conn__.execute('SELECT id, name FROM subjects')
        sbs = await cur.fetchall()
        await cur.close()
        subjects = []
        for sub in sbs:
            subjects.append(Subject(id=str(list(sub)[0]), name=list(sub)[1]))
        return subjects

    async def get_bot_token(self):
        cur = await self.__conn__.execute('SELECT token FROM bot')
        (token,) = await cur.fetchone()
        await cur.close()
        return token

    async def get_username(self):
        cur = await self.__conn__.execute('SELECT username FROM bot')
        (username, ) = await cur.fetchone()
        username = username.replace('_', '')
        await cur.close()
        return username

    async def get_password(self):
        cur = await self.__conn__.execute('SELECT password FROM bot')
        (password, ) = await cur.fetchone()
        password = password.replace('_', '')
        await cur.close()
        return password

    async def get_notion_token(self):
        cur = await self.__conn__.execute('SELECT notion_token FROM bot')
        (token,) = await cur.fetchone()
        await cur.close()
        return token
    
    async def hw_exists(self, homework, student):
        homework = (student.telegram_id, '_'+homework.task_id,)
        cur = await self.__conn__.execute('SELECT EXISTS(SELECT * FROM homeworks WHERE student=? AND task_id=?);', homework)
        (exists, ) = await cur.fetchone()
        await cur.close()
        return bool(exists)

    async def add_homework(self, homework, student):
        homework = (student.telegram_id, '_'+homework.task_id,)
        await self.__conn__.execute("INSERT INTO homeworks (student, task_id) VALUES(?, ?);", homework)
        await self.__conn__.commit()

    async def change_homework_done(self, homework, student, is_done=False):
        homework = (int(is_done), student.telegram_id, '_'+homework.task_id,)
        await self.__conn__.execute("UPDATE homeworks SET is_done=? WHERE student=? AND task_id=?", homework)
        await self.__conn__.commit()
    
    async def is_homework_done(self, homework, student):
        homework = (student.telegram_id, '_'+homework.task_id,)
        cur = await self.__conn__.execute('SELECT is_done FROM homeworks WHERE student=? AND task_id=?', homework)
        (is_done, ) = await cur.fetchone()
        await cur.close()
        return bool(is_done)
    
    async def commit(self):
        await self.__conn__.commit()