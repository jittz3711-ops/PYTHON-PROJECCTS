import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("library.db")   
cursor = conn.cursor()  

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(20),
        password VARCHAR(20),
        role VARCHAR(10)
    )
    ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(50),
        author VARCHAR(30),
        total_copies INTEGER,
        available_copies INTEGER
    )
    ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        user_id INTEGER,
        issue_date VARCHAR(20),
        due_date VARCHAR(20),
        return_date VARCHAR(20),
        status VARCHAR(10),
        FOREIGN KEY(book_id) REFERENCES Books(id),
        FOREIGN KEY(user_id) REFERENCES Users(id)
    )
    ''')

conn.commit()
conn.close()


#  REGISTER / LOGIN 

def registeruser():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    uname = input("enter username: - ")
    upass = input("enter password: - ")

    if uname == "" or upass == "":
        print("username/password cannot be empty")
        conn.close()
        return

    urole = input("register as (1)Admin or (2)Member: - ")
    if urole == "1":
        urole = "Admin"
    elif urole == "2":
        urole = "Member"
    else:
        print("invalid role choice")
        conn.close()
        return

    try:
        cursor.execute('''
            INSERT INTO Users(username,password,role)
            VALUES(?,?,?)
            ''', (uname, upass, urole))
        conn.commit()
        print("registration successful, you can login now")
    except sqlite3.IntegrityError:
        print("something went wrong, try again")
    except sqlite3.Error as e:
        print("database error:", e)

    conn.close()


def loginuser():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    uname = input("enter username: - ")
    upass = input("enter password: - ")

    try:
        cursor.execute('''
            SELECT * FROM Users WHERE username=? AND password=?
            ''', (uname, upass))
        user = cursor.fetchone()   #retrives a single row from the last executed query
    except sqlite3.Error as e:
        print("database error:", e)
        conn.close()
        return None

    conn.close()

    if user:
        print(f"login successful, welcome {user[1]} ({user[3]})")
        return user
    else:
        print("invalid username or password")
        return None



def addbook():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    btitle = input("enter book title: - ")
    bauthor = input("enter author name: - ")

    if btitle == "" or bauthor == "":
        print("title/author cannot be empty")
        conn.close()
        return

    try:
        bcopies = int(input("enter number of copies: - "))
        if bcopies <= 0:
            print("copies must be more than 0")
            conn.close()
            return
    except ValueError:
        print("please enter a valid number")
        conn.close()
        return

    try:
        cursor.execute('''
            INSERT INTO Books(title,author,total_copies,available_copies)
            VALUES(?,?,?,?)
            ''', (btitle, bauthor, bcopies, bcopies))
        conn.commit()
        print("book added successfully")
    except sqlite3.Error as e:
        print("database error:", e)

    conn.close()


def viewbooks():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM Books
        ''')
    books = cursor.fetchall()   
    conn.close()

    if books:
        print("\nID  Title                 Author            Total  Available")
        for i in books:
            print(f"{i[0]:<4}{i[1]:<22}{i[2]:<18}{i[3]:<7}{i[4]}")
        print()
    else:
        print("no books found\n")


def updatebook():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    viewbooks()
    try:
        b_id = int(input("enter book id to update: - "))
    except ValueError:
        print("invalid id")
        conn.close()
        return

    btitle = input("enter new title: - ")
    bauthor = input("enter new author: - ")

    try:
        cursor.execute('''
            UPDATE Books SET title=?, author=? WHERE id=?
            ''', (btitle, bauthor, b_id))
        if cursor.rowcount == 0:
            print("no book found with that id")
        else:
            conn.commit()
            print("book updated")
    except sqlite3.Error as e:
        print("database error:", e)

    conn.close()


def deletebook():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    viewbooks()
    try:
        b_id = int(input("enter book id to delete: - "))
    except ValueError:
        print("invalid id")
        conn.close()
        return

    ch = input("are you sure you want to delete this book\nY/N: - ").lower()
    if ch == "y":
        try:
            cursor.execute('''
                SELECT COUNT(*) FROM Transactions WHERE book_id=? AND status='Issued'
                ''', (b_id,))
            active = cursor.fetchone()[0]

            if active > 0:
                print("cannot delete, this book is currently issued to a member")
            else:
                cursor.execute('''
                    DELETE FROM Books WHERE id=?
                    ''', (b_id,))
                conn.commit()
                print("book deleted")
        except sqlite3.Error as e:
            print("database error:", e)
    else:
        print("book not deleted")

    conn.close()




