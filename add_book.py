import tkinter as tk
from tkinter import messagebox
from isbnlib import is_isbn13, meta
import psycopg2
from tkinter import ttk

# データベース接続情報
db_config = {
    'dbname': 'mydb',
    'user': 'user1',
    'password': 'pass',
    'host': 'localhost'
}

# グローバル変数としてbarcode_entryを宣言
barcode_entry = None
book_info_label = None

def is_isbn_already_saved(isbn):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM book WHERE ISBN = %s", (isbn,))
        count = cursor.fetchone()[0]
        return count > 0
    except psycopg2.Error as e:
        print(f"エラー: ISBNの存在を確認できません - {e}")
    finally:
        if conn:
            conn.close()

def get_book_info(isbn):
    if is_isbn13(isbn):
        book_info = meta(str(isbn))
        return book_info
    else:
        return None

def save_book_info_to_database(isbn, tree):
    if not is_isbn_already_saved(isbn):
        book_info = get_book_info(isbn)
        if book_info:
            title = book_info.get('Title', '')
            authors = ', '.join(book_info.get('Authors', []))
            publisher = book_info.get('Publisher', '')

            # データベースに保存
            try:
                conn = psycopg2.connect(**db_config)
                cursor = conn.cursor()

                # 重複チェック
                cursor.execute("SELECT COUNT(*) FROM book WHERE ISBN = %s", (isbn,))
                count = cursor.fetchone()[0]
                if count > 0:
                    messagebox.showinfo("情報", "この本は既に登録されています。")
                else:
                    cursor.execute("INSERT INTO book (title, author, company, ISBN) VALUES (%s, %s, %s, %s)",
                                   (title, authors, publisher, isbn))
                    conn.commit()
                    messagebox.showinfo("成功", "書籍情報がデータベースに保存されました。")
            except psycopg2.Error as e:
                conn.rollback()
                messagebox.showerror("エラー", f"データベースへのデータ挿入に失敗しました - {e}")
            finally:
                if conn:
                    conn.close()
    else:
        messagebox.showinfo("情報", "このISBNはすでにデータベースに保存されています.")

def scan_barcode_and_show_info(tree):
    global barcode_entry
    isbn = barcode_entry.get()

    if not isbn:
        messagebox.showerror("エラー", "ISBNが空白です。")
        return

    book_info = get_book_info(isbn)

    if book_info:
        title = book_info.get('Title', '')
        authors = ', '.join(book_info.get('Authors', []))
        publisher = book_info.get('Publisher', '')

        # 以前のエントリをTreeviewからクリア
        tree.delete(*tree.get_children())

        # 新しいデータをTreeviewに挿入
        tree.insert("", "end", values=(title, authors, publisher, isbn))
    else:
        messagebox.showinfo("情報", "無効なISBNまたは書籍が見つかりません。")

def show_add_book():
    add_book_window = tk.Toplevel()
    add_book_window.title("本の登録")

    # グローバル変数としてbarcode_entryを宣言
    global barcode_entry
    global book_info_label

    barcode_label = tk.Label(add_book_window, text="バーコード (ISBN):")
    barcode_label.pack()
    barcode_entry = tk.Entry(add_book_window)
    barcode_entry.pack()

    scan_button = tk.Button(add_book_window, text="スキャンして情報表示", command=lambda: scan_barcode_and_show_info(tree))
    scan_button.pack()

    # 表形式で本の情報を表示するためのTreeviewウィジェットの作成
    tree = ttk.Treeview(add_book_window, columns=("Title", "Authors", "Publisher", "ISBN"), show="headings")
    tree.heading("Title", text="タイトル")
    tree.heading("Authors", text="著者")
    tree.heading("Publisher", text="出版社")
    tree.heading("ISBN", text="ISBN")
    tree.pack()

    save_button = tk.Button(add_book_window, text="スキャンして保存", command=lambda: save_book_info_to_database(barcode_entry.get(), tree))
    save_button.pack()

    close_button = tk.Button(add_book_window, text="閉じる", command=add_book_window.destroy)
    close_button.pack()

# GUIの実行
if __name__ == "__main__":
    add_book_window = tk.Tk()
    add_book_window.title("本の登録")

    barcode_label = tk.Label(add_book_window, text="バーコード (ISBN):")
    barcode_label.pack()
    barcode_entry = tk.Entry(add_book_window)
    barcode_entry.pack()

    scan_button = tk.Button(add_book_window, text="スキャンして情報表示", command=show_add_book)
    scan_button.pack()

    add_book_window.mainloop()
