import time as time
import datetime as datetime
import tkinter as tk
from tkinter import ttk
import threading

data_lock = threading.Lock()

tasks = {}
active_thread = ()

def add_task(task_time, text):
    
    with data_lock:

        if task_time in tasks and not tasks[task_time].done:
            print("У Вас есть задач на это время")
            return
        
        new_task = Task(text, task_time, False)
        tasks[task_time] = new_task

def send_reminder():
    while True:
        task_time = None
        now = datetime.datetime.now()
        now_time = now.strftime("%H:%M")

        show_task = ""

        with data_lock:
            for task_time in tasks:
                # Проверяем флаг остановки
                if tasks[task_time].done:
                    continue    
 
                # Проверяем, пришло ли время напоминания
                if task_time == now_time:
                    show_task = tasks[task_time].description
                    break
        
        if show_task:
            root.after(0, create_task_window, task_time, show_task)

        time.sleep(30)
 
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
        print(f"Статус: {'Выполнено' if self.done else 'Не выполнено'}")

    def mark_done(self):
        self.done = True

def get_current_tasks(only_current=True):
    task_listbox.delete(0, tk.END)

    with data_lock:
        if only_current:
            current_tasks = [task for task in tasks.values() if not task['task'].done]  
        else:
            current_tasks = [task for task in tasks.values()]

    if current_tasks:
        current_tasks.sort(key=lambda x: x['task'].deadline)
        status_icon = "✅ " if task.done else ""
        for task, task_time in current_tasks:
            task_listbox.insert(tk.END, f"{task_time}: {status_icon}{task.description}")      

def done_task(task_time):
    with data_lock:
        if task_time in tasks:
            tasks[task_time].done = True

def delete_task(delete=False):
    selected_indices = task_listbox.curselection()
    if not selected_indices:
        return

    with data_lock:
        for index in reversed(selected_indices):
            task_time = task_listbox.get(index).split(":")[0]
            if task_time in tasks:
                if delete:
                    del tasks[task_time]
                else:
                    tasks[task_time].mark_done()
   
def create_task_window(task_time, text):

    def on_close(task_time):
        done_task(task_time)
        win_task.destroy()
        root.update()

    win_task = tk.Toplevel(root)
    win_task.geometry("500x150")
    win_task.config(bg='lightblue')
    win_task.title("🔔 Напоминание")

    text_task = tk.Label(win_task, text=f"⏰{task_time}\n{text}", font=('Arial', 14), bg='lightblue', fg='darkblue')
    text_task.pack(side=tk.LEFT, padx=10)

    button_done = tk.Button(win_task, text="✅ Выполнено", width=15, font=("Arial", 14), bg="lightblue", fg="darkblue", command=lambda: on_close(task_time))
    button_done.pack(side=tk.LEFT, padx=10)
 
def create_add_task_window():

    def save_tasks(task_time, text):
        add_task(task_time, text)

        root_add_task.destroy()
        root.update()

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

    button_add = tk.Button(root_add_task, text="Создать", width=10, font=("Arial", 14), bg="lightblue", fg="darkblue", command=lambda: save_tasks(time_entry.get(), task_entry.get()))
    button_add.pack(side=tk.LEFT, padx=10)

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

manage_frame = tk.Frame(root, bg="lightblue")
manage_frame.pack(side=tk.TOP, pady=5, anchor="w")

button_add = ttk.Button(manage_frame, text="Добавить", width=10, style="Primary.TButton", command=create_add_task_window)
button_add.pack(side=tk.LEFT, padx=10)

button_done = tk.Button(manage_frame, text="Выполнено", width=10, font=("Arial", 14), bg="lightblue", fg="darkblue", command=delete_task)
button_done.pack(side=tk.LEFT, padx=10)

button_del = tk.Button(manage_frame, text="Удалить", width=10, font=("Arial", 14), bg="lightblue", fg="darkblue", command=lambda:delete_task(True))
button_del.pack(side=tk.LEFT, padx=10)

task_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=50, height=10, font=("Arial", 14), bg="white", fg="black")
task_listbox.pack(pady=10)  

get_current_tasks(False)  

reminder_thread = threading.Thread(target=send_reminder, daemon=True)
reminder_thread.start()
  
try:
    root.mainloop()
except KeyboardInterrupt:
    print("Программа завершена пользователем")
    root.destroy()