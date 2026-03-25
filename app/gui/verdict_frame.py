import tkinter as tk
from tkinter import ttk
from datetime import datetime

from app.models.enums import VerdictType


class VerdictFrame(ttk.LabelFrame):
    """Frame for final verdict, cross QA, and analysis datetime."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, text="Final Verdict", padding=10, **kwargs)

        # Row 1: Verdict and Cross QA
        row1 = ttk.Frame(self)
        row1.pack(fill=tk.X, pady=2)

        ttk.Label(row1, text="Verdict:", font=("Segoe UI", 10)).pack(
            side=tk.LEFT, padx=(0, 5))

        self.verdict_var = tk.StringVar(value=VerdictType.PENDING_ANALYSIS.value)
        verdict_values = [v.value for v in VerdictType]
        self.verdict_combo = ttk.Combobox(row1, textvariable=self.verdict_var,
                                          values=verdict_values, width=18,
                                          state="readonly",
                                          font=("Segoe UI", 10))
        self.verdict_combo.pack(side=tk.LEFT, padx=(0, 30))

        ttk.Label(row1, text="Cross QA:", font=("Segoe UI", 10)).pack(
            side=tk.LEFT, padx=(0, 5))
        self.cross_qa_var = tk.StringVar(value="no")
        ttk.Radiobutton(row1, text="Yes", variable=self.cross_qa_var,
                        value="yes").pack(side=tk.LEFT, padx=2)
        ttk.Radiobutton(row1, text="No", variable=self.cross_qa_var,
                        value="no").pack(side=tk.LEFT, padx=2)

        # Row 2: QA Shift-Left % and R&D Automation %
        row2 = ttk.Frame(self)
        row2.pack(fill=tk.X, pady=2)

        ttk.Label(row2, text="QA Shift-Left %:", font=("Segoe UI", 10)).pack(
            side=tk.LEFT, padx=(0, 5))
        self.qa_pct_var = tk.StringVar(value="0")
        ttk.Entry(row2, textvariable=self.qa_pct_var, width=6,
                  font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(0, 20))

        ttk.Label(row2, text="R&D Automation %:", font=("Segoe UI", 10)).pack(
            side=tk.LEFT, padx=(0, 5))
        self.rda_pct_var = tk.StringVar(value="0")
        ttk.Entry(row2, textvariable=self.rda_pct_var, width=6,
                  font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(0, 20))

        ttk.Label(row2, text="Performance:", font=("Segoe UI", 10)).pack(
            side=tk.LEFT, padx=(0, 5))
        self.perf_var = tk.StringVar(value="N/A")
        ttk.Entry(row2, textvariable=self.perf_var, width=8,
                  font=("Segoe UI", 10)).pack(side=tk.LEFT)

        # Row 3: Date and time
        row3 = ttk.Frame(self)
        row3.pack(fill=tk.X, pady=2)

        now = datetime.now()
        ttk.Label(row3, text="Analysis Date:", font=("Segoe UI", 10)).pack(
            side=tk.LEFT, padx=(0, 5))
        self.date_var = tk.StringVar(value=now.strftime("%Y-%m-%d"))
        ttk.Entry(row3, textvariable=self.date_var, width=12,
                  font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(0, 20))

        ttk.Label(row3, text="Time:", font=("Segoe UI", 10)).pack(
            side=tk.LEFT, padx=(0, 5))
        self.time_var = tk.StringVar(value=now.strftime("%H:%M"))
        ttk.Entry(row3, textvariable=self.time_var, width=8,
                  font=("Segoe UI", 10)).pack(side=tk.LEFT)

    def get_verdict(self) -> VerdictType:
        return VerdictType(self.verdict_var.get())

    def get_cross_qa(self) -> bool:
        return self.cross_qa_var.get() == "yes"

    def get_qa_pct(self) -> float:
        try:
            return float(self.qa_pct_var.get())
        except ValueError:
            return 0.0

    def get_rda_pct(self) -> float:
        try:
            return float(self.rda_pct_var.get())
        except ValueError:
            return 0.0

    def get_performance(self) -> str:
        return self.perf_var.get().strip() or "N/A"

    def get_analysis_datetime(self) -> datetime:
        date_str = self.date_var.get().strip()
        time_str = self.time_var.get().strip()
        try:
            return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            return datetime.now()
