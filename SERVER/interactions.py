# function to get the current time
def get_time():
    return str(datetime.now()).split()[1].split(".")[0]+" "

# check if a textbook id is valid in the database
def valid_textbook(args):
    print(get_time()+"Checking if "+args[0]+" is a valid textbook id...")
    return "1"

# check if a student id is valid in the database
def valid_student(args):
    print(get_time()+"checking if "+args[0]+" is a valid student id...")
    return "1"

# get the condition of a textbook
def condition_textbook(args):
    print(get_time()+"Getting the condition of textbook with id "+args[0])
    return "1"

# function dictionary
interact = {"valid_t": valid_textbook,
            "valid_s": valid_student,
            "condition_t": condition_textbook}
