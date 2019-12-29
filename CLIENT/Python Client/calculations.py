def get_textbook_condition(condition):
    if(condition == "New"):
        return 0
    elif(condition == "Good"):
        return 1
    elif(condition == "Fair"):
        return 2
    elif(condition == "Poor"):
        return 3
    elif(condition == "Destroyed"):
        return 4
    else:
        return 1e9

def get_textbook_condition_rev(condition):
    condition = int(condition)
    if(condition == 0):
        return "New"
    elif(condition == 1):
        return "Good"
    elif(condition == 2):
        return "Fair"
    elif(condition == 3):
        return "Poor"
    elif(condition == 4):
        return "Destroyed"
    else:
        return "DAFUQ"

def get_price(price):
    pass
    