import pickle
import csv
import datetime
import os
import sys
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

root = tk.Tk()
root.geometry("1980x1080")
root.title("Finance app")
root.attributes("-fullscreen", True)

folder_name = "DATA"
os.makedirs(folder_name, exist_ok=True)

if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

try:
    with open(os.path.join(base_dir, "WALLPAPERS", "wallfile.bin"), "rb") as currWall:
        wallname = pickle.load(currWall)
    iconame = os.path.join(base_dir,"app.ico")
except FileNotFoundError:
    wallname = os.path.join(base_dir, "WALLPAPERS", "DEFAULTWALL.jpg")
    iconame = os.path.join(base_dir,"app.ico")
image = Image.open(wallname)   # make sure this file is in the same folder OR use full path
image = image.resize((1980, 1080))       # resize to match window
bg_photo = ImageTk.PhotoImage(image)
root.iconbitmap(iconame)

current_time = datetime.date.today()

def days():
    today = datetime.date.today()
    date = today.day
    monthname = today.strftime("%B")
    year = today.year
    d = [date, monthname, year]
    return d

def clearwidgets():
    global bg_label
    for widget in root.winfo_children():
        widget.destroy()
    # Create background label
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo  # <- keep reference!
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

def btncolcng_hover(e,switch):
    switch["background"] = "blue"
    switch["foreground"] = "lightblue"

def btncolcng_leave(e,switch):
    switch["background"] = "SystemButtonFace"
    switch["foreground"] = "black"

def checknpass():
    p = nentry.get()
    cp = centry.get()
    name = nameentry.get()
    try:
        with open (os.path.join(base_dir,"DATA", "ps.bin"),"rb") as red:
            save = pickle.load(red)
    except:
        save = {}
    save[name] = p
    clearwidgets()
    # check Password
    if name=='' or p=='' or cp=='':
        label_prompt4 = tk.Label(root, text="ONE OR ENTRIES MISSING!!")
        label_prompt4.pack(pady=5)
        crlogbtn = tk.Button(root, text="TRY AGAIN", command=createuser)
        crlogbtn.pack(pady=10)
        crlogbtn.bind("<Enter>",lambda e,b=crlogbtn: btncolcng_hover(e,b))
        crlogbtn.bind("<Leave>",lambda e,b=crlogbtn: btncolcng_leave(e,b))
    else:
        if (p == cp):
            with open (os.path.join(base_dir,"DATA", "ps.bin"),"wb") as create:
                pickle.dump(save, create)
            label_prompt4 = tk.Label(root, text="USER CREATED")
            label_prompt4.pack(pady=5)
            trylogbtn = tk.Button(root, text="TRY LOGIN", command=login)
            trylogbtn.pack(pady=10)
            trylogbtn.bind("<Enter>",lambda e,b=trylogbtn: btncolcng_hover(e,b))
            trylogbtn.bind("<Leave>",lambda e,b=trylogbtn: btncolcng_leave(e,b))
            root.bind('<Return>', lambda event: trylogbtn.invoke())
        else:
            label_prompt4 = tk.Label(root, text="PASSWORD DOES NOT MATCH!")
            label_prompt4.pack(pady=5)
            crlogbtn = tk.Button(root, text="TRY AGAIN", command=createuser)
            crlogbtn.pack(pady=10)
            crlogbtn.bind("<Enter>",lambda e,b=crlogbtn: btncolcng_hover(e,b))
            crlogbtn.bind("<Leave>",lambda e,b=crlogbtn: btncolcng_leave(e,b))
            root.bind('<Return>', lambda event: crlogbtn.invoke())
      
def createuser():
    clearwidgets()
    global nameentry, nentry, centry
    # Enter name
    label_prompt1 = tk.Label(root, text="NAME")
    label_prompt1.pack(pady=(250,5))
    nameentry = tk.Entry(root, width=25)
    nameentry.pack(pady=0)
    # Enter Password
    label_prompt2 = tk.Label(root, text="PASSWORD")
    label_prompt2.pack(pady=5)
    nentry = tk.Entry(root, show="*",width=25)
    nentry.pack(pady=0)
    # Enter Confirm Password
    label_prompt3 = tk.Label(root, text="CONFIRM PASSWORD")
    label_prompt3.pack(pady=5)
    centry = tk.Entry(root, show="*", width=25)
    centry.pack(pady=0)

    button = tk.Button(root, text="CREATE", command=checknpass)
    button.pack(pady=10)
    backbtn = tk.Button(root, bg="red", text="Back", command=login)
    backbtn.pack(pady=10)
    button.bind("<Enter>",lambda e,b=button: btncolcng_hover(e,b))
    button.bind("<Leave>",lambda e,b=button: btncolcng_leave(e,b))
    root.bind('<Return>', lambda event: button.invoke())

