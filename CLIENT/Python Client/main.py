#Digitext Program written in python as JavaFX is the definition of cancer
import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import ttk
import time

#import own files
import interactions, calculations
from datetime import datetime
from pynput.keyboard import Key, Listener

MAIN_FONT = "Comic Sans MS"
MAROON = '#B03060'
PINK = '#FF00D4'
NEON_GREEN = '#4DFF4D'


class client(tk.Tk):

    barcode_string = ""
    barcode_scanned = False
    start = datetime.now()
    previous_time = 0
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.server = interactions.Client(address = "127.0.0.1", port = 7356)
        self.scene_list = (WelcomePage, Menu, TextbookManagement, TextbookInfo, TextbookScanner, TextbookDeleter)

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

        self.show_frame("TextbookScanner")

    ##for barcode input
    def on_press(self, key):
        total_elapsed = (datetime.now() - self.start).microseconds + (datetime.now() - self.start).seconds * 1000000
        if(total_elapsed - self.previous_time < 40000):
            if(key != Key.enter and key != Key.shift):
                self.barcode_string += str(key)[1:-1]
            if(key == Key.enter and len(self.barcode_string) > 4):
                exec(self.current_frame_name + ".barcode_scanned(self = self.current_frame, controller=self)")
        else:
            if(key != Key.enter and key != Key.shift):
                self.barcode_string = str(key)
            print(self.server.ping())
        self.previous_time = total_elapsed  

    def show_frame(self, page_name):
        self.current_frame = self.frames[page_name]
        self.current_frame_name = page_name
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
    
    def barcode_scanned(self, controller):
        pass

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controlller = controller

        Menu.configure(self, background = MAROON)
        menu_title = tk.Label(self, text = "DigiText Menu", font = controller.TITLE_FONT , bg = MAROON)
        m_button = controller.make_button(controller = self, d_text = "Textbook Management", scene = "TextbookManagement", option = "menu")
        s_button = controller.make_button(controller = self, d_text = "Textbook Scanner", scene = "TextbookScanner", option = "menu")
        d_button = controller.make_button(controller = self, d_text = "Textbook Deleter", scene = "TextbookDeleter", option = "menu")
        i_button = controller.make_button(controller = self, d_text = "Textbook Info", scene = "TextbookInfo", option = "menu")
        menu_title.pack(pady = (100, 0))
        m_button.pack(pady = (50, 0))
        s_button.pack()
        d_button.pack()
        i_button.pack()

class TextbookManagement(tk.Frame):

    def barcode_scanned(self, controller):
        pass

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controlller = controller

class TextbookScanner(tk.Frame): 
    values_set = True
    current_title = ""
    current_price = 0
    current_condition = 0

    def barcode_scanned(self, controller):
        print(controller.barcode_string)

    def set_values(self, controller):
        if(self.values_set):
            self.set_button.config(text = "RESET")
            
        else:
            self.set_button.config(text = "Set Values")
        self.values_set = not self.values_set
        self.current_condition = calculations.get_textbook_condition(self.condition_entry.get())
        self.current_price = calculations.get_price()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        TextbookScanner.configure(self, background = MAROON)
        
        #labels
        main_label = tk.Label(self, text="Textbook Scanner", font = controller.TITLE_FONT, bg = MAROON)
        main_label.grid(row = 0, column = 0, padx = (178,0))
        title_label = tk.Label(self, text = "Title:", font = controller.SUBTITLE_FONT, bg = MAROON)
        title_label.grid(row = 1, column = 0, padx = 10, pady = (20, 0), sticky = "W")
        condition_label = tk.Label(self, text = "Condition:", font = controller.SUBTITLE_FONT, bg = MAROON)
        condition_label.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = "W")
        price_label = tk.Label(self, text = "Price:", font = controller.SUBTITLE_FONT, bg = MAROON)
        price_label.grid(row = 5, column = 0, padx = 10, pady = 10, sticky = "W")
        self.barcode_label = tk.Label(self, text = "Current Barcode: ", font = controller.MENU_FONT, bg = MAROON)
        self.barcode_label.grid(row = 1, column = 0, padx= (290,0) , pady = (20,0), sticky = "W")
        self.textbook_label = tk.Label(self, text = "Number of textbooks scanned: ", font = controller.MENU_FONT, bg = MAROON)
        self.textbook_label.grid(row = 2, column = 0, padx = (290, 0), sticky = "W")

        #buttons
        back_button = controller.make_back_button(controller = self)
        back_button.grid(row = 8, column = 0, padx = 10, pady = (100,0), sticky = "W")
        self.set_button = tk.Button(self, text = "Set Values", command = lambda : self.set_values(controller = controller.current_frame), font = controller.BUTTON_FONT)
        self.set_button.grid(row = 7, column = 0, padx = 10, pady = 10, sticky = "W")

        #entry points
        self.title_entry = tk.Entry(self, font = controller.FIELD_FONT)
        self.title_entry.grid(row = 2, column = 0, padx = 10, pady = (0,10), sticky = "W")
        self.price_entry = tk.Entry(self, font = controller.FIELD_FONT)
        self.price_entry.grid(row = 6, column = 0, padx = 10, pady = (0,10), sticky = "W")
        self.condition_choices = ["New", "Good", "Fair", "Poor", "Destroyed"]
        self.condition_entry = ttk.Combobox(self, values = self.condition_choices,  state = "readonly")
        self.condition_entry.set("New")
        self.condition_entry.grid(row = 4, column = 0, padx = 10, pady = (0,10), sticky = "W")


class TextbookDeleter(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controlller = controller

class TextbookInfo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controlller = controller

if __name__ =='__main__':
    root = client()
    root.title("DigiText")
    root.iconbitmap("sphs_icon.ico")
    root.geometry("600x500")
    root.mainloop()