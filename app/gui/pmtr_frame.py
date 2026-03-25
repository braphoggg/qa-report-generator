import tkinter as tk
from tkinter import ttk

from app.gui.widgets import ScrollableFrame
from app.gui.sections_frame import SECTION_NAMES
from app.models.pmtr import PMTRTicket


class PMTRRow(ttk.Frame):
    """A single PMTR ticket row."""

    def __init__(self, parent, on_remove, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_remove = on_remove

        self.ticket_var = tk.StringVar()
        self.section_var = tk.StringVar(value=SECTION_NAMES[0])
        self.desc_var = tk.StringVar()
        self.age_var = tk.StringVar(value="0")
        self.blocking_var = tk.BooleanVar(value=False)

        ttk.Entry(self, textvariable=self.ticket_var, width=14,
                  font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=2)

        section_combo = ttk.Combobox(self, textvariable=self.section_var,
                                     values=SECTION_NAMES, width=14,
                                     state="readonly", font=("Segoe UI", 9))
        section_combo.pack(side=tk.LEFT, padx=2)

        ttk.Entry(self, textvariable=self.desc_var, width=30,
                  font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=2)

        ttk.Label(self, text="Age:", font=("Segoe UI", 9)).pack(
            side=tk.LEFT, padx=(4, 0))
        ttk.Entry(self, textvariable=self.age_var, width=4,
                  font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=2)

        ttk.Checkbutton(self, text="Blocking", variable=self.blocking_var
                        ).pack(side=tk.LEFT, padx=4)

        ttk.Button(self, text="X", width=3,
                   command=self._remove).pack(side=tk.LEFT, padx=2)

    def _remove(self):
        self.on_remove(self)
        self.destroy()

    def get_ticket(self) -> PMTRTicket:
        age = 0
        try:
            age = int(self.age_var.get())
        except ValueError:
            pass

        return PMTRTicket(
            ticket_id=self.ticket_var.get().strip(),
            section=self.section_var.get(),
            description=self.desc_var.get().strip(),
            age_days=age,
            blocking_cross_qa=self.blocking_var.get(),
        )


class PMTRFrame(ttk.LabelFrame):
    """Frame for managing PMTR tickets."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, text="PMTR Tickets", padding=10, **kwargs)

        # Header row
        header = ttk.Frame(self)
        header.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(header, text="ID", width=14, font=("Segoe UI", 9, "bold")
                  ).pack(side=tk.LEFT, padx=2)
        ttk.Label(header, text="Section", width=14, font=("Segoe UI", 9, "bold")
                  ).pack(side=tk.LEFT, padx=2)
        ttk.Label(header, text="Description", width=30, font=("Segoe UI", 9, "bold")
                  ).pack(side=tk.LEFT, padx=2)
        ttk.Label(header, text="Age", width=6, font=("Segoe UI", 9, "bold")
                  ).pack(side=tk.LEFT, padx=2)

        self.scroll_frame = ScrollableFrame(self, height=120)
        self.scroll_frame.pack(fill=tk.BOTH, expand=True)

        self.rows: list[PMTRRow] = []

        # Add button
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=(5, 0))
        ttk.Button(btn_frame, text="+ Add PMTR",
                   command=self.add_row).pack(side=tk.LEFT)

    def add_row(self):
        row = PMTRRow(self.scroll_frame.scrollable_frame,
                      on_remove=self._remove_row)
        row.pack(fill=tk.X, pady=1)
        self.rows.append(row)

    def _remove_row(self, row: PMTRRow):
        if row in self.rows:
            self.rows.remove(row)

    def get_tickets(self) -> list:
        tickets = []
        for row in self.rows:
            ticket = row.get_ticket()
            if ticket.ticket_id:  # skip empty rows
                tickets.append(ticket)
        return tickets
