from tkinter import*
import tkinter

root = Tk()
root.geometry('900x500')


var_a = DoubleVar()
var_b = DoubleVar()

############# CREATING PANELS #####################
#----------- General Panel  --------------#
panel_1 = PanedWindow(bd=4,orient = HORIZONTAL ,relief="raised")#, bg = "red")
panel_1.pack(fill=BOTH, expand=1)
#----------- Fist Panel  --------------#
panel_3 = PanedWindow(panel_1, orient = VERTICAL, relief="raised")#, bg = "yellow")
panel_1.add(panel_3, minsize=200) #inserting on panel_1
#----------- Second Panel  --------------#
panel_2 = PanedWindow(panel_1, orient = VERTICAL, relief="raised")#, bg = "blue")
panel_1.add(panel_2, minsize=800) #inserting on panel_1


label2=Label(panel_3,text="Pass the cursor below me")
panel_3.add(label2)

textbox2=Scale(panel_3,orient=HORIZONTAL,variable = var_a)
panel_3.add(textbox2)

label4=Label(panel_3,text="Pass the cursor above me too")
panel_3.add(label4)

textbox4=Scale(panel_3,orient=HORIZONTAL,variable = var_b)
panel_3.add(textbox4)



def bla():
    pass
button1 = Button(panel_3,text="Why I have this size?", height = 0, width = 0, command= bla())
panel_3.add(button1)
button1.pack(fill=X, expand=1) # Only fits in X (horizontal direction), expands according to the panel




tkinter.mainloop()
