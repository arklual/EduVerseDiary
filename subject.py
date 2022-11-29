class Subject:
    def __init__(self, aver, name):
        self.average_mark = aver
        self.marks = []
        self.name = name

    def __str__(self) -> str:
        return f'{self.name} {self.average_mark} {self.marks}'
