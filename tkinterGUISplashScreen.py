

from tkinter.ttk import Progressbar
from tkinter import *

w = Tk()

width_of_window = 427
height_of_window = 250
screen_width = w.winfo_screenwidth()
screen_height = w.winfo_screenheight()
x_coordinate = (screen_width / 2) - (width_of_window / 2)
y_coordinate = (screen_height / 2) - (height_of_window / 2)
w.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))

w.overrideredirect(1)

s = ttk.Style()
s.theme_use('vista')
s.configure("red.Horizontal.TProgressbar")
progress = Progressbar(w, style="red.Horizontal.TProgressbar", orient=HORIZONTAL, length=500, mode='determinate', )


#############progressbar



def bar():
    l4 = Label(w, text='Loading...', fg='white', bg=a)
    lst4 = ('Calibri (Body)', 10)
    l4.config(font=lst4)
    l4.place(x=18, y=210)
    import time
    r = 0

    for i in range(100):
        progress['value'] = r
        w.update_idletasks()
        time.sleep(0.03)
        r = r + 1

    w.destroy()

def endLoop():
    print("hello")
    bar()

    

progress.place(x=-10, y=235)


a = '#972469'
Frame(w, width=427, height=241, bg=a).place(x=0, y=0)  # 249794


######## Label

l1 = Label(w, text='WELCOME', fg='white', bg=a)
lst1 = ('Calibri (Body)', 14, 'bold')
l1.config(font=lst1)
l1.place(x=50, y=80)

l2 = Label(w, text='TO', fg='white', bg=a)
lst2 = ('Calibri (Body)', 12)
l2.config(font=lst2)
l2.place(x=180, y=82)

l3 = Label(w, text='HUMAN EYE CONTROLLED MOUSE', fg='white', bg=a)
lst3 = ('Calibri (Body)', 12, 'bold')
l3.config(font=lst3)
l3.place(x=50, y=110)
w.after(3000, endLoop)
w.mainloop()


