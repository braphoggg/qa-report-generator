import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import tempfile
import os

from app.gui.branch_frame import BranchFrame
from app.gui.sections_frame import SectionsFrame
from app.gui.pmtr_frame import PMTRFrame
from app.gui.verdict_frame import VerdictFrame
from app.gui.recipients_frame import RecipientsFrame
from app.models.report import Report
from app.services.renderer import render_report
from app.services.outlook import display_in_outlook, send_via_outlook
from app.services.history import load_history, save_history_entry


class MainWindow(ttk.Frame):
    """Main application window."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        parent.title("QA Operations Report Generator")
        parent.geometry("780x700")
        parent.minsize(700, 600)

        self._build_ui()

    def _build_ui(self):
        # Main scrollable area
        canvas = tk.Canvas(self.parent, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.parent, orient="vertical",
                                  command=canvas.yview)
        self.main_frame = ttk.Frame(canvas)

        self.main_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas_window = canvas.create_window((0, 0), window=self.main_frame,
                                             anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Resize inner frame width with canvas
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind("<Configure>", on_canvas_configure)

        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind("<Enter>",
                    lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>",
                    lambda e: canvas.unbind_all("<MouseWheel>"))

        pad = {"padx": 10, "pady": 5, "fill": tk.X}

        # Branch & Take
        self.branch_frame = BranchFrame(self.main_frame)
        self.branch_frame.pack(**pad)

        # Section Status
        self.sections_frame = SectionsFrame(self.main_frame)
        self.sections_frame.pack(**pad)

        # PMTR Tickets
        self.pmtr_frame = PMTRFrame(self.main_frame)
        self.pmtr_frame.pack(**pad)

        # Verdict
        self.verdict_frame = VerdictFrame(self.main_frame)
        self.verdict_frame.pack(**pad)

        # Recipients / Email settings
        self.recipients_frame = RecipientsFrame(self.main_frame)
        self.recipients_frame.pack(**pad)

        # Action buttons
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(btn_frame, text="Preview in Browser",
                   command=self._preview).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Open in Outlook",
                   command=self._open_outlook).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Send via Outlook",
                   command=self._send).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update Subject",
                   command=self._update_subject).pack(side=tk.RIGHT, padx=5)

    def _collect_report(self) -> Report:
        """Collect data from all frames into a Report object."""
        verdict = self.verdict_frame.get_verdict()
        branch = self.branch_frame.get_branch()
        take = self.branch_frame.get_take()

        history = load_history()

        return Report(
            branch=branch,
            take=take,
            sections=self.sections_frame.get_sections(),
            pmtr_tickets=self.pmtr_frame.get_tickets(),
            verdict=verdict,
            cross_qa=self.verdict_frame.get_cross_qa(),
            analysis_datetime=self.verdict_frame.get_analysis_datetime(),
            take_history=history,
            qa_shift_left_pct=self.verdict_frame.get_qa_pct(),
            rda_pct=self.verdict_frame.get_rda_pct(),
            performance=self.verdict_frame.get_performance(),
        )

    def _validate(self) -> bool:
        branch = self.branch_frame.get_branch()
        take = self.branch_frame.get_take()
        if not branch:
            messagebox.showwarning("Validation", "Branch is required.")
            return False
        if take <= 0:
            messagebox.showwarning("Validation", "Take must be a positive number.")
            return False
        return True

    def _render_html(self) -> str:
        report = self._collect_report()
        return render_report(report)

    def _preview(self):
        if not self._validate():
            return
        html = self._render_html()
        # Write to temp file and open in browser
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".html", delete=False, encoding="utf-8"
        )
        tmp.write(html)
        tmp.close()
        webbrowser.open(f"file://{tmp.name}")

    def _open_outlook(self):
        if not self._validate():
            return
        html = self._render_html()
        subject = self.recipients_frame.get_subject()
        recipients = self.recipients_frame.get_recipients()

        if not subject:
            self._update_subject()
            subject = self.recipients_frame.get_subject()

        try:
            display_in_outlook(html, subject, recipients)
            self._save_to_history()
        except Exception as e:
            messagebox.showerror("Outlook Error",
                                 f"Could not open Outlook:\n{e}")

    def _send(self):
        if not self._validate():
            return
        recipients = self.recipients_frame.get_recipients()
        if not recipients:
            messagebox.showwarning("Validation",
                                   "Recipients are required to send.")
            return

        if not messagebox.askyesno("Confirm Send",
                                   "Send the report via Outlook now?"):
            return

        html = self._render_html()
        subject = self.recipients_frame.get_subject()

        if not subject:
            self._update_subject()
            subject = self.recipients_frame.get_subject()

        try:
            send_via_outlook(html, subject, recipients)
            self._save_to_history()
            messagebox.showinfo("Success", "Report sent successfully!")
        except Exception as e:
            messagebox.showerror("Outlook Error",
                                 f"Could not send email:\n{e}")

    def _update_subject(self):
        branch = self.branch_frame.get_branch()
        take = self.branch_frame.get_take()
        verdict = self.verdict_frame.get_verdict()
        self.recipients_frame.update_subject(branch, take, verdict.value)

    def _save_to_history(self):
        report = self._collect_report()
        save_history_entry(
            branch=report.branch,
            take=report.take,
            verdict=report.overall_status,
            date=report.analysis_datetime.strftime("%Y-%m-%d"),
        )
