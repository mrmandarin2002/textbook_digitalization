import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try: 
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def close_connection(conn):
    conn.close()

def insert_student(conn, number, name, deposit):
    # create an sql command string
    sql_cmd = """INSERT INTO Students(StudentNumber, StudentName, StudentDeposit)
             VALUES(?,?,?)"""
    # create a cursor object
    cur = conn.cursor()
    # execute the sql command string using the function parameters
    cur.execute(sql_cmd, (number, name, deposit))
    cur.close() # close the cursor object
    # commit the changes to the database
    conn.commit()
    # return the id of the inserted sutdent
    return cur.lastrowid

def remove_student(conn, StudentId):
    # create an sql command string using the function parameter
    sql_cmd = "DELETE FROM Students WHERE StudentNumber="+str(StudentId)+";"
    # create a cursor object
    cur = conn.cursor()
    # execute the sql command string
    cur.execute(sql_cmd)
    cur.close() # close the cursor object
    # commit the changes to the database
    conn.commit()

def get_students(conn):
    # create a cursor object
    cur = conn.cursor()
    # execute an sql command string
    cur.execute("SELECT * FROM Students WHERE 1")
    # return the results of the query
    result = cur.fetchall()
    cur.close()
    return result

def insert_textbook(conn, title, cost, condition):
    # create an sql command string
    sql_cmd = """INSERT INTO Textbooks(Title, Cost, Condition)
                 VALUES (?,?,?)"""
    # create a cursor object
    cur = conn.cursor()
    # execute the sql command string using the function parameters
    cur.execute(sql_cmd, (title, cost, condition))
    # commit the changes to the database
    conn.commit()
    # return the id of the inserted student
    StudentId = cur.lastrowid
    cur.close()
    return StudentId

def remove_textbook(conn, TextbookId):
    # create an sql command string using the function parameter
    sql_cmd = "DELETE FROM Textbooks WHERE TextbookNumber="+str(TextbookId)+";"
    # create a cursor object
    cur = conn.cursor()
    # execute the sql command string
    cur.execute(sql_cmd)
    cur.close() # close the cursor object
    # commit the changes to the database
    conn.commit()

def get_textbooks(conn):
    # create a cursor object
    cur = conn.cursor()
    # execute an sql command string
    cur.execute("select * FROM Textbooks WHERE 1")
    # return the results of the query
    result = cur.fetchall()
    cur.close()
    return result

conn = create_connection("server.db")
print(get_students(conn))
conn.close()