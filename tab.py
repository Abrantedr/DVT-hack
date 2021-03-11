import tkinter as tk        # tk.Frame, tk.Button, tk.Label, tk.Entry
from tkinter import ttk     # ttk.Treeview


class MainTab(tk.Frame):    # self -> tk.Frame
    def __init__(self, root, controller, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root
        self.controller = controller

        # Main tab contents
        # NMT State Label
        self.nmt = tk.StringVar()
        self.lbl_NMT_state = tk.Label(self, text="NMT State: ").grid(row=0, column=0, padx=10, pady=10)
        self.lbl_NMT = tk.Label(self, textvariable=self.nmt).grid(row=0, column=1, padx=10, pady=10)

        # "Write" Button
        self.btn_write = tk.Button(self, text="Write", command=lambda: self.controller.write(0x10, 0x1000, 0x20))
        self.btn_write.grid(row=1, column=0, padx=10, pady=10)


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
