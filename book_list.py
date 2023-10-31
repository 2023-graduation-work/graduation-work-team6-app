import tkinter as tk

def show_book_list():
    book_list_window = tk.Toplevel()
    book_list_window.title("本の一覧")

    # データベースから本の一覧を取得し、ウィジェットを使用して表示するコードを追加
    # ...

    # ページを閉じるボタンを追加
    close_button = tk.Button(book_list_window, text="閉じる", command=book_list_window.destroy)
    close_button.pack()

if __name__ == "__main__":
    show_book_list()
