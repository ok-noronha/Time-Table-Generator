import tkinter
import sqlite3

root = tkinter.Tk()
root.geometry("400x300")
root.title("LALAS")
root.config(bg="light blue")


em_c = tkinter.StringVar()
pcode_c = tkinter.StringVar()
nm_c = tkinter.StringVar()

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


def create():

    another_f = tkinter.Frame(root, relief="raised", border=4, bg="green")
    another_f.grid(row=1, column=0, columnspan=2, sticky="new")

    name = tkinter.Label(another_f, text="Name(in caps)", fg="white", bg="green")
    name.config(font=("Franklin Gothic Medium", 12))
    name.grid(row=0, column=0, sticky="w", padx=4)

    name_blank = tkinter.Entry(another_f, textvariable=nm_c, relief="sunk", border=4)
    name_blank.grid(row=0, column=1, padx=4)

    email_c = tkinter.Label(another_f, text="Email/Phone no.", fg="white", bg="green")
    email_c.config(font=("Franklin Gothic Medium", 12))
    email_c.grid(row=1, column=0, sticky="w", padx=4)

    email_c_b = tkinter.Entry(another_f, textvariable=em_c, relief="sunk", border=4)
    email_c_b.grid(row=1, column=1, padx=4)

    password_c = tkinter.Label(another_f, text="password", fg="white", bg="green")
    password_c.config(font=("Franklin Gothic Medium", 12))
    password_c.grid(row=2, column=0, sticky="w", padx=4)

    password_c_b = tkinter.Entry(another_f, textvariable=pcode_c, relief="sunk", border=4)
    password_c_b.grid(row=2, column=1, padx=4)

    ok_c = tkinter.Button(another_f, text="Confirm", relief="raised", border=4, command=two)
    ok_c.grid(row=3, column=4, sticky="e")

    cancel_c = tkinter.Button(another_f, text="Cancel", relief="raised", border=4, command=root.quit)
    cancel_c.grid(row=3, column=5, sticky="w")

    another_f.tkraise()


def two():
    cp()
    login()


def login():

    lable = tkinter.Label(root, text="Welcome to LALAS", fg="red", bg="light blue")
    lable.config(font=("Comic Sans MS", 20))
    lable.grid(row=0, column=0, columnspan=2, sticky="new")

    iden = tkinter.Frame(root, relief="raised", border=4, bg="green")
    iden.grid(row=1, column=0, columnspan=2, sticky="new")

    email = tkinter.Label(iden, text="Email/phone no.", fg="white", bg="green")
    email.config(font=("Franklin Gothic Medium", 12))
    email.grid(row=0, column=0)

    blank1 = tkinter.Entry(iden, textvariable=em_c, relief="sunk", border=4)
    blank1.grid(row=0, column=1, sticky="we")

    password = tkinter.Label(iden, text="Password", fg="white", bg="green")
    password.config(font=("Franklin Gothic Medium", 12))
    password.grid(row=4, column=0, sticky="ws")

    blank2 = tkinter.Entry(iden, textvariable=pcode_c, relief="sunk", border=4)
    blank2.grid(row=4, column=1, sticky="we")

    okbutton = tkinter.Button(iden, text="Login", relief="raised", border=4, command=data)
    okbutton.grid(row=7, column=5, sticky="se")

    canclebutton = tkinter.Button(iden, text="Cancel", relief="raised", border=4, command=root.quit)
    canclebutton.grid(row=7, column=6, sticky="ws")

    sign = tkinter.Button(iden, text="Create account", relief="raised", border=4, command=create)
    sign.grid(row=8, column=0, sticky="we")


def final():

    fram_f = tkinter.Frame(root, bg="grey")
    fram_f.grid(row=0, column=0, rowspan=4, columnspan=4, sticky="news")
    lable_f = tkinter.Label(fram_f, text="Successfully Login in LALAS account", fg="green", bg="grey")
    lable_f.config(font=("Comic Sans MS", 16))
    lable_f.grid(row=0, column=0, rowspan=5, padx=20, pady=100, columnspan=5, sticky="we")


def found():

    fram_f = tkinter.Frame(root, bg="light blue")
    fram_f.grid(row=0, column=0, rowspan=4, columnspan=4, sticky="news")
    lable_f = tkinter.Label(fram_f, text="Account Not Found", fg="red", bg="light blue")
    lable_f.config(font=("Comic Sans MS", 16))
    lable_f.grid(row=0, column=0, rowspan=5, padx=20, pady=100, columnspan=5, sticky="we")
    sign = tkinter.Button(fram_f, text="<<Back", relief="raised", border=4, command=login)
    sign.grid(row=3, column=0, sticky="we")


"""Data base work start"""

db = sqlite3.connect("lalas2.sqlite")
db.execute("CREATE table if not exists lalas2(name TEXT NOT NULL, email TEXT NOT NULL, password TEXT)")


def data():

    cursor = db.cursor()
    yo = ""
    for i in em_c.get():
        yo += i
    cursor.execute("SELECT email, password from lalas2 WHERE email=? And password=?", (yo, pcode_c.get()))

    row = cursor.fetchone()
    if row:
        final()
    else:
       found()


def cp():
    cu = db.cursor()
    cu.execute("INSERT into lalas2 VALUES(?,?,?)", (nm_c.get(), em_c.get(), pcode_c.get(),))
    cu.connection.commit()


login()

tkinter.mainloop()
