import tkinter as tk
from tkinter import ttk

from app.gui.widgets import StatusButton
from app.models.enums import SectionStatus


SECTION_NAMES = ["Deployment", "Functionality", "Stability", "R&D Automation"]


class SectionsFrame(ttk.LabelFrame):
    """Frame for section status selection."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, text="Section Status", padding=10, **kwargs)

        self.status_buttons: dict[str, StatusButton] = {}

        for name in SECTION_NAMES:
            btn = StatusButton(self, label_text=name)
            btn.pack(fill=tk.X, pady=2)
            self.status_buttons[name] = btn

    def get_sections(self) -> dict:
        result = {}
        for name, btn in self.status_buttons.items():
            status_str = btn.get_status()
            result[name] = SectionStatus(status_str)
        return result

    def set_all_na(self):
        for btn in self.status_buttons.values():
            btn.set_status("na")
