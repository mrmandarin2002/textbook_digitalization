import time
#own files
import main, interactions
from datetime import datetime
from pynput.keyboard import Key, Listener

#####
#the scanner class is how the program detects input from the barcode
#also where data regarding the specifics of the scanned barcode is procssed
#####

class scanner:

    barcode_string = ""
    scanner_status = True
    start = datetime.now()
    previous_time = 0
    student_textbooks = []
    student_needed_textbooks = []
    student_courses = []
    student_textbooks_title = []
    textbook_info = []

    def __init__(self):

        self.server = interactions.Client(address = "127.0.0.1", port = 7356)
        keyLis = Listener(on_press=self.on_press)
        keyLis.start()
        

    def on_press(self, key):
        if(self.scanner_status):
            total_elapsed = (datetime.now() - self.start).microseconds + (datetime.now() - self.start).seconds * 1000000
            if(total_elapsed - self.previous_time < 40000):
                if(key != Key.enter and key != Key.shift):
                    self.barcode_string += str(key)[1:-1]
                if(key == Key.enter and len(self.barcode_string) > 4):
                    self.current_barcode = self.barcode_string
                    self.barcode_string = ""
                    main.root.check_barcode()
                    self.check_barcode()
                    exec("main." + main.root.current_frame_name + ".barcode_scanned(self = main.root.current_frame, controller=main.root)")
                    print("NO PROBLEM!")
            else:
                self.barcode_string = str(key)[1:-1]
                if(key == Key.shift or key == Key.enter):
                    self.barcode_string = ""
            self.previous_time = total_elapsed  

    def check_barcode(self):
        if(self.server.valid_s(self.current_barcode)):
            print("STUDENT BARCODE!")
            self.student_info = self.server.info_s(self.current_barcode)
            self.student_textbooks = self.server.student_t(self.current_barcode)
            self.student_needed_textbooks.clear()
            self.student_textbooks_title.clear()
            self.student_courses.clear()
            for textbook in self.student_textbooks:
                self.student_textbooks_title.append(self.server.info_t(textbook)[1])
            for x in range(4, len(self.student_info)):
                course_info = self.server.info_c(self.student_info[x])
                self.student_courses.append(course_info)
                course_textbooks = course_info[3].split('|')
                for textbook in course_textbooks:
                    if(len(textbook) > 0 and textbook not in self.student_needed_textbooks and textbook not in self.student_textbooks_title):
                        self.student_needed_textbooks.append(textbook)
            self.barcode_status = "Student"
            print(self.student_info)
        elif(self.server.valid_t(self.current_barcode)):
            print("TEXTBOOK BARCODE!")
            self.textbook_info = self.server.info_t(self.current_barcode)
            self.barcode_status = "Textbook"
        else:
            self.barcode_status = "Unknown"     