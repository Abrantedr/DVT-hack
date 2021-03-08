import tkinter as tk
from tkinter import ttk


class TreeTab(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root

        # Contents of TreeTab below
        # Tree view
        self.trv_tree = ttk.Treeview(self)
        self.elm_motor = self.trv_tree.insert("", tk.END, text="Motor")
        elm_nameplate = self.trv_tree.insert(self.elm_motor, tk.END, text="Name Plate")
        self.trv_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.frm_data = ttk.Frame(self)
        self.frm_data.pack(side=tk.RIGHT, expand=1, fill=tk.BOTH)

        self.lbl_tree = tk.Label(self.frm_data, text="Tree Tab")
        self.lbl_tree.pack()
