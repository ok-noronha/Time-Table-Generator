from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import backend
import auth_win
import add_class
import add_course
import add_constraint

class MainWindow():
    def __init__(self, db):
        self.root = Tk()
        self.db=db

        self.root.minsize(800, 600)
        self.root.title("Time Table Generator")
        self.positionRight = int(self.root.winfo_screenwidth()/2 - 400)
        self.positionDown = int(self.root.winfo_screenheight()/2 - 300)
        self.root.geometry("+{}+{}".format(self.positionRight, self.positionDown))

        self.add_class_b = Button(self.root, text="Add Class", command=self.on_add_class)
        self.add_class_b.pack(padx=10,pady=10)

        self.add_constraint_b = Button(self.root, text="Add Constraint", command=self.on_add_constraint)
        self.add_constraint_b.pack(padx=10,pady=10)

        self.add_course_b = Button(self.root, text="Add Course", command=self.on_add_course)
        self.add_course_b.pack(padx=10,pady=10)

        self.gen_tt_b = Button(self.root, text="Generate", command=self.on_gen_tt)
        self.gen_tt_b.pack(padx=10,pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_gen_tt(self):
        print("gent tt")

    def on_add_course(self):
        self.root.destroy()
        add_course.AddCourse(self.db)

    def on_add_constraint(self):
        self.root.destroy()
        add_constraint.AddConstraint(self.db)
        

    def on_add_class(self):
        self.root.destroy()
        add_class.AddClss(self.db)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            auth_win.Authentication()

if __name__ == '__main__':
    MainWindow(0)
