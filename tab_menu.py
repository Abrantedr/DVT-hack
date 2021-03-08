import tkinter as tk
from tkinter import ttk

from main_tab import MainTab
from tree_tab import TreeTab


class TabMenu(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root

        # Create notebook
        self.tab_menu = ttk.Notebook(self.root)

        # Create tabs
        self.tab_main = MainTab(self.tab_menu)
        self.tab_tree = TreeTab(self.tab_menu)
        self.tab_io = ttk.Frame(self.tab_menu)
        self.tab_pdo = ttk.Frame(self.tab_menu)

        # Add tabs to notebook
        self.tab_menu.add(self.tab_main, text="Main")
        self.tab_menu.add(self.tab_tree, text="Tree")
        self.tab_menu.add(self.tab_io, text="Input / Output")
        self.tab_menu.add(self.tab_pdo, text="TPDO / RPDO")

        # Place the tab menu
        self.tab_menu.pack(fill=tk.BOTH, expand=True)

        # "TPDO / RPDO" tab contents
        self.lbl_pdo = tk.Label(self.tab_pdo, text="PDO Tab")
        self.lbl_pdo.pack()
