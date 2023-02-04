from dataclasses import dataclass
from datetime import date

@dataclass
class Note:
    subject: str
    theme: str
    date: date
    files: list
    