import os
from jinja2 import Environment, FileSystemLoader

from app.models.report import Report
from app.models.enums import SectionStatus
from app.assets import icons


def render_report(report: Report) -> str:
    """Render a Report object to an HTML string."""
    templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template("report_email.html")

    # Build icons context
    icons_ctx = {
        "green_check": icons.GREEN_CHECK,
        "red_x": icons.RED_X,
        "na_badge": icons.NA_BADGE,
        "white_check": icons.WHITE_CHECK,
        "white_x": icons.WHITE_X,
        "grey_na": icons.GREY_NA,
        "bug_icon": icons.BUG_ICON,
        "dot_green": icons.DOT_GREEN,
        "dot_red": icons.DOT_RED,
        "dot_grey": icons.DOT_GREY,
        "timeline_icon": icons.TIMELINE_ICON,
        "logo": icons.LOGO,
    }

    html = template.render(
        report=report,
        icons=icons_ctx,
        sections=report.sections,
        pmtr_tickets=report.pmtr_tickets,
        header_color=report.header_color,
        overall_status=report.overall_status,
        status_text=report.status_text,
        formatted_date=report.formatted_date,
        qa_shift_left_pct=report.qa_shift_left_pct,
        rda_pct=report.rda_pct,
        performance=report.performance,
        take_history=report.take_history,
        take_location_path=report.take_location_path,
    )

    return html
