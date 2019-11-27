# import neccessary classes and functions
from datetime import datetime
import Database

# function to get the current time
def get_time():
    return str(datetime.now()).split()[1].split(".")[0]+" "

# checks if a student is valid in the database
def valid_student(args): # student number
    print(get_time()+"Checking if "+args[0]+" is a valid student id...")
    conn = Database.create_connection("server.db")
    students = Database.get_students(conn)
    for student in students:
        if student[1] == int(args[0]):
            conn.close()
            return "1"
    conn.close()
    return "0"

# gets student information from the database
def information_student(args): # student number
    print(get_time()+"Returning information of textbook "+args[0]+"...")
    conn = Database.create_connection("server.db")
    students = Database.get_students(conn)
    for student in students:
        if student[1] == int(args[0]):
            student_strings = []
            for i in student:
                student_strings.append(str(i))
            conn.close()
            return "|".join(student_strings)

# checks if a textbook is valid in the database
def valid_textbook(args): # textbook number
    print(get_time()+"Checking if "+args[0]+" is a valid textbook id...")
    conn = Database.create_connection("server.db")
    textbooks = Database.get_textbooks(conn)
    for textbook in textbooks:
        if textbook[1] == int(args[0]):
            conn.close()
            return "1"
    conn.close()
    return "0"

# gets textbook information from the database
def information_textbook(args): # textbook number
    print(get_time()+"Returning information of textbook "+args[0]+"...")
    conn = Database.create_connection("server.db")
    textbooks = Database.get_textbooks(conn)
    for textbook in textbooks:
        if textbook[1] == int(args[0]):
            textbook_strings = []
            for i in textbook:
                textbook_strings.append(str(i))
            conn.close()
            textbook_strings[-1] = Database.get_studentNumber(conn, textbook_strings[-1])
            return "|".join(textbook_strings[1:])

# delete textbook from database
def delete_textbook(args): # textbook number
    print(get_time()+"Deleting "+args[0]+" from textbook table...")
    conn = Database.create_connection("server.db")
    Database.remove_textbook(conn, args[0])
    conn.close()
    return "1"

# add a textbook to the database
def add_textbook(args): # textbook number, title, cost, condition
    print(get_time()+"Adding textbook to database\n\tNumber: "+args[0]+"\n\tTitle: "+args[1]+"\n\tCost: "+args[2]+"\n\tCondition: "+args[3])
    conn = Database.create_connection("server.db")
    Database.insert_textbook(conn, args[0], args[1], args[2], args[3])
    conn.close()
    return "1"

# ping (always return 1)
def ping(args): # no arguments
    print(get_time()+"Received ping...")
    return "1"

# function dictionary
interact = {"valid_t": valid_textbook,
            "valid_s": valid_student,
            "info_t": information_textbook,
            "info_s": information_student,
            "delete_t": delete_textbook,
            "add_t": add_textbook,
            "p": ping}
