import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import psycopg2
from datetime import datetime

# データベース接続情報
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

        cursor.execute("SELECT mail, lend_date FROM list WHERE ISBN = %s", (isbn,))
        result = cursor.fetchone()

        if result:
            return True, result  # 本が借りられている場合、Trueと借り主情報を返す
        else:
            return False, None  # 本が借りられていない場合、Falseを返す

    except psycopg2.Error as e:
        print(f"エラー: データベースからの検索中にエラーが発生しました - {e}")
        return False, None

    finally:
        if conn:
            conn.close()

def return_book(isbn, return_date, return_book_window):
    # 指定したISBNで本が借りられているか確認
    is_borrowed, borrower_info = is_book_borrowed(isbn)

    if is_borrowed:
        try:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            # lend_listテーブルからデータを削除
            cursor.execute("DELETE FROM list WHERE ISBN = %s", (isbn,))
            conn.commit()

            messagebox.showinfo("結果", f"ISBN {isbn} の本を {return_date} に返却しました。")
        except psycopg2.Error as e:
            error_message = f"エラー: データベースからの削除に失敗しました - {e}"
            messagebox.showerror("エラー", error_message)
        finally:
            if conn:
                conn.close()
            # 返却ボタンがクリックされたらウィンドウを閉じる
            return_book_window.destroy()
    else:
        messagebox.showerror("エラー", "この本はまだ借りられていません。")

def show_return_book():
    return_book_window = tk.Toplevel()
    return_book_window.title("本の返却")
    isbn_label = tk.Label(return_book_window, text="ISBNを入力してください")
    isbn_label.pack()

    global isbn_entry
    isbn_entry = tk.Entry(return_book_window)
    isbn_entry.pack()

    return_date_label = tk.Label(return_book_window, text="返却日の選択")
    return_date_label.pack()

    return_date = DateEntry(return_book_window, date_pattern='yyyy-mm-dd')
    return_date.pack()

    return_button = tk.Button(return_book_window, text="返却する", command=lambda: return_book(isbn_entry.get(), return_date.get(), return_book_window))
    return_button.pack()

if __name__ == "__main__":
    show_return_book()
