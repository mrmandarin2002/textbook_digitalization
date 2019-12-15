#Digitext Program written in python as JavaFX is the definition of cancer

import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3

class client(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.scene_list = (WelcomePage, Menu, TextbookManagement, TextbookInfo, TextbookScanner, TextbookDeleter)
        self.TITLE_FONT = tkfont.Font(family='Times', size=18, weight="bold")

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


class WelcomePage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        welcome_title = tk.Label(self, text = "Welcome to DigiText!!", font = controller.TITLE_FONT)
        welcome_title.pack(side = "top", pady = 50, padx = 50)
        welcome_button = tk.Button(self, text = "Click to continue", command = lambda: controller.show_frame("Menu"));
        welcome_button.pack()
        


class Menu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controlller = controller
        dis_button = tk.Button(self, text = "Textbook Distribution");
        dis_button.pack()

class TextbookManagement(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controlller = controller

class TextbookScanner(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controlller = controller

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