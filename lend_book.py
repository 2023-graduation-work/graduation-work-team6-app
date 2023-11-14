import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry  # tkcalendarをインポート
import psycopg2

# データベース接続情報
db_config = {
    'dbname': 'mydb',
    'user': 'user1',
    'password': 'pass',
    'host': 'localhost'
}

def lend_book(email, book_title, lend_date, lend_book_window):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # lend_listテーブルにデータを挿入
        cursor.execute("INSERT INTO list (title, mail, ISBN, lend_date) VALUES (%s, %s, %s, %s)",
                       (book_title, email, isbn_entry.get(), lend_date))
        
        conn.commit()
        messagebox.showinfo("結果", f"{book_title} を {email} に {lend_date} に貸し出しました。")
    except psycopg2.Error as e:
        print(f"エラー: データベースへのデータ挿入に失敗しました - {e}")
    finally:
        if conn:
            conn.close()
        # 借りるボタンがクリックされたらウィンドウを閉じる
        lend_book_window.destroy()

def show_book_info(book, email, lend_date, parent_window):
    book_info_window = tk.Toplevel(parent_window)
    book_info_window.title("本の情報")

    labels = ["本のタイトル", "ISBN"]
    for i, label_text in enumerate(labels):
        label = tk.Label(book_info_window, text=f"{label_text}: {book[i]}")
        label.pack()

    # カレンダーウィジェットを配置
    lend_date_label = tk.Label(book_info_window, text="貸出日の選択")
    lend_date_label.pack()

    # tkcalendarのDateEntryを使用
    lend_date = DateEntry(book_info_window, date_pattern='yyyy-mm-dd')
    lend_date.pack()

    lend_button = tk.Button(book_info_window, text="借りる", command=lambda: lend_book(email, book[0], lend_date.get(), book_info_window))
    lend_button.pack()

def show_lend_book():
    lend_book_window = tk.Toplevel()
    lend_book_window.title("本の貸出")
    isbn_label = tk.Label(lend_book_window, text="ISBNを入力してください")
    isbn_label.pack()

    global isbn_entry  # isbn_entryをグローバル変数にする
    isbn_entry = tk.Entry(lend_book_window)
    isbn_entry.pack()

    # メールアドレスを入力するためのエントリウィジェットを配置
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
                    show_book_info(book, email, None, lend_book_window)
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
