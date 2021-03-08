import tkinter as tk

from model import Model
from view import View
from menu_bar import MenuBar


class Controller:
    def __init__(self):
        self.root = tk.Tk()
        self.model = Model()
        self.view = View(self.root, self.model)
        self.menu = MenuBar(self.root)

    def run(self):
        self.root.title("DVTH")
        self.root.geometry("800x800")
        self.root.deiconify()
        self.root.protocol("WM_DELETE_WINDOW", self.model.on_close)
        self.root.config(menu=self.menu)
        self.root.mainloop()