def income():
    clearwidgets()
    global scombo, aentry2

    label = tk.Label(root, text="INCOME ENTRY",font=("Times New Roman", 30, "bold"))
    label.pack(pady=(250,20))

    alabel_prompt = tk.Label(root, text="Enter Amount")
    alabel_prompt.pack(pady=5)

    aentry2 = tk.Entry(root, width=25)
    aentry2.pack(pady=0)

    slabel_prompt = tk.Label(root, text="Enter Source")
    slabel_prompt.pack(pady=5)

    sources = ['SALARY','BUSINESS','LOAN','GIFT','OTHER INVESTMENTS']

    scombo = ttk.Combobox(root, values=sources, state="readonly")  
    scombo.set("Select source of income")  # default text
    scombo.pack(pady=20)  

    button = tk.Button(root, text="Enter", command=incomeentry)
    button.pack(pady=10)
    button.bind("<Enter>",lambda e,b=button: btncolcng_hover(e,b))
    button.bind("<Leave>",lambda e,b=button: btncolcng_leave(e,b))

    backbtn = tk.Button(root, bg="red", text="Back", command=Features)
    backbtn.pack(pady=10)

    root.bind('<Return>', lambda event: button.invoke())

def incomeentry():
    source = scombo.get()
    amount = aentry2.get()
    day = days()
    data = [source, amount, datetime.date.today()]
    if (source=='' or amount==''):
        clearwidgets()
        label = tk.Label(root, text = "NO DATA ENTERED",font=("Times New Roman", 30, "bold"))
        label.pack(pady = (300,20))
        conbtn = tk.Button(root, text="TRY AGAIN", command=outgo)
        conbtn.pack(pady=10)
        conbtn.bind("<Enter>",lambda e,b=conbtn: btncolcng_hover(e,b))
        conbtn.bind("<Leave>",lambda e,b=conbtn: btncolcng_leave(e,b))
    else:
        with open (os.path.join(base_dir,"DATA", f"{day[1]}{day[2]}income_{username}.csv"), 'a', newline='') as inputer:
            writer = csv.writer(inputer)
            writer.writerow(data)
        label = tk.Label(root, text = f"Income data: SOURCE - {source}, AMOUNT - {amount}, DATE -  {day[1]} {day[0]} {day[2]}")
        label.pack(pady = 5)
        conbtn = tk.Button(root, text="CONTINUE", command=Features)
        conbtn.pack(pady=10)
        conbtn.bind("<Enter>",lambda e,b=conbtn: btncolcng_hover(e,b))
        conbtn.bind("<Leave>",lambda e,b=conbtn: btncolcng_leave(e,b))
        root.bind('<Return>', lambda event: conbtn.invoke())

def outgo():
    clearwidgets()
    global rcombo, aentry2

    label = tk.Label(root, text="OUTGO ENTRY",font=("Times New Roman", 30, "bold"))
    label.pack(pady=(250,20)) 

    alabel_prompt = tk.Label(root, text="Enter Amount")
    alabel_prompt.pack(pady=5)

    aentry2 = tk.Entry(root, width=25)
    aentry2.pack(pady=0)

    reasons = ['RENT','FOOD','BUSINESS','OTHER INVESTMENTS', 'GIFT', 'CHARITY','PERSONAL','TRAVEL','VACATION']

    rcombo = ttk.Combobox(root, values=reasons, state="readonly")  
    rcombo.set("Select source of income")  # default text
    rcombo.pack(pady=20)

    button = tk.Button(root, text="Enter", command=outgoentry)
    button.pack(pady=10)

    backbtn = tk.Button(root, bg="red", text="Back", command=Features)
    backbtn.pack(pady=10)

    root.bind('<Return>', lambda event: button.invoke())

