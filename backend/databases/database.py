import json

class DataBase:
    def __init__(self) -> None:
        with open("data.json", "r") as read_file: 
            self.__data__ = json.load(read_file)
    

    def save_marks():
        pass
    
    def get_mark():
        pass
