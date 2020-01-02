#Digitext Program written in python as JavaFX is the definition of cancer
import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import ttk
from tkinter import messagebox
import time

#import own files
import interactions, calculations, window
from datetime import datetime
from pynput.keyboard import Key, Listener

MAIN_FONT = "Comic Sans MS"
MAROON = '#B03060'
PINK = '#FF00D4'
NEON_GREEN = '#4DFF4D'

class client(tk.Tk):

    barcode_string = ""
    last_barcode_string = ""
    barcode_scanned = False
    start = datetime.now()
    previous_time = 0
    version = "teacher"

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.server = interactions.Client(address = "127.0.0.1", port = 7356)
        self.scene_list = (WelcomePage, Menu, TextbookManagement, Info, TextbookScanner)

        #different type of fonts used throughout the program
        self.TITLE_FONT = tkfont.Font(family=MAIN_FONT, size=20, weight="bold")
        self.SUBTITLE_FONT = tkfont.Font(family = MAIN_FONT, size = 14, weight = "bold")
        self.FIELD_FONT = tkfont.Font(family = MAIN_FONT, size = 11)
        self.BUTTON_FONT = tkfont.Font(family=MAIN_FONT, size=10)
        self.BACK_BUTTON_FONT = tkfont.Font(family = MAIN_FONT, size = 8)
        self.MENU_FONT = tkfont.Font(family=MAIN_FONT, size=11)
        
        keyLis = Listener(on_press=self.on_press)
        keyLis.start()

        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        for scene in self.scene_list:
            page_name = scene.__name__
            frame = scene(parent=container, controller = self)
            self.frames[page_name] = frame
            frame.grid(row = 0, column = 0, sticky = "nswe")

        self.show_frame("TextbookManagement")

    ##for barcode input
    def on_press(self, key):
        total_elapsed = (datetime.now() - self.start).microseconds + (datetime.now() - self.start).seconds * 1000000
        if(total_elapsed - self.previous_time < 40000):
            if(key != Key.enter and key != Key.shift):
                self.barcode_string += str(key)[1:-1]
            if(key == Key.enter and len(self.barcode_string) > 4):
                self.last_barcode_string = self.barcode_string
                exec(self.current_frame_name + ".barcode_scanned(self = self.current_frame, controller=self)")
        else:
            if(key != Key.enter and key != Key.shift):
                self.barcode_string = str(key)[1:-1]
        self.previous_time = total_elapsed  

    def show_frame(self, page_name):
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

    def clear(self):
        pass

    def barcode_scanned(self, controller):
        pass
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        WelcomePage.configure(self, background = MAROON)
        welcome_title = tk.Label(self, text = "Welcome to DigiText!!", font = controller.TITLE_FONT , bg = MAROON)
        welcome_title.pack(side = "top", pady = 150, padx = 50)
        welcome_button = controller.make_button(controller = self, d_text = "Press to continue...", scene = "Menu", option = '')
        welcome_button.pack()
        
class Menu(tk.Frame):

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
        menu_title.pack(pady = (100, 0))
        m_button.pack(pady = (50, 0))
        s_button.pack()
        i_button.pack()

class TextbookManagement(tk.Frame):

    student_scanned = False
    day = "D"
    current_student_barcode = ""

    def clear(self):
        self.barcode_label.config(text = "Current Barcode: ")
        self.barcode_status_label.config(text = "Barcode Type: ")
        self.textbook_title_label.config(text = "Textbook Title: ")
        self.textbook_condition_label.config(text = "Textbook Condition: ")
        self.textbook_price_label.config(text = "Textbook Price: ")
        self.student_tnum_label.config(text = "Textbooks taken out: ")
        self.student_name_label["text"] = "Student Name:"
 
    def barcode_scanned(self, controller):
        if(controller.server.ping()):
            if(controller.server.valid_s(controller.last_barcode_string)):
                self.clear()
                self.current_student_barcode = ""
                self.student_info = controller.server.info_s(controller.last_barcode_string)
                self.student_textbooks = controller.server.student_t(controller.last_barcode_string)
                self.student_name_label["text"] = "Student Name: " + self.student_info[2]
                self.barcode_status_label.config(text = "Barcode Type: Student")
                self.student_tnum_label["text"] = "Textbooks taken out: " + str(len(self.student_textbooks))

            elif(controller.server.valid_t(controller.last_barcode_string)):
                if(student_scanned):
                    student_info = controller.server.info_s()
                else:
                    messagebox.showerror("Error", "You gotta scan in a student's barcode first my dude...")
            else:
                messagebox.showerror("Error", "I don't know what you scanned in my dude")
            self.barcode_label["text"] = "Current Barcode: " + controller.last_barcode_string

    def switch_mode(self):
        if(self.day == "D"):
            self.day = "R"
            self.mode_label["text"] = "Mode: Return"
            messagebox.showwarning("Mode Switched!", "Mode has been changed to return mode!")
        else:
            self.day = "D"
            self.mode_label["text"] = "Mode: Distribution"
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
        back_button = controller.make_back_button(controller = self)
        back_button.grid(row = 11, column = 0, padx = 10, pady = (40,0), sticky = "W")

