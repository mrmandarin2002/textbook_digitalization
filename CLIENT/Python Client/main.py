#Digitext Program written in python as JavaFX is the definition of cancer
import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import ttk
from tkinter import messagebox

#import own files
import interactions, calculations, window, barcode_interaction

MAIN_FONT = "Comic Sans MS"
MAROON = '#B03060'
PINK = '#FF00D4'
NEON_GREEN = '#4DFF4D'

class client(tk.Tk):

    barcode_string = ""
    current_barcode = ""
    barcode_scanned = False
    version = "teacher"
    student_info = []
    student_textbooks = []
    student_needed_textbooks = []
    student_courses = []
    student_textbooks_title = []
    textbook_info = []
    barcode_status = ""
    textbook_list = []


    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        
        #self.server = interactions.Client(address = "127.0.0.1", port = 7356)
        self.scene_list = (WelcomePage, Menu, TextbookManagement, Info, TextbookScanner, TeacherAssignment)

        #different type of fonts used throughout the program
        self.TITLE_FONT = tkfont.Font(family=MAIN_FONT, size=20, weight="bold")
        self.SUBTITLE_FONT = tkfont.Font(family = MAIN_FONT, size = 14, weight = "bold")
        self.FIELD_FONT = tkfont.Font(family = MAIN_FONT, size = 11)
        self.BUTTON_FONT = tkfont.Font(family=MAIN_FONT, size=10)
        self.BACK_BUTTON_FONT = tkfont.Font(family = MAIN_FONT, size = 8)
        self.MENU_FONT = tkfont.Font(family=MAIN_FONT, size=11)

        self.scanner = barcode_interaction.scanner()


        #listens for keypresses (calls "on_press" function)
        #keyLis = Listener(on_press=self.on_press)
        #keyLis.start()

        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.textbook_list = self.scanner.server.get_textbook_titles()

        self.frames = {}

        for scene in self.scene_list:
            page_name = scene.__name__
            frame = scene(parent=container, controller = self)
            self.frames[page_name] = frame
            frame.grid(row = 0, column = 0, sticky = "nswe")

        self.show_frame("Menu")
    """
    def check_barcode(self):
        if(self.server.ping()):
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
    """

    def show_frame(self, page_name):
        exec(page_name + ".can_enter(self = self.frames[page_name], controller = self)")
        if(self.check_requisites):
            self.current_frame = self.frames[page_name]
            self.current_frame_name = page_name
            exec(self.current_frame_name + ".clear(self = self.current_frame)")
            self.current_frame.tkraise()

    #allows the creation of buttons
    def make_button(self, controller, d_text, scene, option):
        if(option == "menu"):
            return tk.Button(controller, text = d_text, command = lambda: self.show_frame(scene), font = self.MENU_FONT, fg = PINK)
        else:
            return tk.Button(controller, text = d_text, command = lambda: self.show_frame(scene), font = self.BUTTON_FONT)
    
    def make_back_button(self, controller):
        return tk.Button(controller, text = "Back to Menu", command = lambda: self.show_frame("Menu"), font = self.BACK_BUTTON_FONT)

class WelcomePage(tk.Frame):

    def clear(self, controller):
        pass

    def barcode_scanned(self, controller):
        pass

    def can_enter(self, controller):
        controller.check_requisites = True
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        WelcomePage.configure(self, background = MAROON)
        welcome_title = tk.Label(self, text = "Welcome to DigiText!!", font = controller.TITLE_FONT , bg = MAROON)
        welcome_title.pack(side = "top", pady = 150, padx = 50)
        welcome_button = controller.make_button(controller = self, d_text = "Press to continue...", scene = "Menu", option = '')
        welcome_button.pack()
        
class Menu(tk.Frame):

    def can_enter(self, controller):
        controller.check_requisites = True

    def clear(self):
        pass
    
    def barcode_scanned(self, controller):
        pass

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controlller = controller

        Menu.configure(self, background = MAROON)
        menu_title = tk.Label(self, text = "DigiText Menu", font = controller.TITLE_FONT , bg = MAROON)
        m_button = controller.make_button(controller = self, d_text = "Textbook Management", scene = "TextbookManagement", option = "menu")
        s_button = controller.make_button(controller = self, d_text = "Textbook Scanner", scene = "TextbookScanner", option = "menu")
        i_button = controller.make_button(controller = self, d_text = "Info Scanner", scene = "Info", option = "menu")
        t_button = controller.make_button(controller = self, d_text = "Teacher Assignent", scene = "TeacherAssignment", option = "menu")
        menu_title.pack(pady = (100, 0))
        m_button.pack(pady = (50, 0))
        s_button.pack()
        i_button.pack()
        t_button.pack()

