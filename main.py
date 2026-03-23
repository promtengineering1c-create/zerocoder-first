import datetime as time
import tkinter as tk
from tkinter import ttk
import threading

data_lock = threading.Lock()

tasks = {}
user_data = ()
active_thread = ()

def add_task():
    
    time = user_data[0]
    text = user_data[1]

    with data_lock:
        if time in task and not task['time']['stop']:
            print("У Вас есть активное напомнинаие на это время")
            return
        
        tasks[time] = {"text": text, "stop":False}

class TimeEntry(tk.Entry):
    def __init__(self, parent, **kwargs):
        
        super().__init__(parent, **kwargs)

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

def create_task_window():
    root_add_task = tk.Toplevel(root)
    root_add_task.geometry("500x150")
    root_add_task.config(bg='lightblue')
    root_add_task.title("Новая задача")

    task_frame = tk.Frame(root_add_task, bg='lightblue')
    task_frame.pack(pady=20)

    text_task = tk.Label(task_frame, text="Задача:", font=('Arial', 14), bg='lightblue', fg='darkblue')
    text_task.pack(side=tk.LEFT, padx=10)

    task_entry = tk.Entry(task_frame, width=30, font=('Arial',14), bg='white', fg='black')
    task_entry.pack(side=tk.LEFT)

    time_frame = tk.Frame(root_add_task, bg='lightblue')
    time_frame.pack(side=tk.LEFT, padx=10, pady=5) #

    time_task = tk.Label(time_frame, text="Завершить:", font=('Arial', 14), bg='lightblue', fg='darkblue')
    time_task.pack(side=tk.LEFT, padx=10)

    time_entry = TimeEntry(time_frame, width=5, font=('Arial',14), bg='white', fg='black')
    time_entry.pack(side=tk.LEFT)

    with data_lock:
        user_data = time_entry, task_entry

    button_add = tk.Button(root_add_task, text="Создать", width=10, font=("Arial", 14), bg="lightblue", fg="darkblue", command=add_task)
    button_add.pack(side=tk.LEFT, padx=10)

    try:
        root_add_task.mainloop()
    except KeyboardInterrupt:
        print("Программа завершена пользователем")
        root_add_task.destroy()

root = tk.Tk()
root.geometry("300x100")
root.config(bg="lightblue")
root.title("Список задач на сегодня")

style = ttk.Style()
style.theme_use('default')

style.configure(
    "TButton",
    font=("Arial", 12),
    padding=6
)

style.configure(
    "Primary.TButton",
    font=("Arial", 14, "bold"),
    foreground="white",
    background="#0078D7"
)

button_add = ttk.Button(root, text="Добавить новую задачу", width=30, style="Primary.TButton", command=create_task_window)
button_add.pack(side=tk.LEFT, padx=10)

try:
    root.mainloop()
except KeyboardInterrupt:
    print("Программа завершена пользователем")
    root.destroy()