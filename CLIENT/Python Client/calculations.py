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

def get_price(price):
    pass
    