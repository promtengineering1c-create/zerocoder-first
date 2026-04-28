import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import ctypes
import sys
import os
import win32event
import win32api
from winerror import ERROR_ALREADY_EXISTS

# --- Защита от второго запуска ---
mutex_name = "TerminalShadowTool_SingleInstance"
mutex = win32event.CreateMutex(None, False, mutex_name)
if win32api.GetLastError() == ERROR_ALREADY_EXISTS:
    sys.exit(0)

# --- Проверка прав администратора ---
def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

if not is_admin():
    pythonw_path = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
    ctypes.windll.shell32.ShellExecuteW(None, "runas", pythonw_path, f'"{os.path.abspath(sys.argv[0])}"', None, 1)
    sys.exit()

# --- Логика подключения ---
def on_double_click(event):
    selected_item = tree.selection()
    if not selected_item:
        return
    
    values = tree.item(selected_item, "values")
    user_id = values[1]
    
    # Проверяем, что ID — это число, а не "N/A"
    if user_id.isdigit():
        command = f"mstsc /control /noConsentPrompt /shadow:{user_id}"
        print(f"Запуск: {command}")
        subprocess.Popen(command, shell=True) # Используем Popen, чтобы GUI не зависал
    else:
        messagebox.showwarning("Ошибка", f"Невозможно подключиться к сессии с ID: {user_id}")

def get_users():
    for row in tree.get_children():
        tree.delete(row)
    try:
        result = subprocess.run("query user", shell=True, capture_output=True, text=True, encoding='cp866')
        output = result.stdout.strip()
        if not output:
            tree.insert('', 'end', values=("Нет данных", "", "Нет активных сеансов"))
            return
        lines = [line.strip() for line in output.splitlines()]
        for line in lines:
            if line.lower().startswith(("пользователь", "session")) or line.startswith("=") or not line:
                continue
            parts = line.split()
            if len(parts) >= 3:
                user = parts[0]
                session_id = parts[2] if parts[2].isdigit() else "N/A"
                state = parts[3]
                tree.insert('', 'end', values=(user, session_id, state))
    except Exception as e:
        tree.insert('', 'end', values=("Ошибка", "", str(e)))

# --- GUI ---
root = tk.Tk()
root.title("Terminal Shadow Tool")
root.geometry("500x400")

btn_refresh = tk.Button(root, text="Обновить список", command=get_users, bg="#007ACC", fg="white")
btn_refresh.pack(pady=10)

columns = ("user", "id", "state")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("user", text="Пользователь")
tree.heading("id", text="ID")
tree.heading("state", text="Состояние")

# Вот эта строчка связывает двойной клик с нашей функцией!
tree.bind("<Double-1>", on_double_click)

tree.pack(expand=True, fill="both", padx=10, pady=5)
get_users()
root.mainloop()