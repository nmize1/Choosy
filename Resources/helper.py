from enum import Enum
import json

class Meal:
    def __init__(self, name, recipe, vegetarian):
        self.name = name
        self.recipe = recipe
        self.vegetarian = vegetarian

    def dump(self, outfile):
        json.dump(self.__dict__, outfile)

class Recipe:
    def __init__(self, ingredients):
        self.ingredients = ingredients

#helper function for number validation
def isFloat(n):
    try:
        float(n)
        return True
    except ValueError:
        return False

#helper for
class Measurements(Enum):
    PINCH = 0
    TSP = 1 #teaspoon
    TBSP = 2 #tablespoon
    OUNCE = 3
    DRYCUP = 4
    WETCUP = 5
    QUART = 6
    PINT = 7
    GALLON = 8
    POUND = 9
    STICK = 10
    NONE = 11

def toCup(amt, unit):
    match unit:
        case "PINCH":
            return ((amt / 3) / 48)

        case "TSP":
            return (amt / 48)

        case "TBSP":
            return (amt / 16)

        case "OUNCE":
            return (amt / 8)

        case "QUART":
            return (amt * 4)

        case "PINT":
            return (amt * 2)

        case "GALLON":
            return (amt * 16)

        case _:
            return amt

def fromCup(amt, unit):
    wet = True
    if unit in ["PINCH", "TSP", "TBSP", "DRYCUP"]:
        wet = False

    if not wet:
        if(amt <= 0.0026041658):
            return amt * 3 * 48, "PINCH"

        if(amt > 0.0026041658 and amt <= 0.0208333):
            return amt * 48, "TSP"

        if(amt > 0.0208333 and amt < 1):
            return amt * 16, "TBSP"

        if(amt >= 1):
            return amt, "DRYCUP"

    elif unit != "POUND" and unit != "NONE" and unit != "STICK":
        if(amt < 1):
            return amt * 8, "OUNCE"

        if(amt >= 1 and amt < 2):
            return amt, "WETCUP"

        if(amt >= 2 and amt < 4):
            return amt / 2, "PINT"

        if(amt >= 4 and amt < 16):
            return amt / 4, "QUART"

        if(amt >= 16):
            return amt / 16, "GALLON"

    else:
        return amt, unit
