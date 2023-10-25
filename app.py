import tkinter as tk
from tkinter import ttk
import login
import register

app_window = tk.Tk()
app_window.title("図書管理アプリ")

def open_register_page():
    register.register_page(app_window)

def open_login_page():
    login.login_page(app_window)

register_button = ttk.Button(app_window, text="新規登録", command=open_register_page)
register_button.pack(pady=20)

login_button = ttk.Button(app_window, text="ログイン", command=open_login_page)
login_button.pack()

app_window.mainloop()