class TextbookManagement(tk.Frame):

    student_scanned = False
    day = 'D'
    textbook_list_made = False

    def can_enter(self, controller):
        controller.check_requisites = True

    def clear(self):
        self.barcode_label.config(text = "Current Barcode: ")
        self.barcode_status_label.config(text = "Barcode Type: ")
        self.textbook_title_label.config(text = "Textbook Title: ")
        self.textbook_condition_label.config(text = "Textbook Condition: ")
        self.textbook_price_label.config(text = "Textbook Price: ")
        self.student_tnum_label.config(text = "Textbooks taken out: ")
        self.student_name_label["text"] = "Student Name:"
        self.textbook_list.delete(0, tk.END)
 
    def barcode_scanned(self, controller):
        if(controller.server.ping()):
            if(controller.barcode_status == "Student"):
                self.student_scanned = True
                self.clear()
                self.student_name_label["text"] = "Student Name: " + controller.student_info[2]
                self.barcode_status_label.config(text = "Barcode Type: Student")
                self.num_of_textbooks = len(controller.student_textbooks)
                print(controller.student_textbooks)
                self.student_tnum_label["text"] = "Textbooks taken out: " + str(len(controller.student_textbooks))
                self.textbook_list.delete(0, tk.END)
                self.current_student_barcode = controller.current_barcode
                if(self.day == 'D'):
                    print(controller.student_info)
                    cnt = 0
                    for textbook in controller.student_needed_textbooks:
                        self.textbook_list.insert(cnt, textbook)
                        cnt += 1
                else:
                    if(self.num_of_textbooks):
                        self.textbook_list_made = True
                        cnt = 0
                        for textbook in controller.student_textbooks:
                            self.textbook_list.insert(cnt, controller.server.info_t(textbook)[1])
                            cnt += 1
                    else:
                        messagebox.showerror("ERROR", controller.student_info[2] + " has taken out no textbooks")

            elif(controller.server.valid_t(controller.current_barcode)):
                self.barcode_status_label["text"] = "Barcode Type: Textbook"
                if(self.student_scanned):
                    if(self.day == 'D'):
                        print(controller.textbook_info)
                        attempt_assignment = True
                        textbook_needed = True
                        if(controller.textbook_info[1] not in controller.student_needed_textbooks):
                            textbook_needed = False
                            attempt_assignment = messagebox.askyesno("???", "This textbook is not needed by this student, would you like to try to assign it to him anyways?")
                        if(attempt_assignment):
                            textbook_assigned = True
                            if(controller.textbook_info[4] == self.current_student_barcode):
                                messagebox.showerror("ERROR", "This textbook is already assigned to this student")
                                textbook_assigned = False
                            elif(controller.textbook_info[1] in controller.student_textbooks_title):
                                messagebox.showerror("ERROR", "Student already took out a copy of " + controller.textbook_info[1] + ". He cannot own more than one type of the same textbook!")
                            elif(controller.textbook_info[4] == "None"):
                                controller.server.assign_t(controller.current_barcode, self.current_student_barcode)
                                self.num_of_textbooks += 1
                                self.student_tnum_label["text"] = "Textbooks taken out: " + str(self.num_of_textbooks)
                            else:
                                option = messagebox.askyesno("Override?", "This textbook is already assigned to " + controller.server.info_s(controller.textbook_info[4])[2] + ". Would you like to replace anyways?")
                                if(option):
                                    controller.server.return_t(controller.current_barcode)
                                    controller.server.assign_t(controller.current_barcode, self.current_student_barcode)
                                    self.num_of_textbooks += 1
                                    self.student_tnum_label["text"] = "Textbooks taken out: " + str(self.num_of_textbooks)
                                else:
                                    textbook_assigned = False
                            if(textbook_assigned and textbook_needed):
                                for x in range(0, len(controller.student_needed_textbooks)):
                                    if(controller.textbook_info[1] == controller.student_needed_textbooks[x]):
                                        del controller.student_needed_textbooks[x]
                                        self.textbook_list.delete(x)
                                        controller.student_textbooks_title.append(controller.textbook_info[1])
                                        if(len(controller.student_needed_textbooks) == 0):
                                            messagebox.showinfo("DONE!", controller.student_info[2] + " is done taking out his textbooks!")
                                        break
                    else:
                        if(controller.textbook_info[4] == self.current_student_barcode):
                            self.num_of_textbooks -= 1
                            self.student_tnum_label["text"] = "Textbooks taken out: " + str(self.num_of_textbooks)
                            self.textbook_list.delete(controller.student_textbooks.index(controller.current_barcode))
                            controller.student_textbooks.remove(controller.current_barcode)
                            controller.server.return_t(controller.current_barcode)
                            ###
                            #price
                            #waiting for functions to be complete
                            ###
                            if(not self.num_of_textbooks):
                                messagebox.showwarning("Done!", controller.student_info[2] + " is done returning textbooks!")
                        elif(controller.textbook_info[4] != "None"):
                            print(controller.textbook_info)
                            messagebox.showerror("ERROR", "You are trying to return a textbook that belongs to " + (controller.server.info_s(controller.textbook_info[4]))[2])
                        else:
                            messagebox.showerror("ERROR", "This textbook actually belongs to nobody")
                else:
                    messagebox.showerror("Error", "You gotta scan in a student's barcode first my dude...")
            else:
                messagebox.showerror("Error", "I don't know what you scanned in my dude")
            self.barcode_label["text"] = "Current Barcode: " + controller.current_barcode

    def switch_mode(self):
        self.clear()
        if(self.day == 'D'):
            self.day = 'R'
            self.mode_label["text"] = "Mode: Return"
            self.student_textbooks_label["text"] = "Student Textbooks: "
            messagebox.showwarning("Mode Switched!", "Mode has been changed to return mode!")
        else:
            self.day = 'D'
            self.mode_label["text"] = "Mode: Distribution"
            self.student_textbooks_label["text"] = "Needed Textbooks: "
            messagebox.showwarning("Mode Switched!", "Mode has been changed to distribution mode")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controlller = controller
        TextbookManagement.configure(self, background = MAROON)
        
        self.barcode_label = tk.Label(self, text = "Current Barcode: ", font = controller.MENU_FONT, bg = MAROON)
        self.barcode_label.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "W")
        self.barcode_status_label = tk.Label(self, text = "Barcode Type: ", font = controller.MENU_FONT, bg = MAROON)
        self.barcode_status_label.grid(row = 0, column = 0, padx = 10, pady = (40, 0), sticky = "W")
        
        textbook_info_label = tk.Label(self, text = "Textbook Info", font = controller.SUBTITLE_FONT, bg = MAROON)
        textbook_info_label.grid(row = 1, column = 0, padx = 10, pady = (30, 0),  sticky = "W")
        self.textbook_title_label = tk.Label(self, text = "Textbook Title: ", font = controller.MENU_FONT, bg = MAROON)
        self.textbook_title_label.grid(row = 2, column = 0, padx = 10, sticky = "W")
        self.textbook_condition_label = tk.Label(self, text = "Textbook Condition: ", font = controller.MENU_FONT, bg = MAROON)
        self.textbook_condition_label.grid(row = 3, column = 0, padx = 10, sticky = "W")
        self.textbook_price_label = tk.Label(self, text = "Textbook Price: ", font = controller.MENU_FONT, bg = MAROON)
        self.textbook_price_label.grid(row = 4, column = 0, padx = 10, sticky = "W")

        student_info_label = tk.Label(self, text = "Student Info", font = controller.SUBTITLE_FONT, bg = MAROON)
        student_info_label.grid(row = 5, column = 0, padx = 10, pady = (20, 0),  sticky = "W")
        self.student_name_label = tk.Label(self, text = "Student Name: ", font = controller.MENU_FONT, bg = MAROON)
        self.student_name_label.grid(row = 6, column = 0, padx = 10, sticky = "W")
        self.student_grade_label = tk.Label(self, text = "Student Grade: ", font = controller.MENU_FONT, bg = MAROON)
        self.student_grade_label.grid(row = 7, column = 0, padx = 10, sticky = "W")
        self.student_tnum_label = tk.Label(self, text = "Textbooks taken out: ", font = controller.MENU_FONT, bg = MAROON)
        self.student_tnum_label.grid(row = 8, column = 0, padx = 10, sticky = "W")

        selection_button = tk.Button(self, text = "Switch Mode", font = controller.MENU_FONT, command = lambda : self.switch_mode())
        selection_button.grid(row = 9, column = 0, padx = 10, pady = (20,0), sticky = "W")
        self.mode_label = tk.Label(self, text = "Mode: Distribution", font = controller.SUBTITLE_FONT, bg = MAROON)
        self.mode_label.grid(row = 10, column = 0, padx = 10, sticky = "W")
        self.student_textbooks_label = tk.Label(self, text = "Needed Textbooks: ", font = controller.SUBTITLE_FONT, bg = MAROON)
        self.student_textbooks_label.grid(row = 0, column = 1, sticky = "W", pady = (30, 0))
        back_button = controller.make_back_button(controller = self)
        back_button.grid(row = 11, column = 0, padx = 10, pady = (40,0), sticky = "W")
        invisible_label = tk.Label(self, text = "", bg = MAROON)
        invisible_label.grid(row = 12, padx = 150)
        self.textbook_list = tk.Listbox(self, bd = 0, bg = MAROON, font = controller.MENU_FONT, selectmode = "SINGLE", selectbackground = MAROON)
        self.textbook_list.grid(row = 1, column = 1, sticky = "NW", rowspan = 10)
        ###self.textbook_list.bind('<<ListboxSelect>>', lambda event: self.select_textbook(event,controller))### unsure if needed

