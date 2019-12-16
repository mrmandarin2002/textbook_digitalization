#Digitext Program written in python as JavaFX is the definition of cancer

import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
import time, keyboard

MAIN_FONT = "Comic Sans MS"
MAROON = '#B03060'
PINK = '#FF00D4'
NEON_GREEN = '#4DFF4D'

class client(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        start = time.time()
        tk.Tk.__init__(self, *args, **kwargs)

        self.scene_list = (WelcomePage, Menu, TextbookManagement, TextbookInfo, TextbookScanner, TextbookDeleter)
        self.TITLE_FONT = tkfont.Font(family=MAIN_FONT, size=20, weight="bold")
        self.BUTTON_FONT = tkfont.Font(family=MAIN_FONT, size=10)
        self.BACK_BUTTON_FONT = tkfont.Font(family = MAIN_FONT, size = 8)
        self.MENU_FONT = tkfont.Font(family=MAIN_FONT, size=11)

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

        self.show_frame("WelcomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    #allows the creation of buttons
    def make_button(self, controller, d_text, scene, option):
        if(option == "menu"):
            return tk.Button(controller, text = d_text, command = lambda: self.show_frame(scene), font = self.MENU_FONT, fg = PINK)
        else:
            return tk.Button(controller, text = d_text, command = lambda: self.show_frame(scene), font = self.BUTTON_FONT)
    
    def make_back_button(self, controller):
        return tk.Button(controller, text = "Back to Menu", command = lambda: self.show_frame("Menu"), font = self.BACK_BUTTON_FONT)

class WelcomePage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        WelcomePage.configure(self, background = MAROON)
        welcome_title = tk.Label(self, text = "Welcome to DigiText!!", font = controller.TITLE_FONT , bg = MAROON)
        welcome_title.pack(side = "top", pady = 150, padx = 50)
        welcome_button = controller.make_button(controller = self, d_text = "Press to continue...", scene = "Menu", option = '')
        welcome_button.pack()
        
class Menu(tk.Frame):
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
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controlller = controller

class TextbookScanner(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controlller = controller

        TextbookScanner.configure(self, background = MAROON)
        back_button = controller.make_back_button(controller = self)
        back_button.grid(row = 5, column = 0, padx = 5, pady = 5)


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