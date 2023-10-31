import tkinter as tk

def show_lend_book():
    lend_book_window = tk.Toplevel()
    lend_book_window.title("本の貸出")

    # 本を選択し、貸出操作を実行するウィジェットを作成
    # 貸出ボタンを追加
    # ...

    # ページを閉じるボタンを追加
    close_button = tk.Button(lend_book_window, text="閉じる", command=lend_book_window.destroy)
    close_button.pack()

if __name__ == "__main__":
    show_lend_book()