class TeacherAssignment(tk.Frame):

    idx = -1
    cidx = -1
    current_teacher = ""
    course_selected = False
    teacher_selected = False
    identical_courses = False
    teacher_courses = []
    courses_info = []
    full_courses_info = []
    textbook_nums = 0
    current_textbook_list = []
    disable_lambda1 = False
    disable_lambda2 = False
    changes_made = False
    new_course = False

    def can_enter(self, controller):
        if(controller.server.ping()):
            controller.check_requisites = True
            print(controller.textbook_list)
        else:
            controller.check_requisites = False

    def clear(self):
        pass

    def barcode_scanned(self, controller):
        pass

    def display_teacher_info(self, controller):
        self.course_list.delete(0, tk.END)
        course_check = []
        self.courses_info.clear()
        self.full_courses_info.clear()
        cnt = 0
        for course in self.teacher_courses:
            course_info = controller.server.info_c(course)
            print(course_info)
            if(self.identical_courses):
                self.course_list.insert(cnt, course_info[1])
                self.courses_info.append(course_info)
                cnt += 1
            else:
                if(course_info[1] not in course_check):
                    self.course_list.insert(cnt, course_info[1])
                    self.courses_info.append(course_info)
                    course_check.append(course_info[1])
                    cnt += 1
            self.full_courses_info.append(course_info)
                    
    def display_identical_courses(self,controller):
        self.identical_courses = not self.identical_courses
        self.display_teacher_info(controller)
        if(self.identical_courses):
            self.identical_button["text"] = "Revert"
        else:
            self.identical_button["text"] = "Display Identical Courses"

    def select_course(self, event, controller):
        if(self.course_list.curselection()):
            check = True
            if(self.changes_made and self.course_list.curselection()[0] != self.cidx):
                check = messagebox.askyesno("Changes", "You've made changes to this course's textbooks, are you sure you want to discard them?")
            elif(check and self.course_list.curselection()[0] != self.cidx or self.new_course):
                self.new_course = False
                self.changes_made = False
                self.course_selected = True
                self.cidx = (self.course_list.curselection()[0])
                self.course_name_label["text"] = "Course Name: " + self.course_list.get(self.cidx)
                self.course_textbooks.delete(0, tk.END)
                self.current_course_textbooks = controller.server.course_r(self.courses_info[self.cidx][0])
                print(self.current_course_textbooks)
                self.textbook_nums = 0
                self.current_textbook_list.clear()
                for textbook in self.current_course_textbooks:
                    if(len(textbook) > 0):
                        self.course_textbooks.insert(self.textbook_nums, textbook)
                        self.textbook_nums += 1
                        self.current_textbook_list.append(textbook)


    def select_textbook(self, event, controller):
        if(self.course_textbooks.curselection()):
            self.idx = (self.course_textbooks.curselection()[0])

    def delete_selected_textbook(self, controller):
        if(self.idx > -1):
            del self.current_textbook_list[self.idx]
            self.course_textbooks.delete(self.idx)
            self.textbook_nums -= 1
            self.changes_made = True
        else:
            messagebox.showerror("ERROR", "Please select a textbook you would like to delete")

    def add_textbook(self, controller):
        if(not self.teacher_selected):
            messagebox.showerror("Error", "Please let my poor program know who you are before you click fancy buttons -Derek")
        elif(not self.course_selected):
            messagebox.showerror("Error", "Please select a course first before adding textbooks")
        else:
            self.disable_lambda1 = True
            self.disable_lambda2 = True
            current_textbook_name = window.add_textbook_window(self, controller).show()
            self.disable_lambda1 = False
            self.disable_lambda2 = False
            if(current_textbook_name in self.current_textbook_list):
                messagebox.showwarning("WARNING", "You already have the identical textbook for this course")
            elif(len(current_textbook_name) > 0):
                self.changes_made = True
                self.course_textbooks.insert(self.textbook_nums, current_textbook_name)
                self.current_textbook_list.append(current_textbook_name)

    def confirm_changes(self, controller):
        self.changes_made = False
        self.new_course = True
        print(self.current_textbook_list)
        print(self.cidx)
        if(self.identical_courses):
            controller.server.set_course_r(self.teacher_courses[self.cidx], self.current_textbook_list)
        else:
            for course in self.full_courses_info:
                if(course[1] == self.courses_info[self.cidx][1]):
                    controller.server.set_course_r(course[0], self.current_textbook_list)


    def search_teacher(self, controller):
        check = False
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        if(first_name and last_name):
            for t_name in self.teachers:
                if(first_name.lower() in t_name.lower() and last_name.lower() in t_name.lower()):
                    confirm = messagebox.askyesno(title = "Confirm", message = "Are you " + t_name + "?")
                    if(confirm):
                        check = True
                        self.current_teacher = t_name
                        self.teacher_courses = controller.server.get_teacher_c(self.current_teacher)
                        print("TEACHER COURSES: ", self.teacher_courses)
                        self.display_teacher_info(controller)
                        self.course_selected = False
                        self.teacher_selected = True
                        break
                    else:
                        messagebox.showinfo("YOU ARE WHO YOU ARE", "NANI?!?")
        if(not check):
            messagebox.showerror(title = "Error", message = "YOU ARE NOBODY")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        TeacherAssignment.configure(self, background = MAROON)

        self.courses = controller.scanner.server.courses_n()
        self.teachers = controller.scanner.server.get_teachers()
        controller.make_back_button(self).grid(row = 8, column = 0, padx = 10, pady = (15,0))
        self.first_name_entry = tk.Entry(self)
        self.last_name_entry = tk.Entry(self)
        teacher_name_label = tk.Label(self, text = "Who art thee?", font = controller.SUBTITLE_FONT, bg = MAROON)
        teacher_name_label.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan = 2)
        first_name_label = tk.Label(self, text = "First Name:", font = controller.MENU_FONT, bg = MAROON)
        last_name_label = tk.Label(self, text = "Last Name:", font = controller.MENU_FONT, bg = MAROON)
        first_name_label.grid(row = 1, column = 0)
        last_name_label.grid(row = 2, column = 0)
        self.first_name_entry.grid(row = 1, column = 1)
        self.last_name_entry.grid(row = 2, column = 1)

        self.search_button = tk.Button(self, text = "Search that I exist", font = controller.BUTTON_FONT, command = lambda: self.search_teacher(controller))
        self.search_button.grid(row = 3, column = 0, pady = 10, columnspan = 2)
        courses_label = tk.Label(self, text = "Courses", font = controller.SUBTITLE_FONT, bg = MAROON)
        courses_label.grid(row = 4, column = 0, padx = 10, pady = (5,0), columnspan = 2, sticky = "W")
        self.course_list = tk.Listbox(self, bd = 0, bg = MAROON, font = controller.MENU_FONT, selectmode = "SINGLE", selectbackground = MAROON)
        self.course_list.grid(row = 5, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = "W")
        self.identical_button = tk.Button(self, text = "Display Identical Courses", font = controller.BUTTON_FONT, command = lambda: self.display_identical_courses(controller))
        self.identical_button.grid(row = 6, column = 0, columnspan = 3, padx = 10, pady = 2, sticky = "W")
        self.course_list.bind('<<ListboxSelect>>', lambda event: self.select_course(event,controller))
        self.invisible_label = tk.Label(self, text = "", bg = MAROON)
        self.invisible_label.grid(row = 0, column = 4, padx = 30)
        self.course_info_label = tk.Label(self, text = "Course Info:", font = controller.SUBTITLE_FONT, bg = MAROON)
        self.course_info_label.grid(row = 0, column = 5, pady = (10,0), columnspan = 3, sticky = "W")
        self.course_name_label = tk.Label(self, text = "Course Name: ", font = controller.MENU_FONT, bg = MAROON)
        self.course_name_label.grid(row = 1, column = 5, sticky = "W", columnspan = 2)
        self.course_section_label = tk.Label(self, text = "Course Section: ", font = controller.MENU_FONT, bg = MAROON)
        self.course_section_label.grid(row = 2, column = 5, sticky = "W")
        self.course_textbook_label = tk.Label(self, text = "Course Textbooks:", font = controller.SUBTITLE_FONT, bg = MAROON)
        self.course_textbook_label.grid(row = 4, column = 5, sticky = "W")
        self.course_textbooks = tk.Listbox(self, bd = 0, bg = MAROON, font = controller.MENU_FONT, selectmode = "SINGLE", selectbackground = MAROON)
        self.course_textbooks.grid(row = 5, column = 5, pady = 5, sticky = "NW")
        self.course_textbooks.bind('<<ListboxSelect>>', lambda event: self.select_textbook(event,controller))
        self.button_container = tk.Frame(self)
        self.button_container["bg"] = MAROON
        self.button_container.grid(row = 5, column = 6, rowspan = 3, pady = 5, sticky = "NW")
        self.remove_textbook_button = tk.Button(self.button_container, text = "Remove Textbook", font = controller.BUTTON_FONT, command = lambda : self.delete_selected_textbook(controller))
        self.remove_textbook_button.grid(row = 0, column = 0, padx = 6, sticky = "N")
        self.add_textbook_button = tk.Button(self.button_container, text = "Add Textbook", font = controller.BUTTON_FONT, command = lambda : self.add_textbook(controller))
        self.add_textbook_button.grid(row = 1, column = 0,  padx = 6, sticky = "W")
        self.confirm_button = tk.Button(self, text = "Confirm Changes", font = controller.BUTTON_FONT, command = lambda : self.confirm_changes(controller))
        self.confirm_button.grid(row = 6, column = 5, sticky = "W")

