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

        cursor.execute("SELECT id,title, author, company, ISBN FROM book")  # テーブルと列名を調整
        books = cursor.fetchall()

        # 本を表示するリストボックスを作成
        book_listbox = tk.Listbox(book_list_window)
        book_listbox.pack()

        # リストボックスに本を追加
        for book in books:
            book_info = f"{book[0]},{book[1]},{book[2]},{book[3]},{book[4]}"
            book_listbox.insert(tk.END, book_info)

        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("エラー", f"データベースから本の一覧を取得する際にエラーが発生しました: {str(e)}")

    # 閉じるボタン
    close_button = tk.Button(book_list_window, text="閉じる", command=book_list_window.destroy)
    close_button.pack()

if __name__ == "__main__":
    show_book_list()
