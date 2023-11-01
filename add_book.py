import tkinter as tk
from tkinter import messagebox
import psycopg2

def show_add_book():
    add_book_window = tk.Toplevel()
    add_book_window.title("本の登録")

    title_label = tk.Label(add_book_window, text="タイトル:")
    title_label.pack()
    title_entry = tk.Entry(add_book_window)
    title_entry.pack()

    author_label = tk.Label(add_book_window, text="著者:")
    author_label.pack()
    author_entry = tk.Entry(add_book_window)
    author_entry.pack()

    company_label = tk.Label(add_book_window, text="出版社:")
    company_label.pack()
    company_entry = tk.Entry(add_book_window)
    company_entry.pack()

    isbn_label = tk.Label(add_book_window, text="ISBN:")
    isbn_label.pack()
    isbn_entry = tk.Entry(add_book_window)
    isbn_entry.pack()

    def add_book_to_database():
        title = title_entry.get()
        author = author_entry.get()
        company = company_entry.get()
        isbn = isbn_entry.get()

        conn = psycopg2.connect(
            dbname="mydb",
            user="user1",
            password="pass",
            host="localhost"
        )
        cursor = conn.cursor()

        try:

            cursor.execute(
                "INSERT INTO book (title, author, company, ISBN) VALUES (%s, %s, %s, %s)",
                (title, author, company, isbn)
            )
            conn.commit()
            messagebox.showinfo("Success", "本の登録が完了しました。")
            add_book_window.destroy()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"本の登録中にエラーが発生しました: {str(e)}")
    
    def add_book_to_database():
        title = title_entry.get()
        author = author_entry.get()
        company = company_entry.get()
        isbn = isbn_entry.get()

        errors = []

        if not title:
            errors.append("タイトルが入力されていません")
        if not author:
            errors.append("著者が入力されていません")
        if not company:
            errors.append("出版社が入力されていません")
        if not isbn:
            errors.append("ISBNが入力されていません")

        if errors:
            messagebox.showerror("エラー", "\n".join(errors))
            return  # エラーがある場合、本の登録を中止

        conn = psycopg2.connect(
        dbname="mydb",
        user="user1",
        password="pass",
        host="localhost"
        )
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT COUNT(*) FROM book WHERE ISBN = %s", (isbn,))
            count = cursor.fetchone()[0]

            if count > 0:
                messagebox.showerror("エラー", "同じ値のISBNが入力されました")
            else:
                cursor.execute(
                    "INSERT INTO book (title, author, company, ISBN) VALUES (%s, %s, %s, %s)",
                    (title, author, company, isbn)
                )
                conn.commit()
                messagebox.showinfo("成功", "本の登録が完了しました")
                add_book_window.destroy()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("エラー", f"本の登録中にエラーが発生しました: {str(e)}")

        cursor.close()
        conn.close()
        
    add_button = tk.Button(add_book_window, text="登録", command=add_book_to_database)
    add_button.pack()
    close_button = tk.Button(add_book_window, text="閉じる", command=add_book_window.destroy)
    close_button.pack()