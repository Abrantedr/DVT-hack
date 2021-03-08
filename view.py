import tkinter as tk

from tab_menu import TabMenu


class View:
    def __init__(self, root, model):
        self.root = root
        self.model = model

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.tab_menu = TabMenu(self.main_frame)

        self.tab_menu.tab_main.btn_write.bind("<Button>", self.write)
        self.tab_menu.tab_main.btn_read.bind("<Button>", self.read)

    def write(self, event):
        self.model.write()

    def read(self, event):
        self.model.read()
