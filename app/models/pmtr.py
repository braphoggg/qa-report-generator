from dataclasses import dataclass


@dataclass
class PMTRTicket:
    ticket_id: str
    section: str
    description: str = ""
    age_days: int = 0
    blocking_cross_qa: bool = False
