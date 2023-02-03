from dataclasses import dataclass

@dataclass
class Note:
    subject: str
    theme: str
    files: list
    