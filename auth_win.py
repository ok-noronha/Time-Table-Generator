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
        # This is the constructor of the class. It is called when you create an instance of the class.
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

    def on_signupb(self):
        """
        It checks if the user id exists in the database, if it doesn't, it creates a new user.
        """
        # Checking if the user id exists in the db.
        #TODO accept more details if necessary
        #note that the authentication window is useless
        self.usrid=Hash(self.id_entry.get()).hash_value
        self.password=Hash(self.password_entry.get()).hash_value
        self.db = backend.DataBase(self.usrid,self.password)
        if(not self.db.check_id()):
            if(self.validate()):
                self.db.create_user()
                messagebox.showinfo("Account Created"," Try Logging in.")
            else:
                messagebox.showerror("Authentication failed", "Enter a valid user ID.")
        else:
            messagebox.showerror("Authentication failed", "User ID already exists.\n Try Logging in.")

    def on_loginb(self):
        # Checking if the user id and password are correct.
        self.usrid=Hash(self.id_entry.get()).hash_value
        self.password=Hash(self.password_entry.get()).hash_value
        self.db = backend.DataBase(self.usrid,self.password)
        if(self.db.check_id()):
            if(self.db.check_password()):
                #db.reset_db()
                self.root.destroy()
                main_win.MainWindow(self.db)
            else:
                messagebox.showerror("Authentication failed", "Password Does not Match.")
        else:
            messagebox.showerror("Authentication failed", "User with Entered user ID not Found.")

    def on_forgotb(self):
        """
        It takes the user id and password from the entry boxes and then checks if the user id exists in
        the database. If it does, it updates the password in the database.
        """
        #TODO accept more details if necessary
        #TODO check format of usrid and password to be accepted
        #TODO any form of authentication
        self.usrid=Hash(self.id_entry.get()).hash_value
        self.password=Hash(self.password_entry.get()).hash_value
        self.db = backend.DataBase(self.usrid,self.password)
        if(self.db.check_id()):
            self.db.set_password()
            messagebox.showinfo("Password Updated", self.password_entry.get()+" \n Try Logging in.")
        else:
            messagebox.showerror("Authentication failed", "User with Entered user ID not Found.")

    def validate(self):
        """
        It checks the format of the usrid and password to be accepted.
        :return: The return value is a boolean value.
        """
        #TODO check format of usrid and password to be accepted
        return True

    def on_reset(self):
        """
        It resets the database.
        """
        backend.reset_db()

if __name__ == '__main__':
    Authentication()
