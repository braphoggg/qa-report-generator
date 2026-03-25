import tkinter as tk
from tkinter import ttk


class RecipientsFrame(ttk.LabelFrame):
    """Frame for email recipients and subject."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, text="Email Settings", padding=10, **kwargs)

        # To field
        row1 = ttk.Frame(self)
        row1.pack(fill=tk.X, pady=2)
        ttk.Label(row1, text="To:", font=("Segoe UI", 10), width=8).pack(
            side=tk.LEFT, padx=(0, 5))
        self.to_var = tk.StringVar()
        ttk.Entry(row1, textvariable=self.to_var,
                  font=("Segoe UI", 10)).pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Subject field
        row2 = ttk.Frame(self)
        row2.pack(fill=tk.X, pady=2)
        ttk.Label(row2, text="Subject:", font=("Segoe UI", 10), width=8).pack(
            side=tk.LEFT, padx=(0, 5))
        self.subject_var = tk.StringVar()
        ttk.Entry(row2, textvariable=self.subject_var,
                  font=("Segoe UI", 10)).pack(side=tk.LEFT, fill=tk.X, expand=True)

    def update_subject(self, branch: str, take: int, verdict: str):
        self.subject_var.set(
            f"QA Operations Report _ R82.20 {branch} T{take} - {verdict}"
        )

    def get_recipients(self) -> str:
        return self.to_var.get().strip()

    def get_subject(self) -> str:
        return self.subject_var.get().strip()
