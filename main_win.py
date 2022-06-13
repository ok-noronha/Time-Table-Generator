from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import backend
import auth_win


class MainWindow :
    def __init__(self,db,usrid):
        self.job_count = 0
        self.code_labels = {}
        self.code_panes = {}
        self.tt = []

        self.db=db

        self.root = Tk()
        self.root.minsize(800, 600)
        self.root.title("Time Table Generator")
        #self.root.eval('tk::PlaceWindow . center')
        self.positionRight = int(self.root.winfo_screenwidth()/2 - 400)
        self.positionDown = int(self.root.winfo_screenheight()/2 - 300)
        self.root.geometry("+{}+{}".format(self.positionRight, self.positionDown))

        self.main_frame = Frame(self.root)
        self.tt_frame = Frame(self.root)

        self.panel1 = PanedWindow(self.main_frame, orient=HORIZONTAL)
        self.panel1.pack(side=TOP, expand=1)
        self.panel2 = PanedWindow(self.main_frame, orient=VERTICAL)
        self.panel2.pack(side=TOP, expand=1)
        self.panel3 = PanedWindow(self.main_frame, orient=HORIZONTAL)
        self.panel3.pack(side=TOP, expand=1)

        self.warning_label = Label(self.panel1, text="*\t\t\t\t\t\t\t\t\t\t\t\t\t\t*")
        self.warning_label.pack()
        self.panel1.add(self.warning_label)

        self.deleteb = Button(self.panel1, text="Delete Account", command=self.on_delete)
        self.deleteb.pack(side=RIGHT,padx=35)
        self.panel1.add(self.deleteb)

        self.code_entry_label = Label(self.panel3, text="Course Code :")
        self.code_entry_label.grid(row=0, column=0, padx=5)
        self.panel3.add(self.code_entry_label)
        self.code_entry = Entry(self.panel3, width=20)
        self.code_entry.grid(row=0, column=1, padx=5)
        self.panel3.add(self.code_entry)
        self.hours_entry_label = Label(self.panel3, text="Hours Required :")
        self.hours_entry_label.grid(row=0, column=2, padx=5)
        self.panel3.add(self.hours_entry_label)
        self.hours_entry = Entry(self.panel3, width=20)
        self.hours_entry.grid(row=self.job_count + 0, column=3, padx=5)
        self.panel3.add(self.hours_entry)

        self.acb = Button(self.panel3, text="Add Course", command=self.on_add_course)
        self.acb.grid(row=1, column=4, padx=20)
        self.panel3.add(self.acb)
        self.el = Label(self.panel3, text=" ")
        self.el.grid(row=2, column=4, padx=20)
        self.panel3.add(self.el)
        self.rb = Button(self.panel3, text="Refresh", command=self.update_labels)
        self.rb.grid(row=3, column=4, padx=20)
        self.panel3.add(self.rb)
        self.sb = Button(self.panel3, text="Submit", command=self.on_submit)
        self.sb.grid(row=3, column=4, padx=20)
        self.panel3.add(self.sb)

        self.tt_frame.pack(side=BOTTOM, fill=X, expand=1, padx=90)
        self.main_frame.pack(side=TOP, fill=BOTH, expand=1)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.update_labels()
        self.root.mainloop()


    def on_x(self,button):
        if self.db.delete_course(self.code_labels[button]["text"]):
            self.code_panes[button].destroy()
            del self.code_panes[button]
            del self.code_labels[button]


    def update_labels(self):
        courses=self.db.get_courses()
        self.job_count = 0
        for x in self.code_labels.values():
            del x
        for x in self.code_panes.values():
            x.destroy()
            del x
        self.code_panes.clear()
        self.code_labels.clear()
        for course in courses:
            panel = PanedWindow(self.panel2, orient=HORIZONTAL)
            lbl = Label(panel, text=course[0])
            lbl.grid(row=self.job_count*10, column=0)
            panel.add(lbl)
            btn = Button(panel, text="X")
            btn.config(command=lambda button=btn: self.on_x(button))
            btn.grid(row=self.job_count*10, column=900)
            panel.add(btn)
            self.code_labels[btn] = lbl
            self.code_panes[btn] = panel
            panel.pack(side=TOP, expand=1)
            self.panel2.add(panel)
            self.job_count += 1

    def on_delete(self):
        self.db.delete_user()
        self.root.destroy()

    def on_add_course(self):
        code = self.code_entry.get()
        hours = self.hours_entry.get()
        if code == "" or len(code) > 8:
            self.warning_label["text"] = "\t\t\t\t\t\t\t*\tPlease Enter valid the Course Code\t*\t\t\t\t\t\t\t"
            self.code_entry.delete(8, END)
            return
        if hours == "" or (not hours.isdigit()):
            t="\t\t\\t\t\t\t\t*\tPlease Enter the Minimum Hours Required (integer)\t*\t\t\t\t\t\t\t"
            self.warning_label["text"] = t
            self.hours_entry.delete(0, END)

        else:
            self.warning_label["text"] = "*\t\t\t\t\t\t\t\t\t\t\t\t\t\t*"
            if self.db.add_course(code, hours):
                print()
            else:
                self.warning_label["text"] = "* Course Already Exists *"
        self.update_labels()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            auth_win.Authentication()

    def get_day(self,i):
        return "Sunday" if i == 0 else "Monday" if i==1 else "Tuesday" if i==2 else "Wednesday" if i==3 else "Thursday" if i==4 else "Friday" if i==5 else "Saturday"

    def gen_tt(self,jobs):
        self.tt = []
        for i in range(7):
            day=[]
            for j in range(8):
                lbl = Label(self.tt_frame,text=self.get_day(i)if j == 0 else "x")
                lbl.grid(row=i*300, column=j*200,columnspan=6,rowspan=4,padx=15,pady=5)
                day.append(lbl)
            self.tt.append(day)

        for job in jobs:
            code = job[1] if job[1] != None else "None"
            self.tt[int(job[0]/10)][int(job[0]%10)]["text"]=code

        Button(self.tt_frame,text="Reset Data",command=self.on_reset_data).grid(row=10*300, column=10*200,columnspan=6,rowspan=4,padx=15,pady=5)

    def on_submit(self):
        self.db.time_table()
        self.jobs = self.db.get_jobs()
        self.clear_tt()
        self.gen_tt(self.jobs)
        self.tt_frame.tkraise(aboveThis=self.main_frame)
        return

    def clear_tt(self):
        for r in self.tt:
            for c in r:
                c["text"]=" "

    def on_reset_data(self):
        self.db.create_user()
        self.update_labels()