def outgoentry():
    reason = rcombo.get()
    amount = aentry2.get()
    day = days()
    data = [reason, amount, datetime.date.today()]
    if (reason=='' or amount==''):
        clearwidgets()
        label = tk.Label(root, text = "NO DATA ENTERED",font=("Times New Roman", 30, "bold"))
        label.pack(pady = (300,20))
        conbtn = tk.Button(root, text="TRY AGAIN", command=outgo)
        conbtn.pack(pady=10)
        conbtn.bind("<Enter>",lambda e,b=conbtn: btncolcng_hover(e,b))
        conbtn.bind("<Leave>",lambda e,b=conbtn: btncolcng_leave(e,b))
    else:
        with open (os.path.join(base_dir,"DATA", f"{day[1]}{day[2]}outgo_{username}.csv"), 'a', newline='') as inputer:
            writer = csv.writer(inputer)
            writer.writerow(data)
        label = tk.Label(root, text = f"Income data: REASON - {reason}, AMOUNT - {amount}, DATE -  {day[1]} {day[0]} {day[2]}")
        label.pack(pady = 5)
        conbtn = tk.Button(root, text="CONTINUE", command=Features)
        conbtn.pack(pady=10)
        conbtn.bind("<Enter>",lambda e,b=conbtn: btncolcng_hover(e,b))
        conbtn.bind("<Leave>",lambda e,b=conbtn: btncolcng_leave(e,b))
        root.bind('<Return>', lambda event: conbtn.invoke())

def transac1():
    clearwidgets()
    label_prompt = tk.Label(root, text="TRANSACTION",font=("Times New Roman", 30, "bold"))
    label_prompt.pack(pady=(250,10))
    ibutton = tk.Button(root, text="INCOME", command=transaci)
    ibutton.pack(pady=10)
    ibutton.bind("<Enter>",lambda e,b=ibutton: btncolcng_hover(e,b))
    ibutton.bind("<Leave>",lambda e,b=ibutton: btncolcng_leave(e,b))
    obutton = tk.Button(root, text="OUTGO", command=transaco)
    obutton.pack(pady=10)
    obutton.bind("<Enter>",lambda e,b=obutton: btncolcng_hover(e,b))
    obutton.bind("<Leave>",lambda e,b=obutton: btncolcng_leave(e,b))
    backbtn = tk.Button(root, bg="red", text="BACK", command=Features)
    backbtn.pack(pady=10)

def transaci():
    clearwidgets()
    global imoncombo, iyecombo
    yearop = list(range(current_time.year, 1999, -1))
    monthop = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    label = tk.Label(root, text = "SELECT MONTH AND YEAR", font=("Times New Roman", 30, "bold"))
    label.pack(pady = (250,10))
    frame = tk.Frame(root,bg="")
    frame.pack(pady=10)

    imoncombo = ttk.Combobox(frame, values=monthop, state="readonly")  # readonly = user must pick from list
    imoncombo.set("Select search month")  # default text
    imoncombo.pack(side="left",padx=20)

    iyecombo = ttk.Combobox(frame, values=yearop, state="readonly")  # readonly = user must pick from list
    iyecombo.set("Select search year")  # default text
    iyecombo.pack(side="left",padx=20)

    conbtn = tk.Button(root, text="CONTINUE", command=transaction_income)
    conbtn.pack(pady=10)
    conbtn.bind("<Enter>",lambda e,b=conbtn: btncolcng_hover(e,b))
    conbtn.bind("<Leave>",lambda e,b=conbtn: btncolcng_leave(e,b))

    root.bind('<Return>', lambda event: conbtn.invoke())
    
    backbtn = tk.Button(root, bg="red", text="BACK", command=transac1)
    backbtn.pack(pady=10)