class TextbookScanner(tk.Frame): 
    values_set = False
    current_title = ""
    current_price = 0
    current_condition = 0
    num_scanned = 0

    def clear(self):
        pass

    def barcode_scanned(self, controller):
        if(self.values_set):
            if(controller.server.ping()):
                if(controller.server.valid_t(controller.barcode_string)):
                    textbook_info = controller.server.info_t(controller.barcode_string)
                    if(textbook_info[1] == self.current_title and float(textbook_info[2]) == self.current_price):
                        messagebox.showerror("Error", "This textbook has the same values as the set values")                        
                    else:
                        MsgOption = messagebox.askyesno("Textbook already in database!", "Would you like to replace the original values?")
                        if(MsgOption == "yes"):
                            self.num_scanned += 1
                            self.textbook_label.config(text = "Number of textbooks scanned: " + str(self.num_scanned))
                            controller.server.delete_t(controller.barcode_string)
                            controller.server.add_t(controller.barcode_string, self.current_title, str(self.current_price), str(self.current_condition))
                elif(controller.server.valid_s(controller.barcode_string)):
                    messagebox.showwarning("Warning!", "You are scanning in a student's barcode ID!")
                else:
                    self.num_scanned += 1
                    self.barcode_label.config(text = "Current Barcode: " + controller.barcode_string)
                    self.textbook_label.config(text = "Number of textbooks scanned: " + str(self.num_scanned))
                    self.current_condition = calculations.get_textbook_condition(self.condition_entry.get())
                    self.current_title = self.title_entry.get()
                    print("TITLE: " + self.current_title)
                    controller.server.add_t(controller.barcode_string, self.current_title, str(self.current_price), str(self.current_condition))
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
        self.controller = controller
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
        self.set_button = tk.Button(self, text = "Set Values", command = lambda : self.set_values(controller = controller.current_frame), font = controller.BUTTON_FONT)
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

    current_barcode_string = ""

    def clear(self):
        self.barcode_label.config(text = "Current Barcode: ")
        self.barcode_status_label.config(text = "Barcode Type: ")
        self.textbook_title_label.config(text = "Textbook Title: ")
        self.textbook_condition_label.config(text = "Textbook Condition: ")
        self.textbook_price_label.config(text = "Textbook Price: ")
        self.student_name_label.config(text = "Student Name: ")

    def barcode_scanned(self, controller):
        self.current_barcode_string = controller.barcode_string
        if(controller.server.ping()):
            if(controller.server.valid_s(controller.barcode_string)):
                self.clear()
                student_info = controller.server.info_s(controller.barcode_string)
                self.student_name_label.config(text = "Student Name: " + student_info[2])
            elif(controller.server.valid_t(controller.barcode_string)):
                self.clear()
                textbook_info = controller.server.info_t(controller.barcode_string)
                print(textbook_info)
                self.barcode_status_label.config(text = "Barcode Type: Textbook")
                self.textbook_title_label.config(text = "Textbook Title: " + textbook_info[1])
                self.textbook_condition_label.config(text = "Textbook Condition: " + calculations.get_textbook_condition_rev(textbook_info[3]))
                self.textbook_price_label.config(text = "Textbook Price: " + textbook_info[2])
            else:
                messagebox.showerror("Fatal Error", "WTF DID YOU SCAN IN BOI????")
            self.barcode_label.config(text = "Current Barcode: " + str(controller.barcode_string))

    def delete_textbook(self, controller):
        if(controller.server.ping()):
            if(controller.server.valid_s(self.current_barcode_string)):
                messagebox.showerror("Error", "You cannot delete students")
            elif(controller.server.valid_t(self.current_barcode_string)):
                MsgOption = messagebox.askyesno("Warning!", "Are you sure you would like to delete this textbook?")
                if(MsgOption == True):
                    controller.server.delete_t(self.current_barcode_string)
                    self.clear()
            else:
                messagebox.showerror("Error", "Invalid barcode")

    def add_student(self, controller):
        self.w = window.add_student_window(self.master, controller)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        Info.configure(self, background = MAROON)

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
        student_info_label.grid(row = 5, column = 0, padx = 10, pady = (30, 0),  sticky = "W")
        self.student_name_label = tk.Label(self, text = "Student Name: ", font = controller.MENU_FONT, bg = MAROON)
        self.student_name_label.grid(row = 6, column = 0, padx = 10, sticky = "W")
        self.student_grade_label = tk.Label(self, text = "Student Grade: ", font = controller.MENU_FONT, bg = MAROON)
        self.student_grade_label.grid(row = 7, column = 0, padx = 10, sticky = "W")

        pady_dif_back = 0
        if(controller.version == "teacher"):
            delete_button = tk.Button(self, text = "Delete Textbook", font = controller.MENU_FONT, command = lambda: self.delete_textbook(controller = controller))
            delete_button.grid(row = 8, column = 0, padx = 10, pady = (20, 0), sticky = "W")    
            pady_dif_back = 110    
            self.add_s = tk.Button(self, text = "Add student", font = controller.MENU_FONT, command= lambda: self.add_student(controller = controller))
            self.add_s.grid(row = 9, column = 0, padx = 10, pady = (10,0), sticky = "W")
        back_button = controller.make_back_button(controller = self)
        back_button.grid(row = 10, column = 0, padx = 10, pady = (142 - pady_dif_back,0), sticky = "W")

if __name__ =='__main__':
    root = client()
    root.title("DigiText")
    root.iconbitmap("sphs_icon.ico")
    root.geometry("600x500")
    root.mainloop()

        


