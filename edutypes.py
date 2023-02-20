from dataclasses import dataclass
from enum import Enum
from datetime import date


class Gender(Enum):
    MALE = 1
    FEMALE = 2

    def __str__(self) -> str:
        if self == Gender.MALE:
            return 'male'
        else:
            return 'female'

    def __repr__(self) -> str:
        if self == Gender.MALE:
            return 'male'
        else:
            return 'female'


class EnglishGroup(Enum):
    MOLCHANOVA = 1
    KELDINA = 2

    def __str__(self) -> str:
        if self == EnglishGroup.MOLCHANOVA:
            return 'Молчанова'
        else:
            return 'Кельдина'

    def __repr__(self) -> str:
        if self == Gender.MALE:
            return 'Molchanova'
        else:
            return 'Keldina'

@dataclass
class Subject:
    id: str
    name: str

@dataclass
class Student:
    telegram_id: str
    first_name: str
    last_name: str
    gender: Gender
    english_group: EnglishGroup


@dataclass
class Homework:
    subject: str
    task: str
    deadline: date
    files: list


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
