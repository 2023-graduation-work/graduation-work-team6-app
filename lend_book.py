import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from tkcalendar import DateEntry
import psycopg2
from datetime import date

db_config = {
    'dbname': 'mydb',
    'user': 'user1',
    'password': 'pass',
    'host': 'localhost'
}

def is_book_already_borrowed(isbn):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT title, mail, lend_date FROM list WHERE ISBN = %s", (isbn,))
        result = cursor.fetchone()

        if result:
            return True, result
        else:
            return False, None
    except psycopg2.Error as e:
        print(f"エラー: データベース検索中にエラーが発生しました - {e}")
        return False, None
    finally:
        if conn:
            conn.close()

def lend_book(email, user_name, book_title, lend_date, lend_book_window):
    isbn = isbn_entry.get()

    is_borrowed, borrower_info = is_book_already_borrowed(isbn)

    if is_borrowed:
        error_message = f"この本は既に借りられています。\n借り主: {borrower_info[1]}\n貸出日: {borrower_info[2]}"
        messagebox.showerror("エラー", error_message)
    else:
        try:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            cursor.execute("INSERT INTO list (title, user_name, mail, ISBN, lend_date) VALUES (%s, %s, %s, %s, %s)",
                           (book_title, user_name, email, isbn, lend_date))

            conn.commit()
            messagebox.showinfo("結果", f"{book_title} を {user_name} さん に {lend_date} に貸し出しました。")
        except psycopg2.Error as e:
            error_message = f"エラー: データベースへのデータ挿入に失敗しました - {e}"
            messagebox.showerror("エラー", error_message)
        finally:
            if conn:
                conn.close()
            lend_book_window.destroy()

def show_book_info(book, email, parent_window):
    book_info_window = tk.Toplevel(parent_window)
    book_info_window.title("本の情報")

    table = ttk.Treeview(book_info_window, columns=("Property", "Value"), show="headings")
    table.heading("Property", text="")
    table.heading("Value", text="")

    properties = ["本のタイトル", "ISBN", "今日の日付"]
    values = [book[0], book[1], date.today()]

    for prop, val in zip(properties, values):
        table.insert("", "end", values=(prop, val))

    table.pack()

    lend_button = tk.Button(book_info_window, text="借りる", command=lambda: lend_book(email, user_name_entry.get(), book[0], date.today(), book_info_window))
    lend_button.pack()

def show_lend_book():
    lend_book_window = tk.Toplevel()
    lend_book_window.title("本の貸出")

    isbn_label = tk.Label(lend_book_window, text="ISBNを入力してください")
    isbn_label.pack()

    global isbn_entry  
    isbn_entry = tk.Entry(lend_book_window)
    isbn_entry.pack()

    user_name_label = tk.Label(lend_book_window, text="名前を入力してください")
    user_name_label.pack()

    global user_name_entry
    user_name_entry = tk.Entry(lend_book_window)
    user_name_entry.pack()

    email_label = tk.Label(lend_book_window, text="メールアドレスを入力してください")
    email_label.pack()

    email_entry = tk.Entry(lend_book_window)
    email_entry.pack()

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

    search_button = tk.Button(lend_book_window, text="検索", command=search_book)
    search_button.pack()

if __name__ == "__main__":
    show_lend_book()
