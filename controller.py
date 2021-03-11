import tkinter as tk

# Model
from model import Model

# Views
from main_window import MainWindow
from menu_bar import MenuBar


class Controller:
    def __init__(self):
        # Controller holds the main application
        self.root = tk.Tk()

        # Controller receives model and views
        self.model = Model(self)
        self.menu_bar = MenuBar(self.root)
        self.main_window = MainWindow(self.root, self)  # Sends controller to main window

    def write(self, command, index, subindex):    # Controller calls model
        self.model.send(command, index, subindex)

    def update_label(self, b):
        self.main_window.tab_menu.tab_main.nmt.set(b)

    def parse_queue(self):
        pass

    def on_close(self):
        # Set stop conditions for all threads
        self.model.thread_stop.set()
        self.main_window.tab_menu.thread_stop.set()

        # Join non-daemonic threads
        self.main_window.tab_menu.main_tab_sdo_thread.join()

        # End serial communication
        self.model.close()
        exit()  # And get out...

    def run(self):
        self.root.title("DVTH")
        self.root.geometry("800x800")
        self.root.deiconify()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.config(menu=self.menu_bar)
        self.root.mainloop()
