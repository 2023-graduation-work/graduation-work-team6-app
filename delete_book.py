import tkinter as tk
from tkinter import messagebox
import psycopg2

def show_delete_book():
    delete_book_window = tk.Toplevel()
    delete_book_window.title("本の削除")

    isbn_label = tk.Label(delete_book_window, text="削除する本のISBN:")
    isbn_label.pack()
    isbn_entry = tk.Entry(delete_book_window)
    isbn_entry.pack()

    def delete_book_from_database():
        isbn = isbn_entry.get()

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

            if count == 0:
                messagebox.showerror("エラー", "指定した本は見つかりませんでした")
            else:
                cursor.execute("DELETE FROM book WHERE ISBN = %s", (isbn,))
                conn.commit()
                messagebox.showinfo("成功", "削除が完了しました")
                delete_book_window.destroy()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("エラー", f"本の削除中にエラーが発生しました: {str(e)}")

        cursor.close()
        conn.close()

    delete_button = tk.Button(delete_book_window, text="削除", command=delete_book_from_database)
    delete_button.pack()
    close_button = tk.Button(delete_book_window, text="閉じる", command=delete_book_window.destroy)
    close_button.pack()

if __name__ == "__main__":
    show_delete_book()
