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

# get textbooks that a student should have
def student_requisites(args): # student number
    print(get_time()+"Returning requisite textbooks for student: "+args[0])
    conn = Database.create_connection("server.db")
    for s in Database.get_students(conn):
        if s[1] == args[0]:
            courses = s[4].split("|")
    textbooks = []
    for c in Database.get_courses(conn):
        if c[1] in courses:
            textboks.append(c[4].split("|"))
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

# return the requisite textbooks for a given course
def course_requisites(args):
    print(get_time()+"Getting course requisites for course: "+args[0])
    conn = Database.create_connection("server.db")
    for c in Database.get_courses(conn):
        if c[1] == args[0]:
            return c[4]

# return information for a specified course
def information_course(args):
    print(get_time()+"Returning information for course: "+args[0])
    conn = Database.create_connection("server.db")
    for c in Database.get_courses(conn):
        if c[1] == args[0]:
            course = list(c[1:])
    for i in range(len(course)):
        course[i] = str(course[i])
    conn.close()
    return "~".join(course)

# return all course numbers from database
def course_numbers(args):
    print(get_time()+"Returning all course numbers...")
    conn = Database.create_connection("server.db")
    numbers = []
    for c in Database.get_courses(conn):
        numbers.append(c[1])
    conn.close()
    return "|".join(numbers)

def set_course_textbooks(args):
    print(get_time()+"Setting textbooks:\n\t"+"\n\t".join(args[1])+"\nAs requisites to course: "+args[0])
    conn = Database.create_connection("server.db")
    Database.set_course_requisites(conn, args[0], args[1])
    conn.close()
    return "1"

def get_teachers(args):
    print(get_time()+"Getting teacher names and numbers...")
    conn = Database.create_connection("server.db")
    teachers = []
    for course in Database.get_courses(conn):
        if course[3] not in teachers:
            teachers.append(course[3])
    conn.close()
    return "|".join(teachers)

def get_teacher_courses(args):
    print(get_time()+"Getting courses of teacher: "+args[0]+"...")
    conn = Database.create_connection("server.db")
    courses = []
    for course in Database.get_courses(conn):
        print(course)
        if course[3] == args[0] and course[1] not in courses:
            courses.append(course[1])
    conn.close()
    return "|".join(courses)

# ping (always return 1)
def ping(args): # no arguments
    print(get_time()+"Received ping...")
    return "1"

# function dictionary
interact = {"valid_t": valid_textbook,
            "valid_s": valid_student,
            "info_t": information_textbook,
            "info_s": information_student,
            "info_c": information_course,
            "delete_t": delete_textbook,
            "student_t": student_textbooks,
            "student_r": student_requisites,
            "get_teachers": get_teachers,
            "get_teacher_c": get_teacher_courses
            "set_course_r": set_course_textbooks,
            "add_t": add_textbook,
            "add_s": add_student,
            "courses_n": course_numbers,
            "course_r": course_requisites,
            "assign_t": assign_textbook,
            "return_t": return_textbook,
            "p": ping}