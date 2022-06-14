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
        self.root.title("Authentication")
        self.windowWidth = self.root.winfo_reqwidth()
        self.windowHeight = self.root.winfo_reqheight()
        self.positionRight = int(self.root.winfo_screenwidth()/2 - self.windowWidth)
        self.positionDown = int(self.root.winfo_screenheight()/2 - self.windowHeight)
        self.root.geometry("+{}+{}".format(self.positionRight, self.positionDown))
        Button(self.root, text="Reset", command=self.on_reset).grid(row=0, column=2, pady=5)
        self.id_entry_label = Label(self.root, text="User ID:")
        self.id_entry_label.grid(row=1, column=1, pady=5)
        self.id_entry = Entry(self.root, width=20)
        self.id_entry.grid(row=2, column=1, pady=5)
        self.password_entry_label = Label(self.root, text="Password:")
        self.password_entry_label.grid(row=3, column=1, pady=5)
        self.password_entry = Entry(self.root, width=20)
        self.password_entry.grid(row=4, column=1, padx=5)
        Label(self.root, text="  ").grid(row=5, column=1, pady=5)
        self.loginb = Button(text='Login',command=self.on_loginb)
        self.loginb.grid(row=6,column=2)
        self.signupb = Button(text='Sign Up',command=self.on_signupb)
        self.signupb.grid(row=6,column=0)
        self.forgotb = Button(self.root,text="Forgot Password?",command=self.on_forgotb)
        self.forgotb.grid(row=6,column=1)
        self.root.resizable(False,False)
        self.root.mainloop()

    def on_loginb(self):
        self.usrid=Hash(self.id_entry.get()).hash_value
        self.password=Hash(self.password_entry.get()).hash_value
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
        self.password=Hash(self.password_entry.get()).hash_value
        self.db = backend.DataBase(self.usrid,self.password)
        if(not self.db.check_id()):
            if(self.validate()):
                self.db = backend.DataBase(self.usrid,self.password)
                self.db.create_user()
                messagebox.showinfo("Account Created"," Try Logging in.")
            else:
                messagebox.showerror("Authentication failed", "Enter a valid user ID.")
        else:
            messagebox.showerror("Authentication failed", "User ID already exists.\n Try Logging in.")

    def validate(self):
        return True

    def on_reset(self):
        backend.reset_db()

    def on_forgotb(self):
        self.usrid=Hash(self.id_entry.get()).hash_value
        self.password=Hash(self.password_entry.get()).hash_value
        self.db = backend.DataBase(self.usrid,self.password)
        if(self.db.check_id()):
            self.db.set_password()
            messagebox.showinfo("Password Updated", self.password_entry.get()+" \n Try Logging in.")
        else:
            messagebox.showerror("Authentication failed", "User with Entered user ID not Found.")

if __name__ == '__main__':
    Authentication()
