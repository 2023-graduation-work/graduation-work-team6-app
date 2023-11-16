import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import webbrowser
import psycopg2

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

def send_email(mail, book_title, user_name, lend_date):
    subject = "図書室からのお知らせ"
    body = f"{user_name}様\r\n\r\n"\
           "大変お世話になっております。\r\n"\
           "盛ジョビ図書室 狢澤碧 です。\r\n\r\n"\
           f"{str(lend_date)}にお貸しした「{book_title}」の貸し出し期限が過ぎていますので\r\n"\
           "至急、返却をお願いします。"
    
    # 新しく追加
    body = body.replace('\r\n', '%0A').replace('\n', '%0A').replace('\r', '%0A')
    
    email_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={mail}&su={subject}&body={body}"
    webbrowser.open(email_url)

def send_reminder(mail, book_title, user_name, lend_date):
    send_email(mail, book_title, user_name, lend_date)

def show_check_availability():
    check_availability_window = tk.Toplevel() 
    check_availability_window.title("貸出状況確認")

    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT b.id, b.title, b.author, b.company, b.ISBN, l.user_name, l.mail, l.lend_date FROM book b JOIN list l ON b.ISBN = l.ISBN")
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
        user_name_label = tk.Label(frame, text="借りている人")
        user_name_label.grid(row=0, column=5)
        days_borrowed_label = tk.Label(frame, text="貸出日数")
        days_borrowed_label.grid(row=0, column=6)
        mail_label = tk.Label(frame, text="メールアドレス")
        mail_label.grid(row=0, column=7)
        reminder_label = tk.Label(frame, text="メール送信")
        reminder_label.grid(row=0, column=8)

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
            user_name_entry = tk.Entry(frame)
            user_name_entry.insert(0, book[5])
            user_name_entry.grid(row=row_number, column=5)
            cursor.execute("SELECT lend_date FROM list WHERE ISBN = %s", (book[4],))
            lend_date = cursor.fetchone()[0]
            days_borrowed = calculate_days_borrowed(lend_date)
            days_borrowed_entry = tk.Entry(frame)
            days_borrowed_entry.insert(0, days_borrowed)
            days_borrowed_entry.grid(row=row_number, column=6)
            mail_entry = tk.Entry(frame)
            mail_entry.insert(0, book[6])
            mail_entry.grid(row=row_number, column=7)
            
            if days_borrowed > 7:
                color = "#FF9999"  # 薄い赤
            else:
                color = "lightgray"  # 7日以内の場合の色
            
            id_entry.config(bg=color)
            title_entry.config(bg=color)
            author_entry.config(bg=color)
            company_entry.config(bg=color)
            isbn_entry.config(bg=color)
            user_name_entry.config(bg=color)
            days_borrowed_entry.config(bg=color)
            mail_entry.config(bg=color)
            
            if days_borrowed > 7:
                reminder_button = tk.Button(frame, text="メール送信", command=lambda m=book[6], b=book[1], u=book[5], ld=lend_date: send_reminder(m, b, u, ld))
                reminder_button.grid(row=row_number, column=8)
            
            row_number += 1

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("エラー", f"データベースから本の一覧を取得する際にエラーが発生しました: {str(e)}")

    close_button = tk.Button(check_availability_window, text="閉じる", command=check_availability_window.destroy)
    close_button.pack()

if __name__ == "__main__":
    show_check_availability()
