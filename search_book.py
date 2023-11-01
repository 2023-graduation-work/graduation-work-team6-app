import tkinter as tk
from tkinter import messagebox
import psycopg2

def show_search_book():
    search_book_window = tk.Toplevel()
    search_book_window.title("本の検索")

    search_label = tk.Label(search_book_window, text="タイトルまたは著者を入力:")
    search_label.pack()
    search_entry = tk.Entry(search_book_window)
    search_entry.pack()

    search_results_text = tk.Text(search_book_window, height=10, width=50)
    search_results_text.pack()

    def search_books():
        search_text = search_entry.get()

        conn = psycopg2.connect(
            dbname="mydb",
            user="user1",
            password="pass",
            host="localhost"
        )
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM book WHERE title ILIKE %s OR author ILIKE %s", (f"%{search_text}%", f"%{search_text}%"))
            search_results = cursor.fetchall()

            if not search_results:
                search_results_text.delete(1.0, tk.END)
                search_results_text.insert(tk.END, "該当する本は見つかりませんでした")
            else:
                search_results_text.delete(1.0, tk.END)
                for result in search_results:
                    search_results_text.insert(tk.END, f"タイトル: {result[1]}\n著者: {result[2]}\n出版社: {result[3]}\nISBN: {result[4]}\n\n")
        except Exception as e:
            messagebox.showerror("エラー", f"検索中にエラーが発生しました: {str(e)}")

        cursor.close()
        conn.close()

    search_button = tk.Button(search_book_window, text="検索", command=search_books)
    search_button.pack()
    close_button = tk.Button(search_book_window, text="閉じる", command=search_book_window.destroy)
    close_button.pack()

if __name__ == "__main__":
    show_search_book()
