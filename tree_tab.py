import tkinter as tk        # tk.Frame, tk.Label
from tkinter import ttk     # ttk.Treeview


class TreeTab(tk.Frame):    # self -> tk.Frame
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        # Tree tab contents
        # Tree view
        self.trv_tree = ttk.Treeview(self)
        self.elm_motor = self.trv_tree.insert("", tk.END, text="Motor")
        elm_nameplate = self.trv_tree.insert(self.elm_motor, tk.END, text="Name Plate")
        self.trv_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right frame
        self.frm_data = ttk.Frame(self)
        self.frm_data.pack(side=tk.RIGHT, expand=1, fill=tk.BOTH)

        # Right frame label
        self.lbl_tree = tk.Label(self.frm_data, text="Tree Tab")
        self.lbl_tree.pack()
