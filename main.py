import pyodbc 
from tkinter import *
from tkinter.ttk import Radiobutton
from tkinter.ttk import Combobox  
  
global unit, task, quality
global unit_, task_, quality_
cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=DESKTOP-F7CJPVG\MSSQLSERVER01;"
                      "Database=military;"
                      "Trusted_Connection=yes;")



first_str = 'Для заданного Подразделения на всех ФИОЧлЭкипажа,\n\
выполняющих заданную Задачу с качеством не ниже,\n\
чем по заданному классу, выдать учетные данные.' 
second_str = 'Для заданного Подразделения выдать ФИОЧлЭкипажа \nспособных выполнить любую Задачу в этом Подразделении\n\
с качеством не ниже, чем по заданному классу.'
fird_str = 'Для заданного Подразделения выдать ФИО  Командира и ФИОЧлЭкипажа'


def clicked():
    value = selected.get()

    if value == 1:
        global unit_, task_, quality_
        new_window = Tk()
        new_window.title("Запрос 1")  
        new_window.geometry('500x250')
        unit_ = StringVar(new_window)
        task_ = StringVar(new_window)
        quality_ = IntVar(new_window)
        combo_1 = Combobox(new_window, textvariable = unit_)
        combo_2 = Combobox(new_window, textvariable = task_)
        combo_3 = Combobox(new_window, textvariable = quality_)
        lbl_new_1 = Label(new_window, text="Подразделение")
        lbl_new_1.grid(column=0, row=0)
        combo_1['value'] = ('61', '62')  
        combo_1.current(0)  
        combo_1.grid(column=1, row=0)

        lbl_new_2 = Label(new_window, text="Задача")
        lbl_new_2.grid(column=0, row=1)
        combo_2['value'] = ('Наряд', 'Разработка ПО','Уборка КБО','Чистка автомата')  
        combo_2.current(0)  
        combo_2.grid(column=1, row=1)

        lbl_new_3 = Label(new_window, text="Классность")
        lbl_new_3.grid(column=0, row=2)    
        combo_3['value'] = (3, 2, 1)  
        combo_3.current(0)  
        combo_3.grid(column=1, row=2)

        btn_new = Button(new_window, text="Выполнить", command=query_1)
        btn_new.grid(column=0, row=3, sticky = 'w') 

        new_window.mainloop() 

    if value == 2:
        new_window = Tk()
        new_window.title("Запрос 2")  
        new_window.geometry('500x250')
        unit_ = StringVar(new_window)
        quality_ = IntVar(new_window)
        combo_1 = Combobox(new_window, textvariable = unit_)
        combo_3 = Combobox(new_window, textvariable = quality_)
        lbl_new_1 = Label(new_window, text="Подразделение")
        lbl_new_1.grid(column=0, row=0)
        combo_1['value'] = ('61', '62')  
        combo_1.current(0)  
        combo_1.grid(column=1, row=0)

        lbl_new_3 = Label(new_window, text="Классность")
        lbl_new_3.grid(column=0, row=2)    
        combo_3['value'] = (3, 2, 1)  
        combo_3.current(0)  
        combo_3.grid(column=1, row=1)

        btn_new = Button(new_window, text="Выполнить", command=query_2)
        btn_new.grid(column=0, row=2, sticky = 'w') 

        new_window.mainloop()

    if value == 3:
        new_window = Tk()
        new_window.title("Запрос 3")  
        new_window.geometry('500x250')
        unit_ = StringVar(new_window)
        
        combo_1 = Combobox(new_window, textvariable = unit_)
        
        lbl_new_1 = Label(new_window, text="Подразделение")
        lbl_new_1.grid(column=0, row=0)
        combo_1['value'] = ('61', '62')  
        combo_1.current(0)  
        combo_1.grid(column=1, row=0)

        btn_new = Button(new_window, text="Выполнить", command=query_3)
        btn_new.grid(column=0, row=1, sticky = 'w') 

        new_window.mainloop()




def query_1():
    s = ''
    global unit, quality
    unit = unit_.get()
    task = task_.get()
    quality = quality_.get()
    cursor = cnxn.cursor()
    cursor.execute("SELECT ФИО.ФИОЧлЭк, Классность, Подразделение FROM ФИО, Подразделение WHERE ФИО.ФИОЧлЭк = Подразделение.ФИОЧлЭк AND Подразделение = ? AND Задача = ? AND Классность <= ? AND Задействован = 'Да'", (unit, task, quality))
    result = cursor.fetchall()
    for row in result:
        print(row[0])
        s += row[0] + '(' + str(row[1]) + ')\n'
    print(s)
    window_result = Tk()  
    window_result.title("Результат")  
    lbl_result = Label(window_result, text=s)  
    lbl_result.grid(column=0, row=0, sticky = 'w')  
    window_result.mainloop()
    
    return  

def query_2():
    delete = []
    s = ''
    global unit, task, quality
    unit = unit_.get()
    quality = quality_.get()
    cursor = cnxn.cursor()
    cursor.execute("SELECT DISTINCT ФИО.ФИОЧлЭк FROM ФИО, Подразделение WHERE ФИО.ФИОЧлЭк = Подразделение.ФИОЧлЭк AND Подразделение.Подразделение = ? GROUP BY ФИО.ФИОЧлЭк HAVING COUNT(CASE WHEN ФИО.Классность<=? THEN 1 ELSE NULL END) = 4 ", (unit,quality))
    result = cursor.fetchall()
    for row in result:
        s += row[0] + '\n'
    print(s)
    window_result = Tk()  
    window_result.title("Результат")  
    lbl_result = Label(window_result, text=s)  
    lbl_result.grid(column=0, row=0, sticky = 'w')  
    window_result.mainloop()
    
    return

def query_3():
    s = ''
    global unit
    unit = unit_.get()
    cursor = cnxn.cursor()
    cursor.execute("SELECT DISTINCT ФИО.ФИОЧлЭк, Командир.Командир FROM ФИО, Командир, Подразделение WHERE ФИО.ФИОЧлЭк = Подразделение.ФИОЧлЭк AND Подразделение.Подразделение = Командир.Подразделение AND Подразделение.Подразделение = ?", (unit))
    result = cursor.fetchall()
    s += 'Командир:' + '\n' 
    s += result[0][1] + '\n'
    #for row in result:
        #s += row[1] + '\n'
    s += 'ФИОЧлЭк:' + '\n'
    for row in result:
        s += row[0] + '\n'
    print(s)
    window_result = Tk()  
    window_result.title("Результат")  
    lbl_result = Label(window_result, text=s)  
    lbl_result.grid(column=0, row=0, sticky = 'w')  
    window_result.mainloop()
    
    return

window = Tk()  
window.title("military")  
window.geometry('500x250')  
selected = IntVar()  
rad1 = Radiobutton(window,text=first_str, value=1, variable=selected)  
rad2 = Radiobutton(window,text=second_str, value=2, variable=selected)  
rad3 = Radiobutton(window,text=fird_str, value=3, variable=selected)  
btn = Button(window, text="Выбрать", command=clicked)    
rad1.grid(column=0, row=0, sticky = 'w')  
rad2.grid(column=0, row=4, sticky = 'w')  
rad3.grid(column=0, row=5, sticky = 'w')  
btn.grid(column=0, row=6, sticky = 'w')  
  
window.mainloop()

