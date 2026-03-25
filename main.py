"""QA Operations Report Generator - Entry Point."""

import sys
import os
import tkinter as tk
from tkinter import ttk

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    # Enable DPI awareness on Windows for crisp rendering
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    root = tk.Tk()
    root.title("QA Operations Report Generator")

    # Apply a dark-ish theme to the GUI
    style = ttk.Style()
    available_themes = style.theme_names()
    if "clam" in available_themes:
        style.theme_use("clam")

    # Configure dark colors
    style.configure(".", background="#2b2b3d", foreground="#e0e0e0",
                     fieldbackground="#1e1e2e", font=("Segoe UI", 10))
    style.configure("TLabelframe", background="#2b2b3d", foreground="#00bcd4")
    style.configure("TLabelframe.Label", background="#2b2b3d",
                     foreground="#00bcd4", font=("Segoe UI", 11, "bold"))
    style.configure("TButton", background="#37474f", foreground="#e0e0e0",
                     padding=6)
    style.map("TButton",
              background=[("active", "#455a64")],
              foreground=[("active", "#ffffff")])
    style.configure("TEntry", fieldbackground="#1e1e2e", foreground="#e0e0e0")
    style.configure("TCombobox", fieldbackground="#1e1e2e", foreground="#e0e0e0")
    style.configure("TCheckbutton", background="#2b2b3d", foreground="#e0e0e0")
    style.configure("TRadiobutton", background="#2b2b3d", foreground="#e0e0e0")

    root.configure(bg="#2b2b3d")

    from app.gui.main_window import MainWindow
    app = MainWindow(root)

    # Center window on screen
    root.update_idletasks()
    width = 780
    height = 720
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    root.mainloop()


if __name__ == "__main__":
    main()
