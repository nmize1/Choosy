import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
import random
import json
import Resources.helper as helper

stngs = {"AllowVeg": False}

#DAYS = {DAY : VegetarianState}
DAYS = {"SUNDAY" : False, "MONDAY" : False, "TUESDAY" : False, "WEDNESDAY" : False, "THURSDAY" : False, "FRIDAY" : False, "SATURDAY" : False}
#meals = {Meal name : [VegetarianMealState, [[Ingredient 1, Amount of Ingredient 1], [Ingredient 2, Amount of Ingredient 2], ..., [Ingredient n, Amount of Ingredient n]]]}
meals = {}

# Settings maintains options about the days.
# It saves these settings in Resources/options.json
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

# addMeal makes sure there's a name in the text box before allowing ingredients to be added.
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

# addIngredients handles adding as many ingredients as needed for a meal and setting whether it's vegetarian.
# Then it adds the meal to meals. It saves meals in Resources/meals.json
def addIngredients(n):
    def isNum(S):
        return helper.isFloat(S)

    def OK(ings, amnts):
        meals[n] = []
        meals[n].append(vegVar.get())

        ingredients = []
        for i in range(len(ings)):
            a = float(amnts[i].get())
            m = meas[i].get()
            ingredients.append(tuple((ings[i].get(), a, m)))


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
        en = ttk.Entry(entryFrame, validate="key")
        en['validatecommand'] = (en.register(isNum),'%P')
        en.grid(column=1, row=i.get(), padx=10, pady=1)
        amts.append(en)
        ms = tk.StringVar()
        en = ttk.Combobox(entryFrame, textvariable=ms, width=10)
        en['values'] = [option.name for option in helper.Measurements]
        en.grid(column=2, row=i.get(), padx=2, pady=1)
        meas.append(en)
        i.set(i.get() + 1)

    def removeBox(i):
        if i.get() > 3:
            en = ings[-1]
            ings.remove(en)
            en.destroy()
            en = amts[-1]
            amts.remove(en)
            en.destroy()
            en = meas[-1]
            meas.remove(en)
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
    meas = []
    ttk.Button(entryFrame, text="Add Ingredient", command=lambda i=i : addBox(i)).grid(column=0, row=0)
    ttk.Button(entryFrame, text="Remove Ingredient", command=lambda i=i: removeBox(i)).grid(column=1, row=0)
    ttk.Label(entryFrame, text="Ingredient:").grid(column=0, row=1)
    ttk.Label(entryFrame, text="Amount:").grid(column=1, row=1)
    ttk.Label(entryFrame, text="Units:").grid(column=2, row=1)
    en = ttk.Entry(entryFrame)
    en.grid(column=0, row=2, padx=10, pady=1)
    ings.append(en)
    en = ttk.Entry(entryFrame, validate="key")
    en['validatecommand'] = (en.register(isNum), '%P')
    en.grid(column=1, row=2, padx=10, pady=1)
    amts.append(en)
    ms = tk.StringVar()
    en = ttk.Combobox(entryFrame, textvariable=ms, width=10)
    en['values'] = [option.name for option in helper.Measurements]
    en.grid(column=2, row=2, padx=2, pady=1)
    meas.append(en)

    ttk.Button(window, text="Cancel", command=Cancel).pack(side=RIGHT)
    ttk.Button(window, text="OK", command=lambda ings=ings, amnts=amts : OK(ings, amnts)).pack(side=RIGHT)
    ttk.Checkbutton(window, text="Vegetarian", variable=vegVar).pack(side = RIGHT)

# mealPlan creates a random meal plan from the saved meals.
def mealPlan():
    def OK():
        window.destroy()

    # gList takes the meal plan created by mealPlan and uses meals' ingredient
    # lists to create a grocery list for the entire meal plan
    def gList():
        def gOK():
            grocer.destroy()

        lst = {}

        for meal in final:
            try:
                for i in range(len(meals[meal][1])):
                    help = meals[meal][1][i]
                    ingredient = help[0]
                    amt = help[1]
                    meas = help[2]
                    amt = float(helper.toCup(amt, meas))
                    if meas != "POUND" and meas != "NONE":
                        amt, meas = helper.fromCup(amt, meas)


                    tmp = {meas : amt}
                    if ingredient in lst:
                        if meas in lst[ingredient]:
                            lst[ingredient][meas] = lst[ingredient][m] + amt
                        else:
                            lst[ingredient][meas] = amt
                    else:
                        lst[ingredient] = tmp
            except KeyError:
                pass

        grocer = tk.Toplevel(window)
        ttk.Label(grocer, text="Grocery List:").grid(column=0, row=0, columnspan=2)

        i = 1
        for ing, dic in lst.items():
            ttk.Label(grocer, text=ing).grid(column=0, row=i)
            j = 2
            for meas, amt in dic.items():
                ttk.Label(grocer, text=amt).grid(column=j, row=i)
                j = j + 1
                ttk.Label(grocer, text=meas).grid(column=j, row=i)
                j = j + 1
            i = i + 1

        print(meals)
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

# Check whether meals.json exists and options.json exists
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

# Create the main UI
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
