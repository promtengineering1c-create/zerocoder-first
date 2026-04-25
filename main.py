import tkinter as tk
from tkinter import ttk
import subprocess

def get_users():
    # Получаем данные от системы
    try:
        output = subprocess.check_output("query user", shell=True).decode("cp866")
        # Здесь будет логика обработки текста
        print(output) 
    except subprocess.CalledProcessError:
        print("Пользователи не найдены или ошибка команды")

# Создаем главное окно
root = tk.Tk()
root.title("Terminal Shadow Tool")
root.geometry("400x300")

# Кнопка обновления списка
btn_refresh = tk.Button(root, text="Обновить список", command=get_users)
btn_refresh.pack(pady=10)

# Список для отображения (таблица)
columns = ("user", "id", "state")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col.capitalize())
tree.pack(expand=True, fill="both")

root.mainloop()