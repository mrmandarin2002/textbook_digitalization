import time
#own files
import main, interactions
#allow to keep track of time
from datetime import datetime
#pynput's library for enabling threading
from pynput.keyboard import Key, Listener

#####
#the scanner class is how the program detects input from the barcode
#also where data regarding the specifics of the scanned barcode is procssed
#basic idea for barcode detection is that since the barcode scanner sends input as keyboard...
#we can basically have a temporary string that keeps track of keyboard inputs. This string clears...
#every time more than 40 milliseconds elapses between inputs
#####

class scanner:

    #a temporary string to keep track of characters being added
    barcode_string = ""
    #identification of the type of the barcode
    barcode_status = ""
    #keeps track of the current time
    start = datetime.now()
    #keeps track of the time of the last input
    previous_time = 0
    #the textbooks currently taken out by a student
    student_textbooks = []
    #student's info {
    #1 : barcode 
    #2 : name
    #3 : ?
    #4 : textbooks
    #5 - ? : courses
    # }
    student_info = []
    #list of textbooks assigned by teachers
    student_needed_textbooks = []
    #courses that a student takes
    student_courses = []
    #the titles of the student's textbooks (student_textbooks is based on barcode id)
    student_textbooks_title = []
    #a textbook's info{
    # ----
    # ----
    # }
    textbook_info = []

    def __init__(self):

        #where the interaction with server happens
        self.server = interactions.Client(address = "127.0.0.1", port = 7356)

        #starts the thread where program listens for input (if there is input call on_press function below)
        keyLis = Listener(on_press=self.on_press)
        keyLis.start()
        
    #function that is called whenever there is input from a device
    #note that time is in microseconds
    def on_press(self, key):
        #the amount of time between current input and previous input (converted into micro seconds)
        time_elapsed = (datetime.now() - self.start).microseconds + (datetime.now() - self.start).seconds * 1000000
        #this assumes that the input is from barcode scanner as the time between inputs is less than 40 milliseconds
        if(time_elapsed - self.previous_time < 40000):
            #add input to the temporary string (self.barcode_string)
            #we don't want the enter or shift key to be added as to our final string
            if(key != Key.enter and key != Key.shift):
                self.barcode_string += str(key)[1:-1]
            #since the final input of scanner is always enter, if the string we have been adding to is a certain length...
            #the program decides its a barcode. It's quite foolproof
            if(key == Key.enter and len(self.barcode_string) > 4):
                #this makes "self.current_barcode" our official barcode id! For now...
                self.current_barcode = self.barcode_string
                #reset the the temporary barcode string
                self.barcode_string = ""
                #checks what the actual hell the barcode is
                self.check_barcode()
                #executes a function in each frame respectively that will process the barcode
                exec("main." + main.root.current_frame_name + ".barcode_scanned(self = main.root.current_frame, controller=main.root.scanner)")
        else:
            #in case this is the start of a scanner's input, we add the first ccharacter
            self.barcode_string = str(key)[1:-1]
            #once again it would be bad if shifts or enters somehow entered our temporary string...
            if(key == Key.shift or key == Key.enter):
                self.barcode_string = ""
        #sets the time of this input
        self.previous_time = time_elapsed  

    #this function checks what the hell the barcode is
    def check_barcode(self):
        #checks if the barcode is a student's
        if(self.server.valid_s(self.current_barcode)):
            #gets the student's info from the server
            self.student_info = self.server.info_s(self.current_barcode)
            #for debugging I guess
            print("STUDENT BARCODE!")
            print("Student Info: " + self.student_info)
            #gets the textbooks the student has taken out
            self.student_textbooks = self.server.student_t(self.current_barcode)
            #clears a bunch of lists so that the relevant stuff can be added
            self.student_needed_textbooks.clear()
            self.student_textbooks_title.clear()
            self.student_courses.clear()
            #this creates a list of student's textbooks based on title instead of barcode ID
            #useful for comparisons....
            for textbook in self.student_textbooks:
                self.student_textbooks_title.append(self.server.info_t(textbook)[1])
            #this creates a list of a student's courses with the help of student_info
            for x in range(4, len(self.student_info)):
                #gets info of a student's courses
                course_info = self.server.info_c(self.student_info[x])
                #adds course to a student's course
                self.student_courses.append(course_info)
                #the textbooks needed in this course
                course_textbooks = course_info[3].split('|')
                #this loop is to find out which textbooks the student needs to take out that were assigned to him
                for textbook in course_textbooks:
                    #checks for duplicates and idek 
                    if(len(textbook) > 0 and textbook not in self.student_needed_textbooks and textbook not in self.student_textbooks_title):
                        self.student_needed_textbooks.append(textbook)
            #allows other parts of the program know what type of barcode is scanned in
            self.barcode_status = "Student"
        #if the barcode is a textbook's
        elif(self.server.valid_t(self.current_barcode)):
            print("TEXTBOOK BARCODE!")
            self.textbook_info = self.server.info_t(self.current_barcode)
            self.barcode_status = "Textbook"
        #for unknown barcodes
        else:
            print("UNKNOWN BARCODE!")
            self.barcode_status = "Unknown"     