import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import psycopg2

db_config = {
    'dbname': 'mydb',
    'user': 'user1',
    'password': 'pass',
    'host': 'localhost'
}

def is_book_borrowed(isbn):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT title FROM lend_list WHERE ISBN = %s", (isbn,))
        book = cursor.fetchone()

        return bool(book)  # 本が既に借りられていればTrue、そうでなければFalse

    except psycopg2.Error as e:
        print(f"エラー: データベースからの検索中にエラーが発生しました - {e}")
        return True  # エラーが発生した場合も、本が既に借りられているものとみなす

    finally:
        if conn:
            conn.close()

def borrow_book(email, book_title, borrow_date, lend_book_window):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        if is_book_borrowed(isbn_entry.get()):
            messagebox.showerror("エラー", "この本は既に借りられています。")
        else:
            cursor.execute("INSERT INTO lend_list (title, mail, ISBN, borrow_date) VALUES (%s, %s, %s, %s)",
                           (book_title, email, isbn_entry.get(), borrow_date))
            conn.commit()
            messagebox.showinfo("結果", f"{book_title} を {email} に {borrow_date} に借りました。")

    except psycopg2.Error as e:
        print(f"エラー: データベースへのデータ挿入に失敗しました - {e}")

    finally:
        if conn:
            conn.close()
        lend_book_window.destroy()

def show_book_info(book, email, parent_window):
    book_info_window = tk.Toplevel(parent_window)
    book_info_window.title("本の情報")

    labels = ["本のタイトル", "ISBN"]
    for i, label_text in enumerate(labels):
        label = tk.Label(book_info_window, text=label_text)
        label.grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
        entry = tk.Entry(book_info_window)
        entry.insert(0, book[i])
        entry.grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)

    lend_date_label = tk.Label(book_info_window, text="借りる日の選択")
    lend_date_label.grid(row=len(labels), column=0, padx=5, pady=5, sticky=tk.W)

    borrow_date = DateEntry(book_info_window, date_pattern='yyyy-mm-dd')
    borrow_date.grid(row=len(labels), column=1, padx=5, pady=5, sticky=tk.W)

    borrow_button = tk.Button(book_info_window, text="借りる", command=lambda: borrow_book(email, book[0], borrow_date.get(), book_info_window))
    borrow_button.grid(row=len(labels)+1, column=1, padx=5, pady=5, sticky=tk.W)

def show_lend_book():
    global lend_book_window, isbn_entry, email_entry  # グローバル変数として定義
    lend_book_window = tk.Toplevel()
    lend_book_window.title("本の貸出")
    isbn_label = tk.Label(lend_book_window, text="ISBNを入力してください")
    isbn_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

    isbn_entry = tk.Entry(lend_book_window)
    isbn_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

    email_label = tk.Label(lend_book_window, text="メールアドレスを入力してください")
    email_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

    email_entry = tk.Entry(lend_book_window)
    email_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

    search_button = tk.Button(lend_book_window, text="検索", command=search_book)
    search_button.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

def search_book():
    isbn = isbn_entry.get()
    email = email_entry.get()
    if isbn and email:
        try:
            conn = psycopg2.connect(**db_config)
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
        messagebox.showinfo("警告", "ISBNまたはメールアドレスを入力してください.")

if __name__ == "__main__":
    show_lend_book()
