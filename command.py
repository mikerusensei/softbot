import os
import json
import re

from abc import ABC, abstractmethod
from datetime import datetime

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class Current_Datetime(Command):
    def __init__(self):
        self.execute()

    def execute(self):
        now = datetime.now()
        format_now = now.strftime("%m/%d/%Y %I:%M %p")
        parse_now = datetime.strptime(format_now, "%m/%d/%Y %I:%M %p")

        return parse_now
    
class Date_Parser(Command):
    def __init__(self, date):
        self.dt = date

    def execute(self):
        pattern = r"([0-9]{2}:[0-9]{2} (?:AM|PM))\s+(\w+) ([0-9]{2}), ([0-9]{4})"
        result = re.search(pattern, self.dt)
        month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"].index(result[2]) + 1
        day = result[3]
        year = result[4]
        time_parse = result[1]

        parsed_datetime = datetime.strptime(f"{month}/{day}/{year} {time_parse}",  "%m/%d/%Y %I:%M %p")

        return parsed_datetime

class Directory(Command):
    def __init__(self):
        pass

    def execute(self):
        directory = "softbot"
        parent = "C:\\"
        path = os.path.join(parent, directory)

        if  not os.path.exists(path):
            os.mkdir(path)
            print(f"Created {path}")

class Save_JSON(Command):
    def __init__(self, data, file_path):
        self.data = data
        self.file_path = file_path        

    def execute(self):
        with open(self.file_path, "w") as filewrite:
            json.dump(self.data, filewrite, indent=4)

class Load_JSON(Command):
    def __init__(self, file_path):
        self.file_path = file_path

    def execute(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as fileread:
                return json.load(fileread)
        else:
            return {}
