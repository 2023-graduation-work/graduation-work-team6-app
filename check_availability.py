import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import psycopg2
from datetime import datetime, timedelta
import webbrowser

# データベース接続情報
db_config = {
    'dbname': 'mydb',
    'user': 'user1',
    'password': 'pass',
    'host': 'localhost'
}

def calculate_days_elapsed(lend_date):
    today = datetime.now().date()
    days_elapsed = (today - lend_date).days
    return days_elapsed

def send_email(mail, book_title):
    # ここに実際のメール送信処理を実装するコードを追加
    # 以下は仮の実装で、GmailのWebインターフェースを開くだけです
    email_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={mail}&su=返却リマインダー&body={book_title}の返却期限が過ぎています。"
    webbrowser.open(email_url)

def show_check_availability():
    check_availability_window = tk.Toplevel()
    check_availability_window.title("貸出状況確認")

    try:
        # データベースに接続
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # データベースから貸出情報を取得
        cursor.execute("SELECT id, title, mail, ISBN, lend_date FROM list")
        lending_list = cursor.fetchall()

        # ヘッダーの表示
        header_labels = ["ID", "Title", "Mail", "ISBN", "Lend Date", "Days Elapsed"]
        for i, label_text in enumerate(header_labels):
            header_label = tk.Label(check_availability_window, text=label_text)
            header_label.grid(row=0, column=i, padx=5, pady=5)

        # データの表示
        for row_num, lend_info in enumerate(lending_list, start=1):
            id, title, mail, ISBN, lend_date = lend_info
            days_elapsed = calculate_days_elapsed(lend_date)

            # 貸出から一週間以上経過している場合、Days Elapsedラベルを赤字にする
            days_elapsed_color = "red" if days_elapsed > 7 else "black"

            # ラベルの表示
            labels = [id, title, mail, ISBN, lend_date.strftime('%Y-%m-%d'), days_elapsed]
            for i, value in enumerate(labels):
                label = tk.Label(check_availability_window, text=str(value), fg=days_elapsed_color)
                label.grid(row=row_num, column=i, padx=5, pady=5)

            # 超過している場合にメール送信ボタンを追加
            if days_elapsed > 7:
                send_email_button = tk.Button(check_availability_window, text="メール送信", command=lambda m=mail, b=title: send_email(m, b))
                send_email_button.grid(row=row_num, column=len(header_labels), padx=5, pady=5)

        cursor.close()

    except Exception as e:
        tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")

    finally:
        if conn:
            conn.close()

    # ページを閉じるボタンを追加
    close_button = tk.Button(check_availability_window, text="閉じる", command=check_availability_window.destroy)
    close_button.grid(row=row_num + 1, column=0, columnspan=len(header_labels), pady=10)

if __name__ == "__main__":
    show_check_availability()
