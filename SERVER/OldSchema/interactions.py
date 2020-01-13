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
        if student[1] == str(args[0]):
            conn.close()
            return "1"
    conn.close()
    return "0"

# adds a student to the database
def add_student(args):
    conn = Database.create_connection("server.db")
    Database.insert_student(conn, args[0], args[1], args[2])
    conn.close()
    return "1"

# gets student information from the database
def information_student(args): # student number
    print(get_time()+"Returning information of textbook "+args[0]+"...")
    conn = Database.create_connection("server.db")
    students = Database.get_students(conn)
    for student in students:
        if student[1] == str(args[0]):
            student_strings = []
            for i in student:
                student_strings.append(str(i))
            conn.close()
            return "|".join(student_strings)

# get textbooks assigned to a student
def student_textbooks(args): # student number
    print(get_time()+"Returning textbooks currently held by student: "+args[0])
    conn = Database.create_connection("server.db")
    textbooks = []
    for t in Database.get_textbooks(conn):
        if t[5] == args[0]:
            textbooks.append(t[1])
    return "|".join(textbooks)

# checks if a textbook is valid in the database
def valid_textbook(args): # textbook number
    print(get_time()+"Checking if "+args[0]+" is a valid textbook id...")
    conn = Database.create_connection("server.db")
    textbooks = Database.get_textbooks(conn)
    for textbook in textbooks:
        if textbook[1] == str(args[0]):
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
        if textbook[1] == str(args[0]):
            textbook_strings = []
            for i in textbook:
                textbook_strings.append(str(i))
            # textbook_strings[-1] = str(Database.get_studentNumber(conn, textbook_strings[-1]))
            conn.close()
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

# assign a textbook to a student in the database
def assign_textbook(args): # textbook number, student number
    print(get_time()+"Assigning textbook: "+args[0]+" to student: "+args[1]+" in database...")
    conn = Database.create_connection("server.db")
    Database.assign_textbook(conn, args[0], args[1])
    conn.close()
    return "1"

# return a textbook from a student in the database
def return_textbook(args):
    print(get_time()+"Returning textbook: "+args[0]+" from student...")
    conn = Database.create_connection("server.db")
    Database.assign_textbook(conn, args[0], "None")
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
            "student_t": student_textbooks,
            "add_t": add_textbook,
            "add_s": add_student,
            "assign_t": assign_textbook,
            "return_t": return_textbook,
            "p": ping}