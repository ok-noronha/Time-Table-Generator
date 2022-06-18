from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import backend
import main_win

# It creates a GUI with a treeview widget that displays the contents of a database table
class AddClss :
    def __init__(self,db):
        """
        It creates a GUI with a treeview widget that displays the contents of a database table.

        :param db: the database connection
        """

        self.db = db
        self.root = Tk()

        self.root.minsize(800, 600)
        self.root.title("Add class")
        #self.root.eval('tk::PlaceWindow . center')
        self.positionRight = int(self.root.winfo_screenwidth()/2 - 400)
        self.positionDown = int(self.root.winfo_screenheight()/2 - 300)
        self.root.geometry("+{}+{}".format(self.positionRight, self.positionDown))

        self.console = Frame(self.root)

        self.clss_entry_label = Label(self.console, text="Class :")
        self.clss_entry_label.grid(row=0, column=0, padx=5)

        self.clss_entry = Entry(self.console, width=20)
        self.clss_entry.grid(row=0, column=3, padx=5, pady=5)

        self.code_entry_label = Label(self.console, text="Course Code :")
        self.code_entry_label.grid(row=1, column=0, padx=5, pady=5)

        self.code_entry = Entry(self.console, width=20)
        self.code_entry.grid(row=1, column=3, padx=5, pady=5)

        self.add_clss_b = Button(self.console, text="Add Class", command=self.on_add_clss)
        self.add_clss_b.grid(row=2, column=2, padx=10, pady=10, ipadx=10, ipady=5)

        self.del_clss_b = Button(self.console, text="Delete Class", command=self.on_del_clss)
        self.del_clss_b.grid(row=2, column=5, padx=10, pady=10, ipadx=10, ipady=5)


        self.warning_label = Label(self.console, text="")
        self.warning_label.grid(row=3, column=2, padx=10, pady=10)

        col_count, row_count = self.console.grid_size()

        for col in range(col_count):
            self.console.grid_columnconfigure(col, minsize=40)

        for row in range(row_count):
            self.console.grid_rowconfigure(row, minsize=40)

        self.tree_frame = Frame(self.root)

        self.scrl = Scrollbar(self.tree_frame, orient=VERTICAL)

        self.tr_vw = Treeview(
            self.tree_frame,
            selectmode="browse",
            yscrollcommand=self.scrl.set,
        )
        self.scrl.config(command=self.tr_vw.yview)

        self.tr_vw["columns"] = (1, 2)
        self.tr_vw.column(1, width=90, anchor="c")
        self.tr_vw.column(2, width=90, anchor="c")

        self.tr_vw["show"] = "headings"
        self.tr_vw.heading(1, text="Class")
        self.tr_vw.heading(2, text="Course")

        self.scrl.pack(side=RIGHT, fill=Y)
        self.tr_vw.pack(side=LEFT, fill=BOTH, expand=1)

        self.tree_frame.pack(fill=BOTH, expand=1)
        self.console.pack(side=BOTTOM, fill=X, expand=0)
        self.update_tree()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def update_tree(self):
        """
        It deletes all the rows in the treeview and then inserts all the rows from the database.
        """
        self.row = self.db.get_clss()
        self.tr_vw.delete(*self.tr_vw.get_children())
        if len(self.row) != 0:
            for i in self.row:
                 self.tr_vw.insert("", "end", values=i)

    def on_add_clss(self):
        """
        It takes the input from the user and checks if it is valid, if it is valid it adds it to the
        database and updates the treeview.
        :return: The return value of the function is the value of the last expression evaluated.
        """
        clss = self.clss_entry.get()
        code = self.code_entry.get()
        if clss == "" or len(clss) > 8:
            self.warning_label["text"] = "*\tPlease Enter valid Class\t*"
            self.clss_entry.delete(8, END)
            return
        if code == "" or (self.db.get_course(code=code) is None):
            t="*\tPlease Enter the valid Course Code Required\t*"
            self.warning_label["text"] = t
            self.code_entry.delete(0, END)

        else:
            self.warning_label["text"] = ""
            if self.db.add_clss(clss, code):
                self.update_tree()
            else:
                self.warning_label["text"] = "*\tClass-Code Already Exists\t*"

    def on_del_clss(self):
        """
        It deletes a clss from the database.
        """
        self.curr_row = self.tr_vw.focus()
        self.contents = self.tr_vw.item(self.curr_row)
        self.info = self.contents["values"]
        #self.db.delete_clss(clss=self.info[0], code=self.info[1])
        self.db.delete_clss(clss=self.info[0])
        self.update_tree()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            main_win.MainWindow(self.db)

if __name__ == '__main__':
    AddClss(backend.DataBase(0,0))
