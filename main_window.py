import tkinter as tk

from tab_menu import TabMenu


class MainWindow(tk.Frame):     # self -> tk.Frame
    def __init__(self, root, controller, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        # Main window contents
        self.tab_menu = TabMenu(self, controller)
        self.tab_menu.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.pack(fill=tk.BOTH, expand=True)
