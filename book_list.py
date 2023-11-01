import tkinter as tk
import psycopg2
from tkinter import messagebox

def show_book_list():
    book_list_window = tk.Toplevel()
    book_list_window.title("本の一覧")

    # データベースから本の一覧を取得
    try:
        conn = psycopg2.connect(
            dbname="mydb",
            user="user1",
            password="pass",
            host="localhost"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT id, title, author, company, ISBN FROM book")  # テーブルと列名を調整
        books = cursor.fetchall()

        # ラベルとエントリウィジェットを含むフレームを作成
        frame = tk.Frame(book_list_window)
        frame.pack()

        id_label = tk.Label(frame, text="ID")
        id_label.grid(row=0, column=0)
        title_label = tk.Label(frame, text="本のタイトル")
        title_label.grid(row=0, column=1)
        author_label = tk.Label(frame, text="著者")
        author_label.grid(row=0, column=2)
        company_label = tk.Label(frame, text="出版社")
        company_label.grid(row=0, column=3)
        isbn_label = tk.Label(frame, text="ISBN")
        isbn_label.grid(row=0, column=4)

        row_number = 1
        for book in books:
            id_entry = tk.Entry(frame)
            id_entry.insert(0, book[0])
            id_entry.grid(row=row_number, column=0)
            title_entry = tk.Entry(frame)
            title_entry.insert(0, book[1])
            title_entry.grid(row=row_number, column=1)
            author_entry = tk.Entry(frame)
            author_entry.insert(0, book[2])
            author_entry.grid(row=row_number, column=2)
            company_entry = tk.Entry(frame)
            company_entry.insert(0, book[3])
            company_entry.grid(row=row_number, column=3)
            isbn_entry = tk.Entry(frame)
            isbn_entry.insert(0, book[4])
            isbn_entry.grid(row=row_number, column=4)

            row_number += 1

        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("エラー", f"データベースから本の一覧を取得する際にエラーが発生しました: {str(e)}")

    # 閉じるボタン
    close_button = tk.Button(book_list_window, text="閉じる", command=book_list_window.destroy)
    close_button.pack()

if __name__ == "__main__":
    show_book_list()