def piecrt(data,text):
    clearwidgets()
    forpie = {}
    for i in data:
        key = i[0]
        value = int(i[1])
        forpie[key] = forpie.get(key,0) + value
    forpienme = list(forpie.keys())
    forpiesze = list(forpie.values())

    fig = Figure(figsize=(4, 4), dpi=100)
    plot = fig.add_subplot(111)
    plot.pie(forpiesze, labels=forpienme, autopct="%1.1f%%")
    plot.set_title(text)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=(50,0))

    for cat, amt in zip(forpienme, forpiesze):
        lbl = tk.Label(root, text=f"{cat}: ₹{amt}",font=("Times New Roman", 20, "bold"))
        lbl.pack()

    backbtn = tk.Button(root, bg="red", text="BACK", command=Features)
    backbtn.pack(pady=5)

def transaction_income(tablesort='BY DATE',mo=None,ye=None):
    if (mo == None and ye == None):
        month = imoncombo.get()
        year = iyecombo.get()
    else:
        month = mo
        year = ye
    forsort = []
    fortable =[]
    print(os.path.join(base_dir,"DATA", f"{month}{year}income_{username}.csv"))
    clearwidgets()
    try:
        with open(os.path.join(base_dir,"DATA", f"{month}{year}income_{username}.csv"), "r") as tabledat:
            datarow = csv.reader(tabledat)
            for row in datarow:
                forsort.append(row)
            if tablesort == 'BY DATE':
                fortable = forsort
            elif tablesort == 'BY DATE DCS':
                fortable = forsort[::-1]
            elif tablesort == 'BY AMOUNT':
                fortable = sorted(forsort, key=lambda x: int(x[1]))
            else:
                fortable = fortable = sorted(forsort, key=lambda x: int(x[1]), reverse=True)
        columns = ("SOURCE", "AMOUNT", "DATE")
        tree = ttk.Treeview(root, columns= columns, show ="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=30)
        for i in fortable:
            tree.insert("", tk.END, values=i)
        tree.pack(expand=False, fill="both", pady=(250,10))
        frame1 = tk.Frame(root,bg='')
        frame1.pack(pady=10)

        frame11 = tk.Frame(frame1,bg='')
        frame11.pack(side="left",padx=10)
        
        sortbydate = tk.Button(frame11, text="SORT BY DATE", command=lambda: transaction_income('BY DATE',month,year))
        sortbydate.pack(side='left',padx=5)
        sortbydate2 = tk.Button(frame11, text="SORT BY DATE DCS", command=lambda: transaction_income('BY DATE DCS',month,year))
        sortbydate2.pack(side='left',padx=5)

        frame12 = tk.Frame(frame1,bg='')
        frame12.pack(side="left",padx=10)

        sortbyamount = tk.Button(frame12, text="SORT BY AMOUNT", command=lambda: transaction_income('BY AMOUNT',month,year))
        sortbyamount.pack(side='left',padx=5)
        sortbyamount2 = tk.Button(frame12, text="SORT BY AMOUNT DCS", command=lambda: transaction_income('BY AMOUNT DCS',month,year))
        sortbyamount2.pack(side='left',padx=5)
        
        frame2 = tk.Frame(root,bg='')
        frame2.pack(pady=10)
        backbtn = tk.Button(frame2, bg="red", text="BACK", command=transaci)
        backbtn.pack(side='left',padx=5)
        piebtn = tk.Button(frame2,text="PIE CHART",command=lambda: piecrt(forsort,"INCOME OVERVIEW"))
        piebtn.pack(side='left',padx=5)

    except FileNotFoundError:
        label_prompt = tk.Label(root, text="NO FILE FOUND!")
        label_prompt.pack(pady=5)
        backbtn2 = tk.Button(root, bg="red", text="BACK", command=transaci)
        backbtn2.pack(pady=10)

def transaco():
    clearwidgets()
    global omoncombo, oyecombo
    yearop = list(range(current_time.year, 1999, -1))
    monthop = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    label = tk.Label(root, text = "SELECT MONTH AND YEAR", font=("Times New Roman", 30, "bold"))
    label.pack(pady = (100,10))
    frame = tk.Frame(root,bg="")
    frame.pack(pady=10)

    omoncombo = ttk.Combobox(frame, values=monthop, state="readonly")  # readonly = user must pick from list
    omoncombo.set("Select search month")  # default text
    omoncombo.pack(side="left",padx=20)

    oyecombo = ttk.Combobox(frame, values=yearop, state="readonly")  # readonly = user must pick from list
    oyecombo.set("Select search year")  # default text
    oyecombo.pack(side="left",padx=20)

    conbtn = tk.Button(root, text="CONTINUE", command=transaction_outgo)
    conbtn.pack(pady=10)
    conbtn.bind("<Enter>",lambda e,b=conbtn: btncolcng_hover(e,b))
    conbtn.bind("<Leave>",lambda e,b=conbtn: btncolcng_leave(e,b))

    root.bind('<Return>', lambda event: conbtn.invoke())
    
    backbtn = tk.Button(root, bg="red", text="BACK", command=transac1)
    backbtn.pack(pady=10)

def setWall(s):
    global bg_label, image, bg_photo
    image = Image.open(os.path.join(base_dir, "WALLPAPERS", s))   # make sure this file is in the same folder OR use full path
    image = image.resize((1980, 1080))       # resize to match window
    bg_photo = ImageTk.PhotoImage(image)
    bg_label.configure(image=bg_photo)
    bg_label = bg_photo

    with open(os.path.join(base_dir, "WALLPAPERS", "wallfile.bin"), "wb") as currWall:
        pickle.dump(os.path.join(base_dir, "WALLPAPERS", s), currWall)
    Settings()

def transaction_outgo(tablesort='BY DATE',mo=None,ye=None):
    if (mo == None and ye == None):
        month = omoncombo.get()
        year = oyecombo.get()
    else:
        month = mo
        year = ye
    forsort = []
    fortable = []
    clearwidgets()
    try:
        with open(os.path.join(base_dir,"DATA", f"{month}{year}outgo_{username}.csv"), "r") as tabledat:
            datarow = csv.reader(tabledat)
            for row in datarow:
                forsort.append(row)
            if tablesort == 'BY DATE':
                fortable = forsort
            elif tablesort == 'BY DATE DCS':
                fortable = forsort[::-1]
            elif tablesort == 'BY AMOUNT':
                fortable = sorted(forsort, key=lambda x: int(x[1]))
            else:
                fortable = fortable = sorted(forsort, key=lambda x: int(x[1]), reverse=True)
        columns = ("SOURCE", "AMOUNT", "DATE")
        tree = ttk.Treeview(root, columns= columns, show ="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=30)
        for i in fortable:
            tree.insert("", tk.END, values=i)
        tree.pack(expand=False, fill="both", pady=(250,10))

        frame1 = tk.Frame(root,bg='')
        frame1.pack(pady=10)

        frame11 = tk.Frame(frame1,bg='')
        frame11.pack(side="left",padx=10)
        
        sortbydate = tk.Button(frame11, text="SORT BY DATE", command=lambda: transaction_outgo('BY DATE',month,year))
        sortbydate.pack(side='left',padx=5)
        sortbydate2 = tk.Button(frame11, text="SORT BY DATE DCS", command=lambda: transaction_outgo('BY DATE DCS',month,year))
        sortbydate2.pack(side='left',padx=5)

        frame12 = tk.Frame(frame1,bg='')
        frame12.pack(side="left",padx=10)

        sortbyamount = tk.Button(frame12, text="SORT BY AMOUNT", command=lambda: transaction_outgo('BY AMOUNT',month,year))
        sortbyamount.pack(side='left',padx=5)
        sortbyamount2 = tk.Button(frame12, text="SORT BY AMOUNT DCS", command=lambda: transaction_outgo('BY AMOUNT DCS',month,year))
        sortbyamount2.pack(side='left',padx=5)
        
        frame2 = tk.Frame(root,bg='')
        frame2.pack(pady=10)
        backbtn = tk.Button(frame2, bg="red", text="BACK", command=transaco)
        backbtn.pack(side='left',padx=5)
        piebtn = tk.Button(frame2,text="PIE CHART",command=lambda: piecrt(forsort,"SPENING OVERVIEW"))
        piebtn.pack(side='left',padx=5)

    except FileNotFoundError:
        label_prompt = tk.Label(root, text="NO FILE FOUND!")
        label_prompt.pack(pady=5)
        backbtn2 = tk.Button(root, bg="red", text="BACK", command=transaco)
        backbtn2.pack(pady=10)  

def Settings():
    clearwidgets()

    frame1 = tk.Frame(root,bg='')
    frame1.pack(pady=(50,10))
    
    btnimg1 = Image.open(os.path.join(base_dir, "WALLPAPERS", "1.jpg"))
    btnimg1 = btnimg1.resize((256,144))
    btn_photo1 = ImageTk.PhotoImage(btnimg1)
    wall1 = tk.Button(frame1, image=btn_photo1,command=lambda: setWall("1.jpg"))
    wall1.image = btn_photo1
    wall1.pack(side="left",padx=10)

    btnimg2 = Image.open(os.path.join(base_dir, "WALLPAPERS", "2.jpg"))
    btnimg2 = btnimg2.resize((256,144))
    btn_photo2 = ImageTk.PhotoImage(btnimg2)
    wall2 = tk.Button(frame1, image=btn_photo2,command=lambda: setWall("2.jpg"))
    wall2.image = btn_photo2
    wall2.pack(side='left',padx=10)

    frame2 = tk.Frame(root,bg='')
    frame2.pack(pady=(50,10))

    btnimg3 = Image.open(os.path.join(base_dir, "WALLPAPERS", "3.jpg"))
    btnimg3 = btnimg3.resize((256,144))
    btn_photo3 = ImageTk.PhotoImage(btnimg3)
    wall3 = tk.Button(frame2, image=btn_photo3,command=lambda: setWall("3.jpg"))
    wall3.image = btn_photo3
    wall3.pack(side="left",padx=10)

    btnimg4 = Image.open(os.path.join(base_dir, "WALLPAPERS", "4.jpg"))
    btnimg4 = btnimg4.resize((256,144))
    btn_photo4 = ImageTk.PhotoImage(btnimg4)
    wall4 = tk.Button(frame2, image=btn_photo4,command=lambda: setWall("4.jpg"))
    wall4.image = btn_photo4
    wall4.pack(side="left",padx=10)

    frame3 = tk.Frame(root,bg='')
    frame3.pack(pady=(50,10))

    btnimg5 = Image.open(os.path.join(base_dir, "WALLPAPERS", "5.jpg"))
    btnimg5 = btnimg5.resize((256,144))
    btn_photo5 = ImageTk.PhotoImage(btnimg5)
    wall5 = tk.Button(frame3, image=btn_photo5,command=lambda: setWall("5.jpg"))
    wall5.image = btn_photo5
    wall5.pack(side="left",padx=10)

    btnimg6 = Image.open(os.path.join(base_dir, "WALLPAPERS", "6.jpg"))
    btnimg6 = btnimg6.resize((256,144))
    btn_photo6 = ImageTk.PhotoImage(btnimg6)
    wall6 = tk.Button(frame3, image=btn_photo6,command=lambda: setWall("6.jpg"))
    wall6.image = btn_photo6
    wall6.pack(side="left",padx=10)

    backbtn = tk.Button(root, bg="red", text="BACK", command=Features)
    backbtn.pack(pady=10)

def budgetattr():
    try:
        salary = int(salentry.get())
        city = citcombo.get()
        age = int(agecombo.get())
        job = jobcombo.get()
        status = statcombo.get()

        cityindex = {'CHENNAI':3.03,'BANGALORE':3.18,'HYDERABAD':3.08,'MUMBAI':3.49,'KOLKATA':5.29,'DELHI':3.35,'KOCHI':2.71,'PUNE':3.00}
        statindex = {'OWNED PROPERTY':0.0,'VERY BASIC':0.5,'BASIC':1.0,'COMFIER':1.5,'LUXURY':2.0}
        currcit_idx = cityindex[city]
        currstat_idx = statindex[status]
        currtot_idx = (currcit_idx * currstat_idx) / 10

        foodneed_idx = {'LABOUR WORK':0.9, 'DELIVERY/DRIVING JOB':0.7, 'DESK JOB':0.6, 'STUDENT':0.6, 'UNEMPLOYED':0.5}
        currfood_idx = foodneed_idx[job]
        
        rent = salary * currtot_idx
        if (rent > (salary*0.5) ):
            rent = salary * 0.5
            if (rent > currcit_idx*13201.32):
                rent = currcit_idx * 13201.32
        citymul = 5500 * currcit_idx
        agemul = age/30
        jobmul = agemul * (currfood_idx)
        food = jobmul * citymul
        if (food > (salary*0.5)):
            food = salary * 0.5
            if(rent < salary*0.4):
                food = salary * 0.6
            if (food > (currcit_idx*10000)):
                food = currcit_idx * 10000
        balance = salary - (rent + food)
        entertianment = balance * 0.5
        if (entertianment > 200000):
            entertianment = 200000
        savings = salary - (rent + food + entertianment)

        finalbudget = [['RENT',rent],['FOOD',food],['ENTERTIANMENT',entertianment],['SAVINGS',savings]]
        piecrt(finalbudget,"BUDGET SUGGESTION")
    except:
        clearwidgets()
        label_prompt = tk.Label(root, text="DATA MISSING OR WRONG FORMAT",font=("Times New Roman", 30, "bold"))
        label_prompt.pack(pady=(250,10))

        ibutton = tk.Button(root, text="TRY AGAIN", command=budgetprep)
        ibutton.pack(pady=10)
        ibutton.bind("<Enter>",lambda e,b=ibutton: btncolcng_hover(e,b))
        ibutton.bind("<Leave>",lambda e,b=ibutton: btncolcng_leave(e,b))
    

def budgetprep():
    global salentry, citcombo, agecombo, jobcombo, statcombo

    clearwidgets()

    label_prompt = tk.Label(root, text="ENTER DETAILS",font=("Times New Roman", 30, "bold"))
    label_prompt.pack(pady=(250,10))

    frame1 = tk.Frame(root,bg='')
    frame1.pack(pady=10)
    salprom = tk.Label(frame1,text='SALARY')
    salprom.pack(side='left',padx=5)
    salentry = tk.Entry(frame1,width=25)
    salentry.pack(side='left',padx=5)

    frame2 = tk.Frame(root,bg='')
    frame2.pack(pady=10)
    cities = ['CHENNAI','BANGALORE','HYDERABAD','MUMBAI','KOLKATA','DELHI','KOCHI','PUNE']
    citprom = tk.Label(frame2,text='CITY')
    citprom.pack(side='left',padx=5)
    citcombo = ttk.Combobox(frame2, values=cities, state="readonly")
    citcombo.set("Select city")
    citcombo.pack(side="left",padx=20)

    frame3 = tk.Frame(root,bg='')
    frame3.pack(pady=10)
    ages = list(range(18,100))
    ageprom = tk.Label(frame3,text='AGE')
    ageprom.pack(side='left',padx=5)
    agecombo = ttk.Combobox(frame3, values=ages, state="readonly")
    agecombo.set("Select age")
    agecombo.pack(side="left",padx=20)

    frame4 = tk.Frame(root,bg='')
    frame4.pack(pady=10)
    jobs = ['LABOUR WORK', 'DELIVERY/DRIVING JOB', 'DESK JOB', 'STUDENT', 'UNEMPLOYED']
    jobprom = tk.Label(frame4,text='JOB TYPE')
    jobprom.pack(side='left',padx=5)
    jobcombo = ttk.Combobox(frame4, values=jobs, state="readonly")
    jobcombo.set("Select job type")
    jobcombo.pack(side="left",padx=20)

    frame5 = tk.Frame(root,bg='')
    frame5.pack(pady=10)
    stat = ['OWNED PROPERTY','VERY BASIC','BASIC','COMFIER','LUXURY']
    statprom = tk.Label(frame5,text='LIVING PREFERENCE')
    statprom.pack(side='left',padx=5)
    statcombo = ttk.Combobox(frame5, values=stat, state="readonly")
    statcombo.set("Select living pref")
    statcombo.pack(side="left",padx=20)

    conbtn = tk.Button(root, text="CONTINUE", command=budgetattr)
    conbtn.pack(pady=10)
    conbtn.bind("<Enter>",lambda e,b=conbtn: btncolcng_hover(e,b))
    conbtn.bind("<Leave>",lambda e,b=conbtn: btncolcng_leave(e,b))

    backbtn = tk.Button(root, bg="red", text="Back", command=Features)
    backbtn.pack(pady=10)

    root.bind('<Return>', lambda event: conbtn.invoke())
 
def Exit():
    root.destroy()
    
def Features():
    clearwidgets()
    label_prompt5 = tk.Label(root, text=f"WELCOME {username}",font=("Times New Roman", 30, "bold"))
    label_prompt5.pack(pady=(250,10))

    ibutton = tk.Button(root, text="INCOME", command=income)
    ibutton.pack(pady=10)
    ibutton.bind("<Enter>",lambda e,b=ibutton: btncolcng_hover(e,b))
    ibutton.bind("<Leave>",lambda e,b=ibutton: btncolcng_leave(e,b))
    
    obutton = tk.Button(root, text="OUTGO", command=outgo)
    obutton.pack(pady=10)
    obutton.bind("<Enter>",lambda e,b=obutton: btncolcng_hover(e,b))
    obutton.bind("<Leave>",lambda e,b=obutton: btncolcng_leave(e,b))
    
    tbutton = tk.Button(root, text="TRANSACTIONS", command=transac1)
    tbutton.pack(pady=10)
    tbutton.bind("<Enter>",lambda e,b=tbutton: btncolcng_hover(e,b))
    tbutton.bind("<Leave>",lambda e,b=tbutton: btncolcng_leave(e,b))

    bbutton = tk.Button(root, text="BUDGET", command=budgetprep)
    bbutton.pack(pady=10)
    bbutton.bind("<Enter>",lambda e,b=bbutton: btncolcng_hover(e,b))
    bbutton.bind("<Leave>",lambda e,b=bbutton: btncolcng_leave(e,b))
    
    sbutton = tk.Button(root, text="SETTINGS", command=Settings)
    sbutton.pack(pady=10)
    sbutton.bind("<Enter>",lambda e,b=sbutton: btncolcng_hover(e,b))
    sbutton.bind("<Leave>",lambda e,b=sbutton: btncolcng_leave(e,b))
    
    ebutton = tk.Button(root, bg="red", text="EXIT", command=Exit)
    ebutton.pack(pady=10)

def checklpass():
    global username
    username = logname.get()
    trial = pentry.get()
    with open(os.path.join(base_dir,"DATA",'ps.bin'), 'rb') as PASS:
            data = pickle.load(PASS)
            password = data[username]
    clearwidgets()
    if (password == trial):
        Features()
    else:
        label_prompt = tk.Label(root, text="Wrong Password")
        label_prompt.pack(pady=5)
        tabtn = tk.Button(root, text="TRY AGAIN!", command=login)
        tabtn.pack(pady=10)
    
def login():
    clearwidgets()
    global logname, pentry
    try:
        with open(os.path.join(base_dir,"DATA",'ps.bin'), 'rb') as PASS:
            label_prompt = tk.Label(root, text="Enter Username")
            label_prompt.pack(pady=(300,20))
            
            logname = tk.Entry(root, width=25)
            logname.pack(pady=0)
            
            pentry = tk.Entry(root, show="*", width=25)
            pentry.pack(pady=10)

            logname.focus_set()
            def nextfoc(event):
                pentry.focus_set()
            logname.bind('<Return>', nextfoc)

            frame = tk.Frame(root, bg='')
            frame.pack(pady=10)

            button = tk.Button(frame, text="LOGIN", command=checklpass)
            button.pack(side="left",padx=10)
            button.bind("<Enter>",lambda e,b=button: btncolcng_hover(e,b))
            button.bind("<Leave>",lambda e,b=button: btncolcng_leave(e,b))
            

            crbtn = tk.Button(frame, text="CREATE NEW USER", command= createuser)
            crbtn.pack(side="left",padx=10)
            crbtn.bind("<Enter>",lambda e,b=crbtn: btncolcng_hover(e,b))
            crbtn.bind("<Leave>",lambda e,b=crbtn: btncolcng_leave(e,b))

            ebutton = tk.Button(root, bg="red", text="EXIT", command=Exit)
            ebutton.pack(pady=100)

            pentry.bind('<Return>', lambda event: button.invoke())

    except FileNotFoundError:
        label_prompt = tk.Label(root, text="NO USER FOUND!")
        label_prompt.pack(pady=5)
        button = tk.Button(root, text="CREATE NEW USER", command=createuser)
        button.pack(pady=10)

        root.bind('<Return>', lambda event: button.invoke())

login()

root.mainloop()