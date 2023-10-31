import tkinter as tk

def show_check_availability():
    check_availability_window = tk.Toplevel()
    check_availability_window.title("貸出状況確認")

    # 貸出状況を表示するウィジェットを作成
    # データベースから貸出状況を取得し、表示
    # ...

    # ページを閉じるボタンを追加
    close_button = tk.Button(check_availability_window, text="閉じる", command=check_availability_window.destroy)
    close_button.pack()

if __name__ == "__main__":
    show_check_availability()
