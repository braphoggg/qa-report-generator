from dataclasses import dataclass, field
from datetime import datetime

from app.models.enums import SectionStatus, VerdictType
from app.models.pmtr import PMTRTicket


@dataclass
class TakeHistoryEntry:
    branch: str
    take: int
    verdict: str  # "pass", "fail", "doa"
    date: str


@dataclass
class Report:
    branch: str
    take: int
    sections: dict  # {section_name: SectionStatus}
    pmtr_tickets: list
    verdict: VerdictType
    cross_qa: bool
    analysis_datetime: datetime = field(default_factory=datetime.now)
    take_history: list = field(default_factory=list)
    qa_shift_left_pct: float = 0.0
    rda_pct: float = 0.0
    performance: str = "N/A"

    @property
    def overall_status(self) -> str:
        if self.verdict == VerdictType.PASS:
            return "pass"
        elif self.verdict in (VerdictType.FAIL, VerdictType.DOA):
            return "fail"
        else:
            return "na"

    @property
    def header_color(self) -> str:
        status = self.overall_status
        if status == "pass":
            return "#4CAF50"
        elif status == "fail":
            return "#ef5350"
        else:
            return "#9e9e9e"

    @property
    def status_text(self) -> str:
        if self.verdict == VerdictType.PASS:
            return "Approved for cross QA" if self.cross_qa else "Pass"
        elif self.verdict == VerdictType.FAIL:
            return "FAIL"
        elif self.verdict == VerdictType.DOA:
            return "DOA"
        elif self.verdict == VerdictType.PENDING_ANALYSIS:
            return "Pending Analysis"
        else:
            return "N/A"

    @property
    def take_location_path(self) -> str:
        return f"\\\\galaxy\\ckp\\image\\CPsuite-{self.branch}\\take_{self.take}"

    @property
    def formatted_date(self) -> str:
        day = self.analysis_datetime.day
        suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        return self.analysis_datetime.strftime(f"%b {day}{suffix}, %Y")
