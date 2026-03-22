import datetime as time
import tkinter as tk
from tkinter import ttk

tasks = {}

class TimeEntry:
    def __init__(self, width, font, background, fontground):
        
# time_entry = tk.Entry(time_frame, width=15, font=('Arial',14), bg='white', fg='black')

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

# time_entry.pack(side=tk.LEFT)