class TextbookScanner(tk.Frame): 
    values_set = False
    current_title = ""
    current_price = 0
    current_condition = 0
    num_scanned = 0

    def can_enter(self, controller):
        controller.check_requisites = True

    def clear(self):
        pass

    def barcode_scanned(self, controller):
        if(self.values_set):
            if(controller.barcode_status == "Textbook"):
                if(controller.textbook_info[1] == self.current_title and float(controller.textbook_info[2]) == self.current_price):
                    messagebox.showerror("Error", "This textbook has the same values as the set values")                        
                else: 
                    MsgOption = messagebox.askyesno("Textbook already in database!", "Would you like to replace the original values?")
                    if(MsgOption == "yes"):
                        self.num_scanned += 1
                        self.textbook_label.config(text = "Number of textbooks scanned: " + str(self.num_scanned))
                        controller.server.delete_t(controller.current_barcode)
                        controller.server.add_t(controller.current_barcode, self.current_title, str(self.current_price), str(self.current_condition))
            elif(controller.barcode_status == "Student"):
                messagebox.showwarning("Warning!", "You are scanning in a student's barcode ID!")
            else:
                self.num_scanned += 1
                self.barcode_label.config(text = "Current Barcode: " + controller.current_barcode)
                self.textbook_label.config(text = "Number of textbooks scanned: " + str(self.num_scanned))
                self.current_condition = calculations.get_textbook_condition(self.condition_entry.get())
                self.current_title = self.title_entry.get()
                print("TITLE: " + self.current_title)
                controller.server.add_t(controller.current_barcode, self.current_title, str(self.current_price), str(self.current_condition))
        else:
            messagebox.showerror("Error", "Please set the values before scanning in a barcode")

    def set_values(self, controller):
        if(self.values_set):
            self.set_button.config(text = "SET VALUES")
            self.title_entry.config(state = "normal")
            self.price_entry.config(state = "normal")
            self.textbook_label.config(text = "Number of textbooks scanned:")
            self.num_scanned = 0
            self.values_set = False
        else:
            price_string = self.price_entry.get()
            try:
                similar_list = calculations.check_similarity(self.title_entry.get(), controller.textbook_list)
                print(similar_list)
                self.current_price = float(price_string)
                self.set_button.config(text = "RESET")
                self.textbook_label.config(text = "Number of textbooks scanned: " + str(self.num_scanned))
                self.title_entry.config(state = "disabled")
                self.price_entry.config(state = "disabled")
                self.values_set = True
            except ValueError:
                messagebox.showerror("Error", "Please make sure that the price is actually a number")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        TextbookScanner.configure(self, background = MAROON)
        
        #labels
        main_label = tk.Label(self, text="Textbook Scanner", font = controller.TITLE_FONT, bg = MAROON)
        main_label.grid(row = 0, column = 0, padx = (95,0))
        title_label = tk.Label(self, text = "Title:", font = controller.SUBTITLE_FONT, bg = MAROON)
        title_label.grid(row = 1, column = 0, padx = 10, pady = (20, 0), sticky = "W")
        condition_label = tk.Label(self, text = "Condition:", font = controller.SUBTITLE_FONT, bg = MAROON)
        condition_label.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = "W")
        price_label = tk.Label(self, text = "Price:", font = controller.SUBTITLE_FONT, bg = MAROON)
        price_label.grid(row = 5, column = 0, padx = 10, pady = 5, sticky = "W")
        self.barcode_label = tk.Label(self, text = "Current Barcode: ", font = controller.MENU_FONT, bg = MAROON)
        self.barcode_label.grid(row = 3, column = 0, padx= (290,0) , pady = (20,0), sticky = "W")
        self.textbook_label = tk.Label(self, text = "Number of textbooks scanned: ", font = controller.MENU_FONT, bg = MAROON)
        self.textbook_label.grid(row = 4, column = 0, padx = (290, 0), sticky = "W")

        #buttons
        back_button = controller.make_back_button(controller = self)
        back_button.grid(row = 8, column = 0, padx = 10, pady = (120,0), sticky = "W")
        self.set_button = tk.Button(self, text = "Set Values", command = lambda : self.set_values(controller = controller), font = controller.BUTTON_FONT)
        self.set_button.grid(row = 7, column = 0, padx = 10, pady = 10, sticky = "W")

        #entry points
        self.title_entry = tk.Entry(self, font = controller.FIELD_FONT)
        self.title_entry.grid(row = 2, column = 0, padx = 10, pady = (0,10), sticky = "W")
        self.price_entry = tk.Entry(self, font = controller.FIELD_FONT)
        self.price_entry.grid(row = 6, column = 0, padx = 10, pady = (0,10), sticky = "W")
        self.condition_choices = ["New", "Good", "Fair", "Poor", "Destroyed"]
        self.condition_entry = ttk.Combobox(self, values = self.condition_choices, font = controller.FIELD_FONT, state = "readonly", width = 10)
        self.condition_entry.set("New")
        self.condition_entry.grid(row = 4, column = 0, padx = 10, pady = (0,10), sticky = "W")

