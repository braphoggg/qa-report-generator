# QA Operations Report Generator

A Python desktop application for generating, previewing, and sending QA Operations Reports as formatted HTML emails via Microsoft Outlook. Built for release qualification workflows.

---

## Features

- **Tri-state section tracking** — Mark Deployment, Functionality, Stability, and R&D Automation as Pass, Fail, or N/A
- **PMTR ticket management** — Add bug tickets with section mapping, age tracking, and cross-QA blocking flags
- **Multiple verdict types** — Pass, Fail, DOA, Pending Analysis, Not Analyzed
- **Cross QA approval** — Flag reports as approved or blocked for cross-team QA
- **Performance metrics** — Track QA Shift-Left %, R&D Automation %, and Performance status
- **Take history timeline** — Visual dot timeline of previous take verdicts
- **Outlook integration** — Preview in browser, open as Outlook draft, or send directly
- **Auto-generated subject lines** — Format: `QA Operations Report _ {version} {branch} T{take} - {verdict}`
- **Network path linking** — Auto-generates take location paths
- **Dark-themed UI** — Modern interface with intuitive controls
- **History persistence** — Stores take verdicts in JSON for timeline tracking across sessions
- **Report deduplication** — Re-generating a report for an existing take overrides the previous entry

---

## Screenshots

### Generated Report (Pass)
Color-coded HTML email with green header, section statuses, metrics summary, bug list, and take status timeline.

### Generated Report (Fail)
Red header with blocking PMTR tickets, QA Shift-Left and R&D Automation pass rates.

### Generated Report (Pending Analysis)
Grey header with all sections set to N/A, pending completion message.

---

## Installation

### Prerequisites

- **Python 3.9+**
- **Microsoft Outlook** (desktop version) for email integration
- **Windows OS** (required for Outlook COM automation)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/qa-report-generator.git
   cd qa-report-generator
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `jinja2` | >= 3.1.0 | HTML email template rendering |
| `pywin32` | >= 306 | Outlook COM automation |
| `tkcalendar` | >= 1.6.1 | Date picker widget |
| `Pillow` | >= 9.0 | Icon generation (PNG) |
| `svg.path` | >= 6.0 | SVG path parsing for logo |

> **Note:** `tkinter` is bundled with standard Python installations on Windows.

---

## Usage

### Launch the Application

```bash
python main.py
```

### Creating a Report

1. **Set Branch & Take** — Enter the branch name (e.g., `joy_main`) and take number (e.g., `192`)

2. **Set Section Statuses** — Click Pass (green), Fail (red), or N/A (orange) for each section:
   - Deployment
   - Functionality
   - Stability
   - R&D Automation

3. **Add PMTR Tickets** (optional) — Click "Add PMTR" and fill in:
   - Ticket ID (e.g., `PMTR-125079`)
   - Section (dropdown)
   - Description
   - Age in days
   - Blocking Cross QA checkbox

4. **Set Verdict** — Choose from:
   - **Pass** — All tests passed, approved for cross QA
   - **Fail** — Blocking issues found
   - **DOA** — Dead on arrival, cannot proceed
   - **Pending Analysis** — Analysis not yet complete
   - **Not Analyzed** — Skipped

5. **Configure Metrics** — Enter QA Shift-Left %, R&D Automation %, and Performance status

6. **Set Cross QA** — Yes if approved, No if blocked

7. **Set Analysis Date/Time** — Defaults to current date and time

8. **Email Settings** — Enter recipients (comma-separated) and review the auto-generated subject line

### Sending the Report

| Button | Action |
|--------|--------|
| **Preview in Browser** | Renders HTML and opens in your default browser for review |
| **Open in Outlook** | Creates an Outlook draft email — review before sending manually |
| **Send via Outlook** | Sends the report immediately to all recipients |
| **Update Subject** | Regenerates the subject line from current branch/take/verdict |

---

## Project Structure

