import tkinter as tk
import psycopg2
from tkinter import messagebox
from datetime import datetime
import webbrowser

# データベースの設定
db_config = {
    'dbname': 'mydb',
    'user': 'user1',
    'password': 'pass',
    'host': 'localhost'
}

def calculate_days_borrowed(lend_date):
    today = datetime.now().date()
    days_borrowed = (today - lend_date).days
    return max(0, days_borrowed)

def send_email(mail, book_title):
    email_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={mail}&su=返却リマインダー&body={book_title}の返却期限が過ぎています。"
    webbrowser.open(email_url)

def send_reminder(mail, book_title):
    send_email(mail, book_title)

def show_check_availability():
    check_availability_window = tk.Toplevel()
    check_availability_window.title("貸出状況確認")

    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # 本とリストのテーブルを結合して、貸し出し中の本だけを取得するクエリ
        cursor.execute("SELECT b.id, b.title, b.author, b.company, b.ISBN FROM book b JOIN list l ON b.ISBN = l.ISBN")
        books = cursor.fetchall()

        frame = tk.Frame(check_availability_window)
        frame.pack()

        id_label = tk.Label(frame, text="ID")
        id_label.grid(row=0, column=0)
        title_label = tk.Label(frame, text="本のタイトル")
        title_label.grid(row=0, column=1)
        author_label = tk.Label(frame, text="著者")
        author_label.grid(row=0, column=2)
        company_label = tk.Label(frame, text="出版社")
        company_label.grid(row=0, column=3)
        isbn_label = tk.Label(frame, text="ISBN")
        isbn_label.grid(row=0, column=4)
        days_borrowed_label = tk.Label(frame, text="貸出日数")
        days_borrowed_label.grid(row=0, column=5)
        mail_label = tk.Label(frame, text="メールアドレス")
        mail_label.grid(row=0, column=6)
        reminder_label = tk.Label(frame, text="メール送信")
        reminder_label.grid(row=0, column=7)

        row_number = 1
        for book in books:
            id_entry = tk.Entry(frame)
            id_entry.insert(0, book[0])
            id_entry.grid(row=row_number, column=0)
            title_entry = tk.Entry(frame)
            title_entry.insert(0, book[1])
            title_entry.grid(row=row_number, column=1)
            author_entry = tk.Entry(frame)
            author_entry.insert(0, book[2])
            author_entry.grid(row=row_number, column=2)
            company_entry = tk.Entry(frame)
            company_entry.insert(0, book[3])
            company_entry.grid(row=row_number, column=3)
            isbn_entry = tk.Entry(frame)
            isbn_entry.insert(0, book[4])
            isbn_entry.grid(row=row_number, column=4)
            cursor.execute("SELECT COUNT(*) FROM list WHERE ISBN = %s", (book[4],))
            is_lent = cursor.fetchone()[0]
            if is_lent > 0:
                cursor.execute("SELECT lend_date, mail FROM list WHERE ISBN = %s", (book[4],))
                lend_info = cursor.fetchone()
                lend_date = lend_info[0]
                mail = lend_info[1]
                days_borrowed = calculate_days_borrowed(lend_date)
                mail_entry = tk.Entry(frame)
                mail_entry.insert(0, mail)
                mail_entry.grid(row=row_number, column=6)
                days_borrowed_entry = tk.Entry(frame)
                days_borrowed_entry.insert(0, days_borrowed)
                days_borrowed_entry.grid(row=row_number, column=5)
                if days_borrowed > 7:
                    id_entry.config(bg="red")
                    title_entry.config(bg="red")
                    author_entry.config(bg="red")
                    company_entry.config(bg="red")
                    isbn_entry.config(bg="red")
                    days_borrowed_entry.config(bg="red")
                    mail_entry.config(bg="red")
                    reminder_button = tk.Button(frame, text="メール送信", command=lambda m=mail, b=book[1]: send_reminder(m, b))
                    reminder_button.grid(row=row_number, column=7)
                else:
                    id_entry.config(bg="lightgray")  # 7日以内の場合の色
                    title_entry.config(bg="lightgray")
                    author_entry.config(bg="lightgray")
                    company_entry.config(bg="lightgray")
                    isbn_entry.config(bg="lightgray")
                    days_borrowed_entry.config(bg="lightgray")
                    mail_entry.config(bg="lightgray")
            row_number += 1

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("エラー", f"データベースから本の一覧を取得する際にエラーが発生しました: {str(e)}")

    close_button = tk.Button(check_availability_window, text="閉じる", command=check_availability_window.destroy)
    close_button.pack()

if __name__ == "__main__":
    show_check_availability()
