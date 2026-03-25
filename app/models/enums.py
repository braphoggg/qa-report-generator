from enum import Enum


class SectionStatus(Enum):
    PASS = "pass"
    FAIL = "fail"
    NA = "na"


class VerdictType(Enum):
    PASS = "Pass"
    FAIL = "Fail"
    NOT_ANALYZED = "Not Analyzed"
    PENDING_ANALYSIS = "Pending Analysis"
    DOA = "DOA"
