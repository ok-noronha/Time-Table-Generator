from tkinter import *
from tkinter.ttk import *
import backend
from tkinter import messagebox

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
        self.root.eval('tk::PlaceWindow . center')

        self.main_frame = Frame(self.root)
        self.tt_frame = Frame(self.root)

        self.panel1 = PanedWindow(self.main_frame, orient=HORIZONTAL)
        self.panel1.pack(side=TOP, expand=1)
        self.panel2 = PanedWindow(self.main_frame, orient=VERTICAL)
        self.panel2.pack(side=TOP, expand=1)
        self.panel3 = PanedWindow(self.main_frame, orient=HORIZONTAL)
        self.panel3.pack(side=TOP, expand=1)

        self.warning_label = Label(self.panel1, text="*                               *")
        self.warning_label.pack()
        self.panel1.add(self.warning_label)

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
        self.el = Label(self.panel3, text="")
        self.el.grid(row=2, column=4, padx=20)
        self.panel3.add(self.el)
        self.sb = Button(self.panel3, text="Submit", command=self.on_submit)
        self.sb.grid(row=3, column=4, padx=20)
        self.panel3.add(self.sb)

        self.tt_frame.pack(side=BOTTOM, fill=X, expand=1, padx=90)
        self.main_frame.pack(side=TOP, fill=BOTH, expand=1)
        self.root.mainloop()



    def on_x(self,button):
        if self.db.delete_course(self.code_labels[button]["text"]):
            self.code_panes[button].destroy()
            del self.code_panes[button]
            del self.code_labels[button]


    def add_label(self, str):
        panel = PanedWindow(self.panel2, orient=HORIZONTAL)
        lbl = Label(panel, text=str)
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

    def on_add_course(self):
        code = self.code_entry.get()
        hours = self.hours_entry.get()
        if code == "" or len(code) > 8:
            self.warning_label["text"] = "* Please Enter valid the Course Code *"
            self.code_entry.delete(8, END)
            return
        if hours == "" or (not hours.isdigit()):
            self.warning_label["text"] = "* Please Enter the Minimum Hours Required (integer) *"
            self.hours_entry.delete(0, END)

        else:
            self.warning_label["text"] = "*                               *"
            if self.db.add_course(code, hours):
                self.add_label(code)
            else:
                self.warning_label["text"] = "* Course Already Exists *"

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

    def on_reset(self):
        self.db.reset_db()

    def on_submit(self):
        self.db.time_table()
        self.jobs = self.db.get_jobs()
        self.gen_tt(self.jobs)
        self.tt_frame.tkraise(aboveThis=self.main_frame)
        return