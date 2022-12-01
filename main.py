from peewee import MySQLDatabase, InternalError as PeeweeInternalError
from domain_models.book import Book
from apis.my_sql import LibraryModel
from repository.library import Library
from borb.pdf import *
from fpdf import FPDF



def add_book(lib):
    title = input("Введите название книги: ")
    author = input("Введите автора книги: ")
    year = input("Введите год издания книги: ")
    lib.add(book=Book(title, year, author))


def delete_book(lib):
    book_number = input("Введите ID книги которую необходимо удалить: ")
    book = lib.get_at(book_number)
    if not book:
        print("Книга не найдена")
        return
    lib.remove_at(book_number)
    print("Удалена книга ", book)


def update_book(lib):
    id = input("Введите ID книги которую необходимо изменить: ")
    book = lib.get_at(id)

    if not book:
        print("Книга не найдена")
        return
    print("Изменение книги ", book)
    title = input("Введите название книги (пусто, чтобы оставить без изменений): ")
    changed = False
    if title != "":
        book.title = title
        changed = True
    year = input("Введите год издания книги (пусто, чтобы оставить без изменений): ")
    if year != "":
        book.year = year
        changed = True
    author = input("Введите автора книги (пусто, чтобы оставить без изменений): ")
    if author != "":
        book.author = author
        changed = True
    if changed:
        lib.update_at(id, book)
        print("Книга изменена")
    else:
        print("Ничего не изменилось")


def count_books(lib):
    books = lib.get_all_books()
    print("Всего книг в библиотеке: ", len(books))


def find_books_year(lib):
    while True:
        year = input("Введите год для поиска или \"отмена-1\" : ")
        if year == "1":
            return None
        book = lib.find_by_year(year)
        if book != []:
            print("Найдено: ", book)
            return book
        else:
            print("Ничего не надено")


def find_books_author(lib):
    author = input("Введите автора для поиска или \"отмена-1\" : ")
    if author == "1":
        return None
    book = lib.find_by_author(author)
    if book != []:
        print("Найдено: ", book)
        return book
    else:
        print("Ничего не надено")


def find_books_title(lib):
    title = input("Введите название книги для поиска: ")
    if title == "1":
        return None
    book = lib.find_by_title(title)
    if book != []:
        print("Найдено: ", book)
        return book
    else:
        print("Ничего не надено")


def find_books(lib):
    search = input("Искать книги по году, автору или названию?\n(Укажите Год-1, Автор-2, Название-3): ")
    if search == "1":
        return find_books_year(lib)
    elif search == "2":
        return find_books_author(lib)
    elif search == "3":
        return find_books_title(lib)

    return None


def print_all_books(lib):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)

    t=lib.get_all_books()
    for x in t:
        for y in x:
            r=str(y)
            pdf.cell(20, 10, r, ln=1)

    pdf.output("vivod.pdf")
    pdf.close


if __name__ == '__main__':
    try:
        library = Library(data_base=MySQLDatabase('library', user='FOG', password='ilkaFOG29', host='localhost', port=3306))

        library.connect()
        while True:
            print('\nВведите:''\n'' Добавить-1;\n Удалить-2;\n Изменить-3;\n Найти-4;\n Счетчик книг-5;\n Вывести все книги-6;\n Выход-7: ')
            command = input()
            if command == "7":
                break
            elif command == "1":
                add_book(library)
            elif command == "2":
                delete_book(library)
            elif command == "3":
                update_book(library)
            elif command == "4":
                find_books(library)
            elif command == "5":
                count_books(library)
            elif command == "6":
                print_all_books(library)

        library.close()
    except PeeweeInternalError as px:
        print(str(px))
