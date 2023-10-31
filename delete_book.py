import tkinter as tk

def show_delete_book():
    delete_book_window = tk.Toplevel()
    delete_book_window.title("本の削除")

    # 本を選択し、削除操作を実行するウィジェットを作成
    # 削除ボタンを追加
    # ...

    # ページを閉じるボタンを追加
    close_button = tk.Button(delete_book_window, text="閉じる", command=delete_book_window.destroy)
    close_button.pack()

if __name__ == "__main__":
    show_delete_book()
