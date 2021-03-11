import tkinter as tk        # tk.BOTH
from tkinter import ttk     # ttk.Notebook

# Tab imports
from tab import MainTab, TreeTab, IOTab, PDOTab


def on_tab_selected(event):
    tab = event.widget.tab('current')['text']
    if tab == "Main":
        print("You're in Main")
        # TODO: Trigger Main tab SDO related fields


class TabMenu(ttk.Notebook):    # self -> ttk.Notebook
    def __init__(self, root, controller, **kwargs):
        super().__init__(root, **kwargs)

        # Create tabs
        self.tab_main = MainTab(self, controller)   # Sends controller to main tab
        self.tab_tree = TreeTab(self)
        self.tab_io = IOTab(self)
        self.tab_pdo = PDOTab(self)

        # Add tabs to notebook
        self.add(self.tab_main, text="Main")
        self.add(self.tab_tree, text="Tree")
        self.add(self.tab_io, text="Input / Output")
        self.add(self.tab_pdo, text="TPDO / RPDO")

        # Place the tab menu
        self.pack(fill=tk.BOTH, expand=True)

        # Selecting a tab triggers events
        self.bind('<<NotebookTabChanged>>', on_tab_selected)
