from dataclasses import dataclass
from datetime import date

@dataclass
class Homework:
    subject: str
    task: str
    deadline: date
    files: list
    