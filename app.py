import tkinter as tk
import book_list
import add_book
import search_book
import lend_book
import delete_book
import check_availability
import return_book  

root = tk.Tk()
root.title("図書管理アプリ")

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

list_books_button = tk.Button(root, text="本の一覧", command=show_book_list)
add_book_button = tk.Button(root, text="本の登録", command=show_add_book)
search_book_button = tk.Button(root, text="本の検索", command=show_search_book)
lend_book_button = tk.Button(root, text="本の貸出", command=show_lend_book)
delete_book_button = tk.Button(root, text="本の削除", command=show_delete_book)
check_availability_button = tk.Button(root, text="貸出状況確認", command=show_check_availability)
return_book_button = tk.Button(root, text="本の返却", command=show_return_book)

list_books_button.pack()
add_book_button.pack()
search_book_button.pack()
lend_book_button.pack()
delete_book_button.pack()
check_availability_button.pack()
return_book_button.pack()

root.mainloop()
