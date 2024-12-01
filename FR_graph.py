# Import Module
from tkinter import *
import FR_graph_body
from FR_graph_body import Parse


# create root window
root = Tk()
a=''
b=''
c=''

# root window title and dimension
root.title("Парсинг Федресурс")
# Set geometry(widthxheight)
root.geometry('500x200')

# adding menu bar in root window
# new item in menu bar labelled as 'New'
# adding more items in the menu bar 
menu = Menu(root)
item = Menu(menu)
item.add_command(label='New')
menu.add_cascade(label='File', menu=item)
root.config(menu=menu)

# adding a label to the root window
lbl1 = Label(root, text = "Введите ИНН лизингодателя:")
lbl1.grid()

# adding Entry Field
txt1 = Entry(root, width=10)
txt1.grid(column =1, row =0)

def clicked1():
    a=txt1.get()
    res1 = "Записан ИНН: " + a
    lbl1.configure(text = res1)
    return a

# button widget with red color text inside
#btn1 = Button(root, text = "Записать" ,
#             fg = "black", command=clicked1)
# Set Button Grid
#btn1.grid(column=2, row=0)



# adding a label to the root window
lbl2 = Label(root, text = "Введите начальную дату интервала (ЧЧ.ММ.ГГГГ):")
lbl2.grid(column =0, row =2)

# adding Entry Field
txt2 = Entry(root, width=10)
txt2.grid(column =1, row =2)

def clicked2():
    b = txt2.get()
    res2 = "Записана начальная дата: " + b
    lbl2.configure(text = res2)
    return b

# button widget with red color text inside
#btn2 = Button(root, text = "Записать" ,
#             fg = "black", command=clicked2)
# Set Button Grid
#btn2.grid(column=2, row=2)





# adding a label to the root window
lbl3 = Label(root, text = "Введите конечную дату интервала (ЧЧ.ММ.ГГГГ):")
lbl3.grid(column =0, row =4)

# adding Entry Field
txt3 = Entry(root, width=10)
txt3.grid(column =1, row =4)

def clicked3():
    c=txt3.get()
    res3 = "Записана конечная дата: " + c
    lbl3.configure(text = res3)
    return c

# button widget with red color text inside
#btn3 = Button(root, text = "Записать" ,
#             fg = "black", command=clicked3)
# Set Button Grid
#btn3.grid(column=2, row=4)


lbl4 = Label(root, text = "Парсинг:")
lbl4.grid(column =0, row =8)

def clicked4():
    a=txt1.get()
    b=txt2.get()
    c=txt3.get()
    print(a,b,c)
    obj=Parse(a, b, c)
    res4 = obj.Body()
    lbl4.configure(text = res4)

# button widget with red color text inside
btn4 = Button(root, text = "Выполнить парсинг" ,
             fg = "black", command=clicked4)
# Set Button Grid
btn4.grid(column=1, row=8)



# Execute Tkinter
root.mainloop()





