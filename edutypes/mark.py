from dataclasses import dataclass
from edutypes.student import Student

@dataclass
class Mark:
    student: Student
    mark: str
    subject: str