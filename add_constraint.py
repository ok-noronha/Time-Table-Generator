from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import backend
import main_win

# It creates a GUI with a treeview widget that displays the contents of a database table
class AddConstraint :
    def __init__(self,db):
        """
        It creates a GUI with a treeview widget that displays the contents of a database table.

        :param db: the database connection
        """

        self.db = db
        self.root = Tk()

        self.root.minsize(800, 600)
        self.root.title("Add Constraint")
        #self.root.eval('tk::PlaceWindow . center')
        self.positionRight = int(self.root.winfo_screenwidth()/2 - 400)
        self.positionDown = int(self.root.winfo_screenheight()/2 - 300)
        self.root.geometry("+{}+{}".format(self.positionRight, self.positionDown))

        self.console = Frame(self.root)

        self.code_entry_label = Label(self.console, text="Course Code :")
        self.code_entry_label.grid(row=0, column=0, padx=5)

        self.code_entry = Entry(self.console, width=20)
        self.code_entry.grid(row=0, column=3, padx=5, pady=5)

        self.slot_entry_label = Label(self.console, text="Slot No:")
        self.slot_entry_label.grid(row=1, column=0, padx=5)

        self.slot_entry = Entry(self.console, width=20)
        self.slot_entry.grid(row=1, column=3, padx=5, pady=5)


        self.clss_entry_label = Label(self.console, text="Class :")
        self.clss_entry_label.grid(row=2, column=0, padx=5, pady=5)

        self.clss_entry = Entry(self.console, width=20)
        self.clss_entry.grid(row=2, column=3, padx=5, pady=5)

        self.add_Constraint_b = Button(self.console, text="Add Constraint", command=self.on_add_constraint)
        self.add_Constraint_b.grid(row=3, column=2, padx=10, pady=10, ipadx=10, ipady=5)

        self.del_Constraint_b = Button(self.console, text="Delete Constraint", command=self.on_del_constraint)
        self.del_Constraint_b.grid(row=3, column=5, padx=10, pady=10, ipadx=10, ipady=5)


        self.warning_label = Label(self.console, text="")
        self.warning_label.grid(row=4, column=2, padx=10, pady=10)

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

        self.tr_vw["columns"] = (1, 2, 3)
        self.tr_vw.column(1, width=90, anchor="c")
        self.tr_vw.column(2, width=90, anchor="c")
        self.tr_vw.column(3, width=90, anchor="c")

        self.tr_vw["show"] = "headings"
        self.tr_vw.heading(1, text="Course Code")
        self.tr_vw.heading(2, text="Slot No")
        self.tr_vw.heading(3, text="Class")

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
        self.row = self.db.get_constraint()
        self.tr_vw.delete(*self.tr_vw.get_children())
        if self.row is not None and len(self.row) != 0:
            for i in self.row:
                 self.tr_vw.insert("", "end", values=i)

    def on_add_constraint(self):
        code = self.code_entry.get()
        clss = self.clss_entry.get()
        slot = self.slot_entry.get()
        if code not in self.db.get_course(code=code)[0]:
            print(self.db.get_course(code=code)[0])
            print(self.db.get_course(code=code))
            self.warning_label["text"] = "*\tPlease Enter valid Course Code\t*"
            self.code_entry.delete(0, END)
            return
        if clss != self.db.get_clss(clss=clss)[0][0]:
            t="*\tPlease Enter valid Class Required\t*"
            self.warning_label["text"] = t
            self.clss_entry.delete(0, END)
            return
        if self.db.get_clss(clss=clss,code=code) is None:
            self.warning_label["text"] = "*\tPlease Enter valid Class-Course Relation\t*"
            self.code_entry.delete(0, END)
            self.clss_entry.delete(0, END)
            return

        if int(slot) not in backend.slotss:
            self.warning_label["text"] = "*\tPlease Enter valid Slot Code\t*"
            self.slot_entry.delete(0, END)
            return
        else:
            self.warning_label["text"] = ""
            if self.db.add_constraint(clss=clss,code=code,slot=slot):
                self.update_tree()
            else:
                self.warning_label["text"] = "*\tConstraint Already Exists\t*"

    def on_del_constraint(self):
        """
        It deletes a Constraint from the database.
        """
        self.curr_row = self.tr_vw.focus()
        self.contents = self.tr_vw.item(self.curr_row)
        self.info = self.contents["values"]
        self.db.delete_constraint(code=self.info[0], clss=self.info[2], slot=int(self.info[1]))
        self.update_tree()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            main_win.MainWindow(self.db)

if __name__ == '__main__':
    AddConstraint(backend.DataBase(0,0))