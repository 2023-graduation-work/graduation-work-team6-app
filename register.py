import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import psycopg2
import hashlib

def register_page(root):
    def register():
        username = username_entry.get()
        age = int(grade_combobox.get())  # 学年を整数に変換
        gender = gender_var.get()
        email = email_entry.get()
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

        try:
            # データベースにユーザー情報を挿入
            cursor.execute(
                "INSERT INTO users (username, age, gender, email, password) VALUES (%s, %s, %s, %s, %s)",
                (username, age, gender, email, hashed_password)
            )
            conn.commit()
            messagebox.showinfo("Success", "新規登録が完了しました。")
            register_window.destroy()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"新規登録中にエラーが発生しました: {str(e)}")

        cursor.close()
        conn.close()

    register_window = tk.Toplevel(root)
    register_window.title("新規登録")

    username_label = ttk.Label(register_window, text="ユーザー名")
    username_label.pack()
    username_entry = ttk.Entry(register_window)
    username_entry.pack()

    grade_label = ttk.Label(register_window, text="学年")
    grade_label.pack()

    # 学年を選択するCombobox（整数値を使う）
    grade_combobox = ttk.Combobox(register_window, values=[1, 2, 3, 4])
    grade_combobox.set(1)  # 初期値を整数で設定
    grade_combobox.pack()

    gender_label = ttk.Label(register_window, text="性別")
    gender_label.pack()

    gender_var = tk.StringVar()

    male_radio = ttk.Radiobutton(register_window, text="男性", variable=gender_var, value="Male")
    male_radio.pack()
    female_radio = ttk.Radiobutton(register_window, text="女性", variable=gender_var, value="Female")
    female_radio.pack()
    no_answer_radio = ttk.Radiobutton(register_window, text="無回答", variable=gender_var, value="無回答")
    no_answer_radio.pack()

    email_label = ttk.Label(register_window, text="メールアドレス")
    email_label.pack()
    email_entry = ttk.Entry(register_window)
    email_entry.pack()

    password_label = ttk.Label(register_window, text="パスワード")
    password_label.pack()
    password_entry = ttk.Entry(register_window, show="*")
    password_entry.pack()

    register_button = ttk.Button(register_window, text="新規登録", command=register)
    register_button.pack()
