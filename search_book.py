import tkinter as tk

def show_search_book():
    search_book_window = tk.Toplevel()
    search_book_window.title("本の検索")

    # 本を検索するための入力フォームを作成
    # 検索ボタンを追加
    # 検索結果を表示するウィジェットを追加
    # ...

    # ページを閉じるボタンを追加
    close_button = tk.Button(search_book_window, text="閉じる", command=search_book_window.destroy)
    close_button.pack()

if __name__ == "__main__":
    show_search_book()
