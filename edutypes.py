from dataclasses import dataclass
from enum import Enum
from datetime import date


@dataclass
class Subject:
    id: str
    name: str

@dataclass
class Student:
    telegram_id: str
    first_name: str
    last_name: str
    gender: str
    english_group: str
    info_group: str

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.telegram_id == other.telegram_id
        else:
            return False

@dataclass
class Homework:
    subject: str
    task: str
    deadline: date
    files: list
    task_id: str


@dataclass
class Note:
    subject: str
    theme: str
    date: date
    files: list


@dataclass
class Mark:
    student: Student
    mark: str
    subject: Subject

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.student.telegram_id == other.student.telegram_id) and (self.mark == other.mark) and (self.subject.id == other.subject.id)
        else:
            return False
