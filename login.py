import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import psycopg2
import hashlib

def login_page(root):
    def login():
        username = username_entry.get()
        password = password_entry.get()
        
        # パスワードをハッシュ化
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # データベースに接続
        conn = psycopg2.connect(
        dbname="mydb",
        user="user1",
        password="pass",
        host="localhost"
        )
        cursor = conn.cursor()
        
        # データベースからユーザー情報を検索
        cursor.execute("SELECT username, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        if user:
            stored_username, stored_password = user
            if hashed_password == stored_password:
                messagebox.showinfo("Success", "ログインに成功しました。")
                login_window.destroy()  # ログイン成功時にウィンドウを閉じる
            else:
                messagebox.showerror("Error", "パスワードが正しくありません。")
        else:
            messagebox.showerror("Error", "ユーザー名が存在しません.")
        
        cursor.close()
        conn.close()

    login_window = tk.Toplevel(root)
    login_window.title("ログイン")

    username_label = ttk.Label(login_window, text="ユーザー名")
    username_label.pack()
    username_entry = ttk.Entry(login_window)
    username_entry.pack()

    password_label = ttk.Label(login_window, text="パスワード")
    password_label.pack()
    password_entry = ttk.Entry(login_window, show="*")
    password_entry.pack()

    login_button = ttk.Button(login_window, text="ログイン", command=login)
    login_button.pack()