class Info(tk.Frame):

    textbook_selected = False
    textbook_selected_index = 0
    textbook_list_made = False

    def can_enter(self, controller):
        return True

    def clear(self):
        self.barcode_label.config(text = "Current Barcode: ")
        self.barcode_status_label.config(text = "Barcode Type: ")
        self.textbook_title_label.config(text = "Textbook Title: ")
        self.textbook_condition_label.config(text = "Textbook Condition: ")
        self.textbook_price_label.config(text = "Textbook Price: ")
        self.student_name_label.config(text = "Student Name: ")
        self.textbook_barcode_label["text"] = "Textbook Barcode: "
        if(self.textbook_list_made):
            self.textbook_list_made = False
            self.textbook_list.delete(0, tk.END)
            self.textbook_list.grid_forget()

    def select_textbook(self, event, controller):
        self.textbook_selected = True
        self.textbook_selected_index = int((self.textbook_list.curselection())[0])
        controller.textbook_info = controller.server.info_t(controller.student_textbooks[self.textbook_selected_index])
        self.display_textbook_info(controller)

    def display_textbook_info(self, controller):
        self.textbook_title_label["text"] = "Textbook Title: " + controller.textbook_info[1]
        self.textbook_condition_label["text"] = "Textbook Condition: " + calculations.get_textbook_condition_rev(controller.textbook_info[3])
        self.textbook_price_label["text"] = "Textbook Price: " + controller.textbook_info[2]
        self.textbook_barcode_label["text"] = "Textbook Barcode " + controller.textbook_info[0]

    def barcode_scanned(self, controller):
        self.textbook_selected = False
        if(controller.barcode_status == "Student"):
            self.clear()
            self.student_name_label.config(text = "Student Name: " + controller.student_info[2])
            cnt = 1
            self.textbook_list = tk.Listbox(self, bd = 0, bg = MAROON, font = controller.MENU_FONT, selectmode = "SINGLE", selectbackground = MAROON)
            for textbook in controller.student_textbooks:
                textbook_info = controller.server.info_t(textbook)
                self.textbook_list.insert(cnt, textbook_info[1])
                cnt += 1
            self.textbook_list.grid(row = 1, column = 1, sticky = "NW", rowspan = 10)
            self.textbook_list.bind('<<ListboxSelect>>', lambda event: self.select_textbook(event,controller))

        elif(controller.barcode_status == "Textbook"):
            self.clear()
            print(controller.textbook_info[4])
            if(controller.textbook_info[4] != "None"):
                self.student_name_label["text"] = "Textbook Owner: " + controller.server.info_s(controller.textbook_info[4])[2]
            else:
                self.student_name_label["text"] = "Textbook Owner: N/A"
            self.display_textbook_info(controller)
        else:
            self.clear()
            messagebox.showerror("Fatal Error", "WTF DID YOU SCAN IN BOI????")
        self.barcode_label.config(text = "Current Barcode: " + str(controller.current_barcode))
        self.barcode_status_label["text"] = "Barcode Type: " + controller.barcode_status

    def delete_textbook(self, controller):
        if(controller.server.ping()):
            if(controller.barcode_status == "Textbook"):
                controller.server.delete_t(controller.current_barcode)
                messagebox.showwarning("DELETED!", "This textbook has been deleted")
                self.clear()
            elif(self.textbook_selected):
                option = messagebox.askyesno("Warning", "Would you like to the delete (return) the textbook you selected?")
                if(option):
                    controller.server.return_t(controller.textbook_info[0])
                    self.textbook_list.delete(self.textbook_selected_index)
                    controller.student_textbooks.remove(controller.textbook_info[0])
            else:
                messagebox.showerror("ERROR", "Please select a textbook you would like to delete")


    def add_student(self, controller):
        self.w = window.add_student_window(self.master, controller)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        Info.configure(self, background = MAROON)

        self.barcode_label = tk.Label(self, text = "Current Barcode: ", font = controller.MENU_FONT, bg = MAROON)
        self.barcode_label.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "W")
        self.barcode_status_label = tk.Label(self, text = "Barcode Type: ", font = controller.MENU_FONT, bg = MAROON)
        self.barcode_status_label.grid(row = 0, column = 0, padx = 10, pady = (50, 0), sticky = "W")
        
        textbook_info_label = tk.Label(self, text = "Textbook Info", font = controller.SUBTITLE_FONT, bg = MAROON)
        textbook_info_label.grid(row = 1, column = 0, padx = 10, pady = (30, 0),  sticky = "W")
        self.textbook_title_label = tk.Label(self, text = "Textbook Title: ", font = controller.MENU_FONT, bg = MAROON)
        self.textbook_title_label.grid(row = 2, column = 0, padx = 10, sticky = "W")
        self.textbook_condition_label = tk.Label(self, text = "Textbook Condition: ", font = controller.MENU_FONT, bg = MAROON)
        self.textbook_condition_label.grid(row = 3, column = 0, padx = 10, sticky = "W")
        self.textbook_price_label = tk.Label(self, text = "Textbook Price: ", font = controller.MENU_FONT, bg = MAROON)
        self.textbook_price_label.grid(row = 4, column = 0, padx = 10, sticky = "W")
        self.textbook_barcode_label = tk.Label(self, text = "Textbook Barcode: ", font = controller.MENU_FONT, bg = MAROON)
        self.textbook_barcode_label.grid(row = 5, column = 0, padx = 10, sticky = "W")

        student_info_label = tk.Label(self, text = "Student Info", font = controller.SUBTITLE_FONT, bg = MAROON)
        student_info_label.grid(row = 6, column = 0, padx = 10, pady = (20, 0),  sticky = "W")
        self.student_name_label = tk.Label(self, text = "Student Name: ", font = controller.MENU_FONT, bg = MAROON)
        self.student_name_label.grid(row = 7, column = 0, padx = 10, sticky = "W")
        self.student_grade_label = tk.Label(self, text = "Student Grade: ", font = controller.MENU_FONT, bg = MAROON)
        self.student_grade_label.grid(row = 8, column = 0, padx = 10, sticky = "W")
        invisible_label = tk.Label(self, text = "", bg = MAROON)
        invisible_label.grid(row = 12, padx = 150)
        student_textbooks_label = tk.Label(self, text = "Student Textbooks: ", font = controller.SUBTITLE_FONT, bg = MAROON)
        student_textbooks_label.grid(row = 0, column = 1, sticky = "W", pady = (30, 0))
        
        pady_dif_back = 0
        if(controller.version == "teacher"):
            delete_button = tk.Button(self, text = "Delete Textbook", font = controller.MENU_FONT, command = lambda: self.delete_textbook(controller = controller))
            delete_button.grid(row = 9, column = 0, padx = 10, pady = (20, 0), sticky = "W")    
            pady_dif_back = 110    
            self.add_s = tk.Button(self, text = "Add student", font = controller.MENU_FONT, command= lambda: self.add_student(controller = controller))
            self.add_s.grid(row = 10, column = 0, padx = 10, pady = (10,0), sticky = "W")
        back_button = controller.make_back_button(controller = self)
        back_button.grid(row = 11, column = 0, padx = 10, pady = (132 - pady_dif_back,0), sticky = "W")



root = client()
root.title("DigiText")
root.iconbitmap("sphs_icon.ico")
root.geometry("600x500")
root.mainloop()

        



