"""Outlook email integration with multiple fallback methods."""

import os
import tempfile
import subprocess


def _try_com_dispatch(html_body: str, subject: str, recipients: str, send: bool):
    """Try classic COM automation (works with desktop Office/Outlook)."""
    import win32com.client
    outlook = win32com.client.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)  # olMailItem
    if recipients:
        mail.To = recipients
    mail.Subject = subject
    mail.HTMLBody = html_body
    if send:
        mail.Send()
    else:
        mail.Display()


def _try_com_ensure_dispatch(html_body: str, subject: str, recipients: str, send: bool):
    """Try EnsureDispatch (regenerates COM cache, fixes some registration issues)."""
    import win32com.client
    outlook = win32com.client.gencache.EnsureDispatch("Outlook.Application")
    mail = outlook.CreateItem(0)
    if recipients:
        mail.To = recipients
    mail.Subject = subject
    mail.HTMLBody = html_body
    if send:
        mail.Send()
    else:
        mail.Display()


def _try_outlook_exe(html_body: str, subject: str, recipients: str):
    """Launch Outlook via command line with an .eml file as fallback."""
    # Save HTML to a temporary .htm file, then create an .eml wrapping it
    eml_content = _build_eml(html_body, subject, recipients)

    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".eml", delete=False, encoding="utf-8",
        dir=tempfile.gettempdir()
    )
    tmp.write(eml_content)
    tmp.close()

    # os.startfile opens .eml with the default mail client
    os.startfile(tmp.name)


def _build_eml(html_body: str, subject: str, recipients: str) -> str:
    """Build a minimal .eml (RFC 2822) file with HTML body."""
    import email.mime.text
    import email.utils
    from datetime import datetime

    msg = email.mime.text.MIMEText(html_body, "html", "utf-8")
    msg["Subject"] = subject
    msg["Date"] = email.utils.formatdate(localtime=True)
    if recipients:
        msg["To"] = recipients
    msg["X-Unsent"] = "1"  # Tells Outlook to open as draft for editing
    return msg.as_string()


def display_in_outlook(html_body: str, subject: str, recipients: str = ""):
    """Open the report in Outlook for user review before sending.

    Tries COM automation first, falls back to opening an .eml file.
    """
    errors = []

    # Method 1: Classic COM Dispatch
    try:
        _try_com_dispatch(html_body, subject, recipients, send=False)
        return
    except Exception as e:
        errors.append(f"COM Dispatch: {e}")

    # Method 2: EnsureDispatch (regenerates cache)
    try:
        _try_com_ensure_dispatch(html_body, subject, recipients, send=False)
        return
    except Exception as e:
        errors.append(f"COM EnsureDispatch: {e}")

    # Method 3: Open .eml file (works with any Outlook version including New Outlook)
    try:
        _try_outlook_exe(html_body, subject, recipients)
        return
    except Exception as e:
        errors.append(f"EML fallback: {e}")

    raise RuntimeError(
        "All Outlook methods failed:\n" + "\n".join(f"  - {e}" for e in errors)
    )


def send_via_outlook(html_body: str, subject: str, recipients: str):
    """Send the report immediately via Outlook."""
    errors = []

    try:
        _try_com_dispatch(html_body, subject, recipients, send=True)
        return
    except Exception as e:
        errors.append(f"COM Dispatch: {e}")

    try:
        _try_com_ensure_dispatch(html_body, subject, recipients, send=True)
        return
    except Exception as e:
        errors.append(f"COM EnsureDispatch: {e}")

    # For send, fall back to opening as draft — user can hit Send manually
    try:
        _try_outlook_exe(html_body, subject, recipients)
        raise RuntimeError(
            "COM automation unavailable. Report opened as draft in Outlook — "
            "please review and send manually."
        )
    except RuntimeError:
        raise
    except Exception as e:
        errors.append(f"EML fallback: {e}")

    raise RuntimeError(
        "All Outlook methods failed:\n" + "\n".join(f"  - {e}" for e in errors)
    )
