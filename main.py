import datetime as time

tasks = {}

class Task:
    description: str
    deadline: time
    done: bool

    def __init__(self, description, deadline, done):
        self.description = description
        self.deadline = deadline
        self.done = done

    def info(self):
        print(f"Задача: {self.description}")
        print(f"Срок выполнения: {self.deadline}")