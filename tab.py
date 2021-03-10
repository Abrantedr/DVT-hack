import tkinter as tk    # tk.Frame, tk.Button, tk.Label
from tkinter import ttk     # ttk.Treeview


class MainTab(tk.Frame):    # self -> tk.Frame
    def __init__(self, root, controller, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        # Main tab contents
        # "Write" Button
        self.btn_write = tk.Button(self, text="Write", command=controller.write)    # Button calls controller
        self.btn_write.grid(row=0, column=0, ipadx=10, ipady=10)

        # "Read" Button
        self.btn_read = tk.Button(self, text="Read", command=controller.read)
        self.btn_read.grid(row=0, column=1, ipadx=10, ipady=10)


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


class IOTab(tk.Frame):  # self -> tk.Frame
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        # I/O tab contents
        self.lbl_io = tk.Label(self, text="I/O tab")
        self.lbl_io.pack()


class PDOTab(tk.Frame):     # self -> tk.Frame
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root

        # Contents of IOTab below
        self.lbl_pdo = tk.Label(self, text="PDO Tab")
        self.lbl_pdo.pack()
