import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
import random
import json

stngs = {"AllowVeg": False}

DAYS = {"SUNDAY" : False, "MONDAY" : False, "TUESDAY" : False, "WEDNESDAY" : False, "THURSDAY" : False, "FRIDAY" : False, "SATURDAY" : False}
meals = {}


def settings():
    def onCheck(days, i, boolVar):
        DAYS[days[i]] = boolVar.get()

    def vegCheck(boolVeg):
        stngs["AllowVeg"] = boolVeg.get()
        print(boolVeg.get())

    def OK():
        window.destroy()

    def Apply():
        with open("Resources/options.json", "w") as outfile:
            json.dump(DAYS, outfile)
            outfile.write('\n')
            json.dump(stngs, outfile)

    window = tk.Toplevel(root)
    ttk.Label(window, text="Vegetarian Days:").grid(column=1, row=0, columnspan=2)

    boolVeg = BooleanVar()
    if stngs["AllowVeg"]:
        boolVeg.set(True)
    ttk.Checkbutton(window, text="Allow vegetarian meals on non-vegetarian days", variable=boolVeg, command=lambda boolVeg=boolVeg : vegCheck(boolVeg)).grid(column=5, row=0, columnspan=3)

    days = list(DAYS)
    for i in range(3):
        ttk.Label(window, text="|").grid(column=0, row=i+1)
        ttk.Label(window, text="|").grid(column=8, row=i+1, sticky=W)

    for i in range(7):
        boolVar = BooleanVar()
        ttk.Label(window, text="-----").grid(column=i+1, row=1, sticky=W)
        ttk.Checkbutton(window, text=days[i], variable=boolVar, command=lambda days=days, i=i, boolVar=boolVar : onCheck(days, i, boolVar)).grid(column=i+1, row=2, sticky=W)
        if(DAYS[days[i]]):
            boolVar.set(True)
        ttk.Label(window, text="-----").grid(column=i+1, row=3, sticky=W)

    ttk.Button(window, text="OK", command=OK).grid(column=6, row=9)
    ttk.Button(window, text="Apply", command=Apply).grid(column=7, row=9, sticky=W)

def addMeal():
    def OK():
        error.destroy()

    n = name.get()
    if n == "":
        error = tk.Toplevel(root)
        ttk.Label(error, text="Meal name cannot be blank.").pack()
        ttk.Button(error, text="OK", command=OK).pack()
    else:
        name.set("")
        addIngredients(n)

def addIngredients(n):
    def OK(ings, amnts):
        meals[n] = []
        meals[n].append(vegVar.get())

        ingredients = []
        for i in range(len(ings)):
            ingredients.append(tuple((ings[i].get(), amnts[i].get())))

        meals[n].append(ingredients)
        print(meals)
        with open("Resources/meals.json", "w") as outfile:
            json.dump(meals, outfile)
        window.destroy()

    def Cancel():
        window.destroy()

    def addBox(i):
        en = ttk.Entry(entryFrame)
        en.grid(column=0, row=i.get(), padx=10, pady=1)
        ings.append(en)
        en = ttk.Entry(entryFrame)
        en.grid(column=1, row=i.get(), padx=10, pady=1)
        amts.append(en)
        i.set(i.get() + 1)

    def removeBox(i):
        if i.get() > 3:
            en = ings[-1]
            ings.remove(en)
            en.destroy()
            en = amts[-1]
            amts.remove(en)
            en.destroy()
            i.set(i.get() - 1)


    window = tk.Toplevel(root)
    label = "Shopping list for " + n + ":"
    ttk.Label(window, text=label).pack()

    entryFrame = ttk.Frame(window)
    entryFrame.pack()

    i = IntVar()
    vegVar = BooleanVar()

    i.set(3)
    ings = []
    amts = []
    ttk.Button(entryFrame, text="Add Ingredient", command=lambda i=i : addBox(i)).grid(column=0, row=0)
    ttk.Button(entryFrame, text="Remove Ingredient", command=lambda i=i: removeBox(i)).grid(column=1, row=0)
    ttk.Label(entryFrame, text="Ingredient:").grid(column=0, row=1)
    ttk.Label(entryFrame, text="Amount:").grid(column=1, row=1)
    en = ttk.Entry(entryFrame)
    en.grid(column=0, row=2, padx=10, pady=1)
    ings.append(en)
    en = ttk.Entry(entryFrame)
    en.grid(column=1, row=2, padx=10, pady=1)
    amts.append(en)

    ttk.Checkbutton(window, text="Vegetarian", variable=vegVar).pack()
    ttk.Button(window, text="Cancel", command=Cancel).pack(side=RIGHT)
    ttk.Button(window, text="OK", command=lambda ings=ings, amnts=amts : OK(ings, amnts)).pack(side=RIGHT)


