import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
import random
import json
import Resources.helper as helper

stngs = {"AllowVeg": False}
days = {"SUNDAY" : False, "MONDAY" : False, "TUESDAY" : False, "WEDNESDAY" : False, "THURSDAY" : False, "FRIDAY" : False, "SATURDAY" : False}
rdays = {"SUNDAY" : False, "MONDAY" : False, "TUESDAY" : False, "WEDNESDAY" : False, "THURSDAY" : False, "FRIDAY" : False, "SATURDAY" : False}
meals = []
restaurants = []

# Settings maintains options about the days.
# It saves these settings in Resources/options.json
def settings():
    def onCheck(dys, i, boolVar):
        days[dys[i]] = boolVar.get()

    def ronCheck(dys, i, rboolVar):
        rdays[dys[i]] = rboolVar.get()

    def vegCheck(boolVeg):
        stngs["AllowVeg"] = boolVeg.get()
        print(boolVeg.get())

    def OK():
        window.destroy()

    def Apply():
        with open("Resources/options.json", "w") as outfile:
            json.dump(days, outfile)
            outfile.write('\n')
            json.dump(rdays, outfile)
            outfile.write('\n')
            json.dump(stngs, outfile)

    window = tk.Toplevel(root)
    ttk.Label(window, text="Vegetarian days:").grid(column=1, row=0, columnspan=2)

    boolVeg = BooleanVar()
    if stngs["AllowVeg"]:
        boolVeg.set(True)
    ttk.Checkbutton(window, text="Allow vegetarian meals on non-vegetarian days", variable=boolVeg, command=lambda boolVeg=boolVeg : vegCheck(boolVeg)).grid(column=5, row=0, columnspan=3)

    dys = list(days)
    for i in range(3):
        ttk.Label(window, text="|").grid(column=0, row=i+1)
        ttk.Label(window, text="|").grid(column=8, row=i+1, sticky=W)

    for i in range(7):
        boolVar = BooleanVar()
        ttk.Label(window, text="-----").grid(column=i+1, row=1, sticky=W)
        ttk.Checkbutton(window, text=dys[i], variable=boolVar, command=lambda days=days, i=i, boolVar=boolVar : onCheck(dys, i, boolVar)).grid(column=i+1, row=2, sticky=W)
        if(days[dys[i]]):
            boolVar.set(True)
        ttk.Label(window, text="-----").grid(column=i+1, row=3, sticky=W)

    ttk.Label(window, text="Restaurant days:").grid(column=1, row=9, columnspan=2)
    for i in range(3):
        ttk.Label(window, text="|").grid(column=0, row=9+i+1)
        ttk.Label(window, text="|").grid(column=8, row=9+i+1, sticky=W)

    for i in range(7):
        rboolVar = BooleanVar()
        ttk.Label(window, text="-----").grid(column=i+1, row=10, sticky=W)
        ttk.Checkbutton(window, text=dys[i], variable=rboolVar, command=lambda days=days, i=i, rboolVar=rboolVar : ronCheck(dys, i, rboolVar)).grid(column=i+1, row=11, sticky=W)
        if(rdays[dys[i]]):
            rboolVar.set(True)
        ttk.Label(window, text="-----").grid(column=i+1, row=12, sticky=W)

    ttk.Button(window, text="OK", command=OK).grid(column=6, row=13)
    ttk.Button(window, text="Apply", command=Apply).grid(column=7, row=13, sticky=W)

