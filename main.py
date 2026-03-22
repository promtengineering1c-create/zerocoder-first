import datetime as time
import tkinter as tk
from tkinter import ttk

tasks = {}

class TimeEntry:
    def __init__(self, parent, width, font, bg, fg):
        
        super().__init__(parent, width, font, bg, fg)

        self.var = tk.StringVar()
        self.config(textvariable=self.var)
        self.var.trace_add("write", self.on_write)

        self._last = ""

    def on_write(self, *args):
        
        value = self.var.get()

        s = "".join(filter(str.isdigit, value))
        if len(s) > 4:
            s = s[:4]

        if len(s) >= 2:
            s = s[:2] + ":" + s[2:]
        
        if len(s) > 5:
            s = s[:5]

        if s == self._last:
            return   

        self._last = s
        self.var.set(s)

    def get_time(self):

        s = self.var.get()
        if len(s) != 5 or s[2] != ":":
            return None

        try:
            h = int(s[:2])
            m = int(s[3:])
            if 0 <= h <= 23 and 0 <= m <= 59:
                return h, m
            return None
        except ValueError:
            return None
        
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

root_add_task = tk.Tk()
root_add_task.config(bg='lightblue')
root_add_task.title("Новая задача")

task_frame = tk.Frame(root_add_task, bg='lightblut')
task_frame.pack(pady=20)

text_task = tk.Label(task_frame, text="Задача:", font=('Arial', 14), bg='lightblue', fg='darkblue')
text_task.pack(side=tk.LEFT, padx=10)

task_entry = tk.Entry(task_frame, width=30, font=('Arial',14), bg='white', fg='black')
task_entry.pack(side=tk.LEFT)

time_frame = tk.Frame(root_add_task, bg='lightblut')
time_frame.pack(pady=20)

time_task = tk.Label(time_frame, text="Завершить:", font=('Arial', 14), bg='lightblue', fg='darkblue')
time_task.pack(side=tk.LEFT, padx=10)

time_entry = TimeEntry(time_frame, 15, ('Arial',14), 'white', 'black')
time_entry.pack(side=tk.LEFT)

root_add_task.mainloop()