def mealPlan():
    def OK():
        window.destroy()

    def gList():
        def gOK():
            grocer.destroy()

        lst = {}

        for meal in final:
            try:
                for i in range(len(meals[meal][1])):
                    helper = meals[meal][1][i]
                    ingredient = helper[0]
                    amt = int(helper[1])
                    if ingredient in lst:
                        lst[ingredient] = lst[ingredient] + amt
                    else:
                        lst[ingredient] = amt
            except KeyError:
                pass

        grocer = tk.Toplevel(window)
        ttk.Label(grocer, text="Grocery List:").grid(column=0, row=0, columnspan=2)

        i = 1
        for key, val in lst.items():
            ttk.Label(grocer, text=key).grid(column=0, row=i)
            ttk.Label(grocer, text=val).grid(column=1, row=i)
            i = i + 1

        ttk.Button(grocer, text="OK", command=gOK).grid(column=0, row=i, columnspan=2)

    if(len(list(meals)) < 7):
        print("Not enough meals")
        return

    window = tk.Toplevel(root)
    vgmls = []
    rgmls = []
    numVeg = 0

    for day, veg in DAYS.items():
        if veg:
            numVeg = numVeg + 1

    for m, v in meals.items():
        if v[0]:
            vgmls.append(m)
        else:
            rgmls.append(m)

    try:
        mls = random.sample(rgmls, 7)
    except ValueError:
        mls = rgmls

    try:
        if numVeg > 0:
            vmls = random.sample(vgmls, numVeg)
        else:
            vmls = vgmls
    except ValueError:
        vmls = vgmls

    for i in range(5):
        ttk.Label(window, text="|").grid(column=0, row=i+1)
        ttk.Label(window, text="|").grid(column=8, row=i+1)

    i = 0
    v = 0
    m = 0

    if stngs["AllowVeg"]:
        mls = mls + vmls

    final = []
    for day, veg in DAYS.items():
        if veg:
            try:
                d = vmls[v]
                v = v + 1
            except IndexError:
                d = "No Vegetarian Meals"
        else:
            d = mls[m]
            m = m + 1

        final.append(d)

        ttk.Label(window, text="-----").grid(column=i+1, row=1)
        ttk.Label(window, text=day).grid(column=i+1, row=2)
        ttk.Label(window, text="-----").grid(column=i+1, row=3)
        ttk.Label(window, text=d).grid(column=i+1, row=4)
        ttk.Label(window, text="-----").grid(column=i+1, row=5)

        i = i + 1

    ttk.Button(window, text="OK", command=OK).grid(column=7, row=6)
    ttk.Button(window, text="Grocery List", command=gList).grid(column=6, row=6)

try:
    with open('Resources/meals.json', 'r') as openfile:
        meals = json.load(openfile)
except IOError as error:
    pass
    print("Meals file doesn't exist. Will create when meals are saved.")

try:
    with open('Resources/options.json', 'r') as openfile:
        opts = [json.loads(line) for line in openfile]
        DAYS = opts[0]
        stngs = opts[1]
except IOError as error:
    pass
    print("Options file doesn't exist. Will create when options are applied.")

root = Tk()
root.iconbitmap("Resources/icon.ico")
root.title("Choosy")

logoframe = ttk.Frame(root).pack()
logo = tk.PhotoImage(file="Resources/logo.png")
logo = logo.subsample(2, 2)
ttk.Label(logoframe, image=logo).pack()

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.pack()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

name = tk.StringVar()
ttk.Entry(mainframe, textvariable=name).grid(column=1, row=2, sticky=N)
ttk.Button(mainframe, text="Add Meal", command=addMeal).grid(column=2, row=2, sticky=N)
ttk.Button(mainframe, text="Generate Meal Plan", command=mealPlan).grid(column=1, row=3, sticky=N)
ttk.Button(mainframe, text="Settings", command=settings).grid(column=2, row=3, sticky=N)

root.mainloop()