def borrowbook(user):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    viewbooks()
    try:
        b_id = int(input("enter book id to borrow: - "))
    except ValueError:
        print("invalid id")
        conn.close()
        return

    try:
        cursor.execute('''
            SELECT * FROM Books WHERE id=?
            ''', (b_id,))
        book = cursor.fetchone()

        if not book:
            print("no book found with that id")
        elif book[4] <= 0:
            print("no copies available right now")
        else:
            idate = datetime.now().strftime("%Y-%m-%d")
            ddate = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

            cursor.execute('''
                INSERT INTO Transactions(book_id,user_id,issue_date,due_date,status)
                VALUES(?,?,?,?,?)
                ''', (b_id, user[0], idate, ddate, "Issued"))

            cursor.execute('''
                UPDATE Books SET available_copies = available_copies - 1 WHERE id=?
                ''', (b_id,))

            conn.commit()
            print(f"book borrowed successfully, return by {ddate}")

    except sqlite3.Error as e:
        print("database error:", e)

    conn.close()


def returnbook(user):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    viewmytransactions(user)
    try:
        t_id = int(input("enter transaction id to return: - "))
    except ValueError:
        print("invalid id")
        conn.close()
        return

    try:
        cursor.execute('''
            SELECT * FROM Transactions WHERE id=? AND user_id=?
            ''', (t_id, user[0]))
        txn = cursor.fetchone()

        if not txn:
            print("no such transaction found")
        elif txn[6] == "Returned":
            print("this book is already returned")
        else:
            rdate = datetime.now().strftime("%Y-%m-%d")
            cursor.execute('''
                UPDATE Transactions SET status='Returned', return_date=? WHERE id=?
                ''', (rdate, t_id))
            cursor.execute('''
                UPDATE Books SET available_copies = available_copies + 1 WHERE id=?
                ''', (txn[1],))
            conn.commit()
            print("book returned successfully")

    except sqlite3.Error as e:
        print("database error:", e)

    conn.close()


def viewmytransactions(user):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM Transactions WHERE user_id=?
        ''', (user[0],))
    rows = cursor.fetchall()
    conn.close()

    if rows:
        print("\nTxnID  BookID  Issued      Due         Returned    Status")
        for i in rows:
            print(f"{i[0]:<7}{i[1]:<8}{i[3]:<12}{i[4]:<12}{(i[5] or '-'):<12}{i[6]}")
        print()
    else:
        print("no transactions found\n")


def viewalltransactions():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT Transactions.id, Users.username, Books.title, Transactions.issue_date,
               Transactions.due_date, Transactions.return_date, Transactions.status
        FROM Transactions
        JOIN Users ON Transactions.user_id = Users.id
        JOIN Books ON Transactions.book_id = Books.id
        ''')
    rows = cursor.fetchall()
    conn.close()

    if rows:
        print("\nTxnID  User          Title                 Issued      Due         Returned    Status")
        for i in rows:
            print(f"{i[0]:<7}{i[1]:<14}{i[2]:<22}{i[3]:<12}{i[4]:<12}{(i[5] or '-'):<12}{i[6]}")
        print()
    else:
        print("no transactions found\n")


def viewmembers():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, username, role FROM Users
        ''')
    rows = cursor.fetchall()
    conn.close()

    print("\nID  Username        Role")
    for i in rows:
        print(f"{i[0]:<4}{i[1]:<16}{i[2]}")
    print()


# ---------------- MENUS ----------------

def adminmenu(user):
    while True:
        print("----- ADMIN MENU -----")
        print("1.Add Book\n2.View Books\n3.Update Book\n4.Delete Book\n5.View Members\n6.View All Transactions\n7.Logout")
        try:
            ch = int(input("enter choice: - "))
        except ValueError:
            print("invalid choice")
            continue

        if ch == 1:
            addbook()
        elif ch == 2:
            viewbooks()
        elif ch == 3:
            updatebook()
        elif ch == 4:
            deletebook()
        elif ch == 5:
            viewmembers()
        elif ch == 6:
            viewalltransactions()
        elif ch == 7:
            print("logging out...\n")
            break
        else:
            print("invalid option")


def membermenu(user):
    while True:
        print("----- MEMBER MENU -----")
        print("1.View Books\n2.Borrow Book\n3.Return Book\n4.My Transactions\n5.Logout")
        try:
            ch = int(input("enter choice: - "))
        except ValueError:
            print("invalid choice")
            continue

        if ch == 1:
            viewbooks()
        elif ch == 2:
            borrowbook(user)
        elif ch == 3:
            returnbook(user)
        elif ch == 4:
            viewmytransactions(user)
        elif ch == 5:
            print("logging out...\n")
            break
        else:
            print("invalid option")


def main():
    print("Welcome to Library Management System")
    while True:
        print("\n1.Register\n2.Login\n3.Exit")
        try:
            ch = int(input("enter choice: - "))
        except ValueError:
            print("invalid choice")
            continue

        if ch == 1:
            registeruser()
        elif ch == 2:
            user = loginuser()
            if user:
                if user[3] == "Admin":
                    adminmenu(user)
                else:
                    membermenu(user)
        elif ch == 3:
            print("Goodbye!")
            break
        else:
            print("invalid option")


main()