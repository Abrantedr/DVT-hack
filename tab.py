import tkinter as tk  # tk.Frame, tk.Button, tk.Label, tk.Entry
from tkinter import ttk  # ttk.Treeview


class MainTab(tk.Frame):  # self -> tk.Frame
    def __init__(self, root, controller, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root
        self.controller = controller

        # Main tab contents
        # "Set Pre-Operational" Button
        self.btn_pre_operational = tk.Button(self, text="Set Pre-Operational",
                                             command=lambda: self.controller.set_operational_state(0x80, 0x01, 0x2F,
                                                                                                   0x00, 0x28, 0x00,
                                                                                                   0x01))
        self.btn_pre_operational.grid(row=0, column=0, padx=10, pady=10)

        # "Set Operational" Button
        self.btn_operational = tk.Button(self, text="Set Operational",
                                         command=lambda: self.controller.set_operational_state(0x01, 0x01, 0x2F, 0x00,
                                                                                               0x28, 0x00))
        self.btn_operational.grid(row=0, column=1, padx=10, pady=10)

        # "Torque Mode" Button
        self.btn_torque_mode = tk.Button(self, text="Torque Mode", command=lambda: self.controller.write(0x2F, 0x60,
                                                                                                         0x60, 0x00,
                                                                                                         0x04))
        self.btn_torque_mode.grid(row=1, column=0, padx=10, pady=10)

        # "Velocity Mode" Button
        self.btn_velocity_mode = tk.Button(self, text="Velocity Mode", command=lambda: self.controller.write(0x2F, 0x60,
                                                                                                             0x60, 0x00,
                                                                                                             0x03))
        self.btn_velocity_mode.grid(row=1, column=1, padx=10, pady=10)

        # NMT State Label
        self.var_nmt = tk.StringVar()
        self.lbl_nmt_state = tk.Label(self, text="NMT State: ").grid(row=2, column=0, padx=10, pady=10)
        self.lbl_nmt = tk.Label(self, textvariable=self.var_nmt).grid(row=2, column=1, padx=10, pady=10)

        # Operational Mode Label
        self.var_mode = tk.StringVar()
        self.lbl_operational_mode = tk.Label(self, text="Operational Mode: ").grid(row=3, column=0, padx=10, pady=10)
        self.lbl_mode = tk.Label(self, textvariable=self.var_mode).grid(row=3, column=1, padx=10, pady=10)

        # Actual Velocity Label
        self.var_vel = tk.StringVar()
        self.lbl_actual_velocity = tk.Label(self, text="Actual Velocity: "). grid(row=4, column=0, padx=10, pady=10)
        self.lbl_vel = tk.Label(self, textvariable=self.var_vel).grid(row=4, column=1, padx=10, pady=10)
        self.lbl_vel_units = tk.Label(self, text="RPM").grid(row=4, column=2, padx=10, pady=10)

        # Actual Motor Current Label
        self.var_current = tk.StringVar()
        self.lbl_actual_current = tk.Label(self, text="Actual Motor Current: ").grid(row=5, column=0, padx=10, pady=10)
        self.lbl_current = tk.Label(self, textvariable=self.var_current).grid(row=5, column=1, padx=10, pady=10)
        self.lbl_current_units = tk.Label(self, text="A (RMS)").grid(row=5, column=2, padx=10, pady=10)


class TreeTab(tk.Frame):  # self -> tk.Frame
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


class PDOTab(tk.Frame):  # self -> tk.Frame
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root

        # Contents of IOTab below
        self.lbl_pdo = tk.Label(self, text="PDO Tab")
        self.lbl_pdo.pack()
