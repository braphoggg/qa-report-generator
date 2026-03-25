import tkinter as tk
from tkinter import ttk


class StatusButton(ttk.Frame):
    """Tri-state radio button group: Pass (green), Fail (red), N/A (grey)."""

    COLORS = {
        "pass": "#4CAF50",
        "fail": "#ef5350",
        "na": "#FF9800",
    }

    def __init__(self, parent, label_text: str, **kwargs):
        super().__init__(parent, **kwargs)
        self.status_var = tk.StringVar(value="na")

        label = ttk.Label(self, text=label_text, width=18, anchor="w",
                          font=("Segoe UI", 10))
        label.pack(side=tk.LEFT, padx=(0, 10))

        for value, text, color in [
            ("pass", "Pass", "#4CAF50"),
            ("fail", "Fail", "#ef5350"),
            ("na", "N/A", "#FF9800"),
        ]:
            btn = tk.Radiobutton(
                self,
                text=text,
                variable=self.status_var,
                value=value,
                indicatoron=0,
                width=6,
                font=("Segoe UI", 9),
                bg="#2a2a3e",
                fg="white",
                selectcolor=color,
                activebackground=color,
                activeforeground="white",
                relief="flat",
                bd=1,
                highlightthickness=0,
            )
            btn.pack(side=tk.LEFT, padx=2)

    def get_status(self) -> str:
        return self.status_var.get()

    def set_status(self, value: str):
        self.status_var.set(value)


class ScrollableFrame(ttk.Frame):
    """A scrollable frame container."""

    def __init__(self, parent, height=150, **kwargs):
        super().__init__(parent, **kwargs)

        self.canvas = tk.Canvas(self, height=height, bg="#1e1e2e",
                                highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical",
                                       command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind mouse wheel
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

        # Resize inner frame width with canvas
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
