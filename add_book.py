import tkinter as tk

def show_add_book():
    add_book_window = tk.Toplevel()
    add_book_window.title("本の登録")

    # 本の情報を入力するフォームを作成
    # データベースに情報を挿入するボタンを追加
    # ...

    # 登録ボタンとページを閉じるボタンを追加
    add_button = tk.Button(add_book_window, text="登録")
    add_button.pack()
    close_button = tk.Button(add_book_window, text="閉じる", command=add_book_window.destroy)
    close_button.pack()

if __name__ == "__main__":
    show_add_book()
