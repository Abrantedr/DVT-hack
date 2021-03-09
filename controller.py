import tkinter as tk

from main_window import MainWindow
from menu_bar import MenuBar
from model import Model


class Controller:
    def __init__(self):
        self.root = tk.Tk()

        # Controller receives model and views
        self.model = Model()
        self.menu_bar = MenuBar(self.root)
        self.main_window = MainWindow(self.root, self)  # Sends controller to main window

    def write(self):    # Controller calls model
        self.model.write()

    def read(self):
        self.model.read()

    def run(self):
        self.root.title("DVTH")
        self.root.geometry("800x800")
        self.root.deiconify()
        self.root.protocol("WM_DELETE_WINDOW", self.model.on_close)
        self.root.config(menu=self.menu_bar)
        self.root.mainloop()