```
ops_report_gen/
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── README.md
├── app/
│   ├── gui/
│   │   ├── main_window.py           # Main window with layout and actions
│   │   ├── branch_frame.py          # Branch & take input
│   │   ├── sections_frame.py        # Section status buttons
│   │   ├── pmtr_frame.py            # PMTR ticket management table
│   │   ├── verdict_frame.py         # Verdict, metrics, date/time
│   │   ├── recipients_frame.py      # Email recipients & subject
│   │   └── widgets.py               # Custom widgets (StatusButton, ScrollableFrame)
│   ├── models/
│   │   ├── report.py                # Report dataclass with computed properties
│   │   ├── enums.py                 # SectionStatus, VerdictType enums
│   │   └── pmtr.py                  # PMTRTicket dataclass
│   ├── services/
│   │   ├── renderer.py              # Jinja2 HTML report rendering
│   │   ├── outlook.py               # Outlook COM automation (3-layer fallback)
│   │   └── history.py               # Take history JSON persistence
│   ├── assets/
│   │   └── icons.py                 # Base64-encoded PNG icon generation
│   └── templates/
│       └── report_email.html        # Jinja2 HTML email template
└── data/
    ├── history.json                 # Persisted take history
    └── *.svg / *.png                # Logo source files
```

---

## Architecture

```
User Input (GUI Frames)
        │
        ▼
MainWindow._collect_report()  →  Report (dataclass)
        │
        ▼
renderer.render_report()  →  HTML string (Jinja2 template)
        │
        ├──► Preview in Browser (temp file)
        ├──► outlook.display_in_outlook() → Outlook draft
        └──► outlook.send_via_outlook() → Send immediately
                │
                ▼
        history.save_history_entry() → data/history.json
```

### Outlook Fallback Chain

The application handles different Outlook configurations with a 3-layer fallback:

1. **COM Dispatch** — Standard `win32com.client.Dispatch("Outlook.Application")`
2. **COM EnsureDispatch** — Regenerates COM cache for corrupted registrations
3. **EML File** — Generates RFC 2822 `.eml` file and opens with system mail client (supports New Outlook)

---

## Report Format

Generated reports are HTML emails optimized for Outlook's Word-based rendering engine:

- **All inline CSS** — No external stylesheets or `<style>` blocks
- **Table-based layout** — Maximum compatibility across email clients
- **PNG icons** — All icons are base64-encoded PNGs (SVG is not supported in Outlook)
- **Dark theme** — Background `#1a1a2e`, cards `#16213e`, text `#e0e0e0`

### Report Sections

| Section | Description |
|---------|-------------|
| **Header** | "QA OPERATIONS REPORT" title with the company logo |
| **Status Bar** | Color-coded banner (green/red/grey) with verdict, branch, take, and date |
| **Section Grid** | Pass/Fail/N/A icons for each of the 4 test sections |
| **Metrics** | QA Shift-Left %, R&D Automation %, Performance |
| **Bugs** | PMTR ticket list with section tags, age, blocking flags, and descriptions |
| **Timeline** | Visual dot timeline of historical take verdicts |
| **Footer** | Links to R82.20 Dashboard (Jira) and Take Location (network path) |

---

## History & Timeline

Take verdicts are persisted to `data/history.json`. Each entry records:

```json
{
  "branch": "joy_main",
  "take": 192,
  "verdict": "pass",
  "date": "2026-03-25"
}
```

The **Take Status Timeline** renders these as colored dots:
- Green = Pass
- Red = Fail
- Grey = DOA

Re-generating a report for an existing branch + take combination will override the previous entry.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Could not open Outlook: Invalid class string` | You may have "New Outlook" or Microsoft Store Office. The app will fall back to `.eml` file method automatically. |
| Icons appear broken in email | Ensure `Pillow` is installed. The app generates PNG icons at runtime. |
| `tkinter` not found | Reinstall Python with the "tcl/tk" option enabled. |
| Take history not updating | Check write permissions on `data/history.json`. |
| Subject line not updating | Click "Update Subject" after changing branch, take, or verdict. |

---

## License

This project is proprietary and intended for internal QA operations use.
