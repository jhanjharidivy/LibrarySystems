import pandas
import mysql.connector as conn
import functions

con = conn.connect(host='localhost', user='root', password='root', database='library')
cursor = con.cursor()

# ESSENTIALS
cursor.execute("select * from members;")
members = pandas.DataFrame(cursor.fetchall(), columns=['ID', 'Name', 'Phone', 'Address'])
snomax = int(max(members.ID)[1:])
cursor.execute("select * from books;")
books = pandas.DataFrame(cursor.fetchall(), columns=['ID', 'Name', 'Genre', 'Cost', 'Issued To'])
admin = False


def fprint(*args):
    print()
    print(*args)


def main():
    global members, books, snomax
    while True:
        fprint("-" * 30)
        print("\t\tLIBRARY SYSTEMS")
        print("-" * 30)
        print("1. View Books")
        print("2. View Members")
        print("3. Register Member")
        print("4. Issue Books")
        print("5. Return Books")
        print("6. Exit Library")
        try:
            choice = int(input("Enter Choice : "))
            if choice == 1:
                fprint(books)
                input()
            elif choice == 2:
                fprint(members)
                input()
            elif choice == 3:
                functions.register_member()
            elif choice == 4:
                functions.issue_books()
            elif choice == 5:
                functions.return_books()
            elif choice == 6:
                fprint("Thank you for using our systems")
                break
            else:
                fprint("Enter a valid choice")
                continue
        except ValueError:
            fprint("Enter Integer Value!")


if __name__ == '__main__':
    main()
