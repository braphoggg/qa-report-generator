import tkinter as tk
from tkinter import ttk


class BranchFrame(ttk.LabelFrame):
    """Frame for Branch and Take inputs."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, text="Branch & Take", padding=10, **kwargs)

        row = ttk.Frame(self)
        row.pack(fill=tk.X)

        ttk.Label(row, text="Branch:", font=("Segoe UI", 10)).pack(
            side=tk.LEFT, padx=(0, 5))
        self.branch_var = tk.StringVar(value="joy_main")
        self.branch_entry = ttk.Entry(row, textvariable=self.branch_var,
                                      width=20, font=("Segoe UI", 10))
        self.branch_entry.pack(side=tk.LEFT, padx=(0, 20))

        ttk.Label(row, text="Take:", font=("Segoe UI", 10)).pack(
            side=tk.LEFT, padx=(0, 5))
        self.take_var = tk.StringVar()
        self.take_entry = ttk.Entry(row, textvariable=self.take_var,
                                    width=8, font=("Segoe UI", 10))
        self.take_entry.pack(side=tk.LEFT)

        # Validate take is numeric
        vcmd = (self.register(self._validate_take), "%P")
        self.take_entry.configure(validate="key", validatecommand=vcmd)

    def _validate_take(self, value: str) -> bool:
        if value == "":
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False

    def get_branch(self) -> str:
        return self.branch_var.get().strip()

    def get_take(self) -> int:
        val = self.take_var.get().strip()
        return int(val) if val else 0
