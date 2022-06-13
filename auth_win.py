from tkinter import *
from tkinter.ttk import *
import backend
import main_win
from tkinter import messagebox

class Hash:
    def __init__(self, s: str):
        self.hash_value = 0
        self.p, self.m = 31, 10**9 + 7
        self.length = len(s)
        hash_so_far = 0
        p_pow = 1
        for i in range(self.length):
            hash_so_far = (hash_so_far + (1 + ord(s[i]) - ord('a')) * p_pow) % self.m
            p_pow = (p_pow * self.p) % self.m
        self.hash_value = hash_so_far

    def __eq__(self, other):
        return self.hash_value == other.hash_value

class Authentication:
    def __init__(self):
        self.usrid=0
        self.password=0
        self.db=None
        self.root = Tk()
        self.id_entry_label = Label(self.root, text="User ID:")
        self.id_entry_label.grid(row=0, column=1, pady=5)
        self.id_entry = Entry(self.root, width=20)
        self.id_entry.grid(row=1, column=1, pady=5)
        self.password_entry_label = Label(self.root, text="Password:")
        self.password_entry_label.grid(row=2, column=1, pady=5)
        self.password_entry = Entry(self.root, width=20)
        self.password_entry.grid(row=3, column=1, padx=5)
        self.loginb = Button(text='Login',command=self.on_loginb)
        self.loginb.grid(row=4,column=2)
        self.signupb = Button(text='Sign Up',command=self.on_signupb)
        self.signupb.grid(row=4,column=0)
        self.root.mainloop()

    def on_loginb(self):
        self.usrid=Hash(self.id_entry.get())
        self.password=Hash(self.id_entry.get())
        self.db = backend.DataBase(self.usrid,self.password)
        if(self.db.check_id()):
            if(self.db.check_password()):
                #db.reset_db()
                self.root.destroy()
                main_win.MainWindow(backend.DataBase(self.usrid,self.password),self.usrid)
            else:
                messagebox.showerror("Authentication failed", "Password Does not Match.")
        else:
            messagebox.showerror("Authentication failed", "User with Entered user ID not Found.")

    def on_signupb(self):
        self.usrid=Hash(self.id_entry.get()).hash_value
        self.password=Hash(self.id_entry.get()).hash_value
        self.db = backend.DataBase(self.usrid,self.password)
        if(not self.db.check_id()):
            if(self.check()):
                self.db = backend.DataBase(self.usrid,self.password)
                self.db.create_user()
            else:
                messagebox.showerror("Authentication failed", "Enter a valid user ID.")
        else:
            messagebox.showerror("Authentication failed", "User ID already exists.")

    def check(self):
        return True







if __name__ == '__main__':
    Authentication()
