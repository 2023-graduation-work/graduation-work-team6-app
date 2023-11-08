import tkinter as tk
import psycopg2
from tkinter import messagebox

def show_lend_book():
    lend_book_window = tk.Toplevel()
    lend_book_window.title("本の貸出")

    # ISBNを入力するためのエントリウィジェットを配置
    isbn_label = tk.Label(lend_book_window, text="ISBNを入力してください")
    isbn_label.pack()

    isbn_entry = tk.Entry(lend_book_window)
    isbn_entry.pack()

    # メールアドレスを入力するためのエントリウィジェットを配置
    email_label = tk.Label(lend_book_window, text="メールアドレスを入力してください")
    email_label.pack()

    email_entry = tk.Entry(lend_book_window)
    email_entry.pack()

    # 検索ボタンをクリックしたときの処理
    def search_book():
        isbn = isbn_entry.get()
        email = email_entry.get()
        if isbn and email:
            try:
                conn = psycopg2.connect(
                    dbname="mydb",
                    user="user1",
                    password="pass",
                    host="localhost"
                )
                cursor = conn.cursor()

                cursor.execute("SELECT title, ISBN FROM book WHERE ISBN = %s", (isbn,))
                book = cursor.fetchone()

                if book:
                    show_book_info(book, email, lend_book_window)
                else:
                    messagebox.showinfo("結果", "該当する本が見つかりませんでした.")
                cursor.close()
                conn.close()
            except Exception as e:
                messagebox.showerror("エラー", f"データベースからの検索中にエラーが発生しました: {str(e)}")
        else:
            messagebox.showinfo("警告", "ISBNとメールアドレスを入力してください.")

    search_button = tk.Button(lend_book_window, text="検索", command=search_book)
    search_button.pack()

def show_book_info(book, email, parent_window):
    book_info_window = tk.Toplevel(parent_window)
    book_info_window.title("本の情報")

    labels = ["本のタイトル", "ISBN"]
    for i, label_text in enumerate(labels):
        label = tk.Label(book_info_window, text=f"{label_text}: {book[i]}")
        label.pack()

    # 借りるボタンを作成
    lend_button = tk.Button(book_info_window, text="借りる", command=lambda: lend_book(email, book[0], book_info_window))
    lend_button.pack()

def lend_book(email, book_title, book_info_window):
    # ここで実際の貸出処理を行う
    messagebox.showinfo("結果", f"{book_title} を {email} に貸し出しました。")

    # 貸し出し処理後、ウィンドウを閉じる
    book_info_window.destroy()

if __name__ == "__main__":
    show_lend_book()
