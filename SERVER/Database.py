import sqlite3
from sqlite3 import Error
import os, shutil

def reset_database(db_file, db_backup):
    os.remove(db_file)
    shutil.copy(db_backup, db_file)

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
    cur.execute(sql_cmd, (str(number), str(name), float(deposit)))
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

def get_studentNumber(conn, studentId):
    students = get_students(conn)
    for student in students:
        if student[0] == studentId:
            return str(student[1])

def insert_textbook(conn, number, title, cost, condition):
    # create an sql command string
    sql_cmd = """INSERT INTO Textbooks(TextbookNumber, TextbookTitle, TextbookCost, TextbookCondition)
                 VALUES (?,?,?,?)"""
    # create a cursor object
    cur = conn.cursor()
    # execute the sql command string using the function parameters
    cur.execute(sql_cmd, (number, title, cost, condition))
    # commit the changes to the database
    conn.commit()
    # return the id of the inserted textbook
    TextbookId = cur.lastrowid
    cur.close()
    return TextbookId

def remove_textbook(conn, TextbookNumber):
    # create an sql command string using the function parameter
    sql_cmd = "DELETE FROM Textbooks WHERE TextbookNumber="+str(TextbookNumber)+";"
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

def assign_textbook(conn, TextbookNumber, StudentNumber):
    # get textbook information
    for t in get_textbooks(conn):
        if t[1] == TextbookNumber:
            textbook = list(t)
    if textbook:
        textbook[5] = StudentNumber
        textbook.append(textbook[0])
        textbook = textbook[1:]
        # create a cursor object
        cur = conn.cursor()
        # create an sql command string to update textbooks table with new information
        sql = """UPDATE Textbooks
                SET TextbookNumber = ? ,
                    TextbookTitle = ? ,
                    TextbookCost = ? ,
                    TextbookCondition = ? ,
                    StudentNumber = ?
                WHERE TextbookId = ?"""
        # execute sql command string with selected textbook as input parameters and close cursor object
        print(textbook)
        cur.execute(sql, textbook)
        cur.close()
        # commit the changed database
        conn.commit()