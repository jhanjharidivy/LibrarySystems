import main
import pandas
import mysql.connector as conn

con = conn.connect(host='localhost', user='root', password='root', database='library')
cursor = con.cursor()


def register_member():
    main.fprint("Enter Details of New Member :")
    print()
    ID = f"M{main.snomax + 1}"
    name = input("Enter Name : ")
    phone = input("Enter Phone Number : ")
    address = input("Enter Address : ")

    if len(name) <= 30 and (len(phone) == 10 and phone.isdigit()) and len(address) <= 50:
        cursor.execute(f"insert into members values ('{ID}', '{name}', '{phone}', '{address}');")
        con.commit()
        main.fprint(f"Member {name} successfully added to the database!")

        to_append = [ID, name, phone, address]
        ser = pandas.Series(to_append, index=main.members.columns)
        main.members = main.members.append(ser, ignore_index=True)
        main.snomax = int(max(main.members.ID)[1:])
    else:
        main.fprint("Wrong parameters entered")


def issue_books():
    print()
    memid = input("Enter Member ID : ")
    memidlist = list(main.members.ID)
    if memid not in memidlist:
        main.fprint("Member doesn\'t exists !")
    else:
        cursor.execute("select * from books where issued_to IS NULL;")
        avlbooks = pandas.DataFrame(cursor.fetchall(), columns=['ID', 'Name', 'Genre', 'Cost', 'Issued To'])
        main.fprint(avlbooks)
        print()
        to_issue = input("Enter book(s) ID to issue {separate by spaces if multiple} :")
        to_issue = to_issue.split()
        issue = True
        for x in to_issue:
            if x not in list(avlbooks.ID):
                main.fprint("Selected book(s) not available for issue !")
                issue = False
        if issue:
            for x in to_issue:
                cursor.execute(f"update books set issued_to='{memid}' where bookid='{x}';")
                con.commit()
                cursor.execute(f"select cost from books where bookid='{x}';")
                cost = cursor.fetchone()[0] // 10
                cursor.execute(f"insert into issued_books values('{x}', '{memid}', (select curdate()), {cost});")
                con.commit()
            main.fprint(f"Book(s) {','.join(to_issue)} issued to Member {memid}")


def return_books():
    cursor.execute("select * from issued_books;")
    issued = pandas.DataFrame(cursor.fetchall(), columns=['BookID', 'MemberID', 'Date', 'Cost'])
    main.fprint(issued)
    if issued.empty:
        main.fprint("No issued books available!")
    else:
        print()
        memid = input("Enter Member ID : ")
        memidlist = list(issued.MemberID)
        if memid not in memidlist:
            main.fprint(f"No books issued by member {memid}")
        else:
            cursor.execute(f"select * from issued_books where memid='{memid}';")
            membooks = pandas.DataFrame(cursor.fetchall(), columns=['BookID', 'MemberID', 'Date', 'Cost'])
            main.fprint(membooks)
            print()
            resp = input("Are you sure you want to return these books? (Y/N) : ")
            if resp.upper() == 'Y':
                cursor.execute(f"delete from issued_books where memid='{memid}';")
                con.commit()
                main.fprint(f"Returned books {', '.join([x for x in list(membooks.BookID)])}")
            else:
                main.fprint("Books not returned !")


if __name__ == '__main__':
    print("Execute main to access library")
