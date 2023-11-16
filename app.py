import tkinter as tk
from tkinter import ttk
import book_list  
import add_book  
import search_book  
import lend_book 
import delete_book  
import check_availability  
import return_book

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")

root = tk.Tk()
root.title("図書管理アプリ")

window_width = root.winfo_screenwidth() - 100
window_height = root.winfo_screenheight() - 100

root.geometry(f"{window_width}x{window_height}")

menu_label = tk.Label(root, text="図書管理メニュー", font=('Helvetica', 24))
menu_label.pack(pady=20)

style = ttk.Style()
style.configure("TButton", padding=15, font=('Helvetica', 16))

def show_book_list():
    book_list.show_book_list()

def show_add_book():
    add_book.show_add_book()

def show_search_book():
    search_book.show_search_book()

def show_lend_book(): 
    lend_book.show_lend_book()

def show_delete_book():
    delete_book.show_delete_book()

def show_check_availability():
    check_availability.show_check_availability()
    
def show_return_book():
    return_book.show_return_book()

list_books_button = ttk.Button(root, text="本の一覧", command=show_book_list, style="TButton")
add_book_button = ttk.Button(root, text="本の登録", command=show_add_book, style="TButton")
search_book_button = ttk.Button(root, text="本の検索", command=show_search_book, style="TButton")
lend_book_button = ttk.Button(root, text="本の貸出", command=show_lend_book, style="TButton")
delete_book_button = ttk.Button(root, text="本の削除", command=show_delete_book, style="TButton")
check_availability_button = ttk.Button(root, text="貸出状況確認", command=show_check_availability, style="TButton")
return_book_button = ttk.Button(root, text="本の返却", command=show_return_book, style="TButton")

list_books_button.pack(side=tk.LEFT, padx=5, pady=(20, 10), expand=True)
add_book_button.pack(side=tk.LEFT, padx=5, pady=(20, 10), expand=True)
search_book_button.pack(side=tk.LEFT, padx=5, pady=(20, 10), expand=True)
lend_book_button.pack(side=tk.LEFT, padx=5, pady=(20, 10), expand=True)
delete_book_button.pack(side=tk.LEFT, padx=5, pady=(20, 10), expand=True)
check_availability_button.pack(side=tk.LEFT, padx=5, pady=(20, 10), expand=True)
return_book_button.pack(side=tk.LEFT, padx=5, pady=(20, 10), expand=True)

def on_resize(event):
    center_window(root, event.width, event.height)

root.bind("<Configure>", on_resize)

center_window(root, window_width, window_height)

root.mainloop()