# addRest adds restaurants to restaurants list for restaurant days
def addRest():
    def OK():
        error.destroy()

    n = name.get()
    if n == "":
        error = tk.Toplevel(root)
        ttk.Label(error, text="Restaurant name cannot be blank.").pack()
        ttk.Button(error, text="OK", command=OK).pack()
    else:
        name.set("")
        restaurants.append(n)
        with open("Resources/restaurants.json", "w") as outfile:
            json.dump(restaurants, outfile)
            outfile.write('\n')

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
        ingredients = []
        for i in range(len(ings)):
            a = float(amnts[i].get())
            m = meas[i].get()
            ingredients.append(tuple((ings[i].get(), a, m)))

        m = helper.Meal(n, ingredients, vegVar.get())
        meals.append(m)
        with open("Resources/meals.json", "w") as outfile:
            for m in meals:
                m.dump(outfile)
                outfile.write('\n')
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
                ings = meal.recipe
                for i in ings:
                    print(i)
                    ingredient = i[0]
                    amt = i[1]
                    meas = i[2]
                    amt = float(helper.toCup(amt, meas))
                    if meas != "POUND" and meas != "NONE":
                        amt, meas = helper.fromCup(amt, meas)


                    tmp = {meas : amt}
                    if ingredient in lst:
                        print(ingredient)
                        if meas in lst[ingredient]:
                            d = lst[ingredient]
                            d[meas] = d[meas] + amt
                        else:
                            lst[ingredient][meas] = amt
                    else:
                        lst[ingredient] = tmp

                    print(lst[ingredient][meas])
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

        ttk.Button(grocer, text="OK", command=gOK).grid(column=0, row=i, columnspan=2)

    if(len(list(meals)) < 7):
        print("Not enough meals")
        return

    window = tk.Toplevel(root)
    vgmls = []
    rgmls = []
    numVeg = 0

    for day, veg in days.items():
        if veg:
            numVeg = numVeg + 1

    for m in meals:
        if m.vegetarian:
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
    for day, veg in days.items():
        if veg:
            try:
                d = vmls[v]
                v = v + 1
            except IndexError:
                d = helper.Meal("No Vegetarian Meals", [], True)
        else:
            d = mls[m]
            m = m + 1

        print(rdays[day])
        if rdays[day]:
            r = random.choice(restaurants)
            d = helper.Meal(r, [], False)

        final.append(d)

        ttk.Label(window, text="-----").grid(column=i+1, row=1)
        ttk.Label(window, text=day).grid(column=i+1, row=2)
        ttk.Label(window, text="-----").grid(column=i+1, row=3)
        ttk.Label(window, text=d.name).grid(column=i+1, row=4)
        ttk.Label(window, text="-----").grid(column=i+1, row=5)

        i = i + 1

    ttk.Button(window, text="OK", command=OK).grid(column=7, row=6)
    ttk.Button(window, text="Grocery List", command=gList).grid(column=6, row=6)

# editMeal handles replacing meal's recipes by removing the meal and replacing it with a new one
def editMeal():
    def isNum(S):
        return helper.isFloat(S)

    def OK(ings, amnts):
        ingredients = []
        for i in range(len(ings)):
            a = float(amnts[i].get())
            m = meas[i].get()
            ingredients.append(tuple((ings[i].get(), a, m)))

        m = helper.Meal(selectedMeal.get(), ingredients, vegVar.get())
        for mls in meals:
            if mls.name == m.name:
                meals.remove(mls)

        print(m.recipe)
        meals.append(m)
        refreshMeals()
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
    label = "Shopping list for:"
    ttk.Label(window, text=label).pack()
    selectedMeal = ttk.Combobox(window, width=10)
    selectedMeal['values'] = [m.name for m in meals]
    selectedMeal.pack()

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

# rewrite meals.json after a change to a meal
def refreshMeals():
    os.remove("Resources/meals.json")
    with open("Resources/meals.json", "w") as outfile:
        for m in meals:
            m.dump(outfile)
            outfile.write('\n')

# Check whether meals.json exists and options.json exists
try:
    with open('Resources/meals.json', 'r') as openfile:
        file = [json.loads(line) for line in openfile]
        for f in file:
            m = helper.Meal(f["name"], f["recipe"], f["vegetarian"])
            meals.append(m)

except IOError as error:
    pass
    print("Meals file doesn't exist. Will create when meals are saved.")

try:
    with open('Resources/restaurants.json', 'r') as openfile:
        file = [json.loads(line) for line in openfile]
        for f in file:
            restaurants.append(f)

except IOError as error:
    pass
    print("Meals file doesn't exist. Will create when meals are saved.")

try:
    with open('Resources/options.json', 'r') as openfile:
        opts = [json.loads(line) for line in openfile]
        days = opts[0]
        rdays = opts[1]
        stngs = opts[2]
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
ttk.Button(mainframe, text="Add Restaurant", command=addRest).grid(column=3, row=2, sticky=N)
ttk.Button(mainframe, text="Edit Meals", command=editMeal).grid(column=2, row=3, sticky=N)
ttk.Button(mainframe, text="Generate Meal Plan", command=mealPlan).grid(column=1, row=3, sticky=N)
ttk.Button(mainframe, text="Settings", command=settings).grid(column=3, row=3, sticky=N)

root.mainloop()
