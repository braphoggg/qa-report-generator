"""Generate all report icons as base64-encoded PNGs for Outlook compatibility.

Outlook uses Word's HTML renderer which does NOT support:
- SVG images
- data:image/svg+xml URIs
So all icons must be PNG with data:image/png;base64,... URIs.
"""

import base64
import io
import math
from PIL import Image, ImageDraw, ImageFont
from svg.path import parse_path


def _img_to_data_uri(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def _get_font(size: int):
    """Try to load a good font, fall back to default."""
    font_names = [
        "arialbd.ttf", "arial.ttf", "segoeui.ttf", "segoeuib.ttf",
        "calibrib.ttf", "verdanab.ttf",
    ]
    for name in font_names:
        try:
            return ImageFont.truetype(name, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def _draw_check(draw, cx, cy, r, color, width=2):
    """Draw a checkmark centered at (cx, cy) fitting within radius r."""
    # Checkmark points relative to center
    s = r * 0.55
    points = [
        (cx - s * 0.7, cy + s * 0.05),
        (cx - s * 0.1, cy + s * 0.55),
        (cx + s * 0.75, cy - s * 0.5),
    ]
    draw.line(points, fill=color, width=width, joint="curve")


def _draw_x(draw, cx, cy, r, color, width=2):
    """Draw an X centered at (cx, cy) fitting within radius r."""
    s = r * 0.35
    draw.line([(cx - s, cy - s), (cx + s, cy + s)], fill=color, width=width)
    draw.line([(cx + s, cy - s), (cx - s, cy + s)], fill=color, width=width)


def _make_circle_icon(size, bg_color, symbol, symbol_color="white"):
    """Create a circle icon with a symbol (check, x, or text)."""
    scale = 4  # supersampling for anti-aliasing
    s = size * scale
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    margin = s // 10
    draw.ellipse([margin, margin, s - margin, s - margin], fill=bg_color)

    cx, cy = s // 2, s // 2
    r = (s - 2 * margin) // 2

    if symbol == "check":
        _draw_check(draw, cx, cy, r, symbol_color, width=max(2, s // 12))
    elif symbol == "x":
        _draw_x(draw, cx, cy, r, symbol_color, width=max(2, s // 12))
    elif symbol == "na":
        font = _get_font(s // 3)
        bbox = draw.textbbox((0, 0), "N/A", font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((cx - tw // 2, cy - th // 2 - bbox[1]), "N/A",
                  fill=symbol_color, font=font)

    return img.resize((size, size), Image.LANCZOS)


def _make_na_badge(size):
    """Create an orange rounded-rect N/A badge."""
    scale = 4
    s = size * scale
    w, h = int(s * 1.0), int(s * 0.7)
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    y_off = (s - h) // 2
    radius = h // 3
    draw.rounded_rectangle([s // 10, y_off, s - s // 10, y_off + h],
                           radius=radius, fill="#FF9800")

    font = _get_font(h // 2)
    bbox = draw.textbbox((0, 0), "N/A", font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((s // 2 - tw // 2, y_off + h // 2 - th // 2 - bbox[1]),
              "N/A", fill="white", font=font)

    return img.resize((size, size), Image.LANCZOS)


def _make_header_icon(size, symbol):
    """Create a semi-transparent white icon for the colored header bar."""
    scale = 4
    s = size * scale
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = s // 2, s // 2
    margin = s // 8

    # Outer glow circle
    draw.ellipse([margin, margin, s - margin, s - margin],
                 fill=(255, 255, 255, 70))
    # Inner circle
    inner_m = s // 5
    draw.ellipse([inner_m, inner_m, s - inner_m, s - inner_m],
                 fill=(255, 255, 255, 120))

    r = (s - 2 * margin) // 2

    if symbol == "check":
        _draw_check(draw, cx, cy, r, "white", width=max(3, s // 10))
    elif symbol == "x":
        _draw_x(draw, cx, cy, r, "white", width=max(3, s // 10))
    elif symbol == "na":
        font = _get_font(s // 4)
        bbox = draw.textbbox((0, 0), "N/A", font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((cx - tw // 2, cy - th // 2 - bbox[1]),
                  "N/A", fill="white", font=font)

    return img.resize((size, size), Image.LANCZOS)


def _make_dot(size, color):
    """Create a small colored dot for the timeline."""
    scale = 4
    s = size * scale
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    margin = s // 6
    draw.ellipse([margin, margin, s - margin, s - margin], fill=color)
    return img.resize((size, size), Image.LANCZOS)


def _make_bug_icon(size):
    """Create a bug icon (orange circle with bug symbol)."""
    scale = 4
    s = size * scale
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    margin = s // 10
    draw.ellipse([margin, margin, s - margin, s - margin], fill="#FF6D00")

    # Draw a simple bug shape
    cx, cy = s // 2, s // 2
    r = (s - 2 * margin) // 2
    bug_r = int(r * 0.35)

    # Bug body (two ovals)
    draw.ellipse([cx - bug_r, cy - int(bug_r * 0.3), cx + bug_r, cy + int(bug_r * 1.2)],
                 fill="white")
    draw.ellipse([cx - int(bug_r * 0.7), cy - int(bug_r * 1.0),
                  cx + int(bug_r * 0.7), cy + int(bug_r * 0.15)],
                 fill="white")

    # Antennae
    lw = max(2, s // 30)
    draw.line([(cx - int(bug_r * 0.3), cy - int(bug_r * 0.9)),
               (cx - int(bug_r * 0.7), cy - int(bug_r * 1.4))],
              fill="white", width=lw)
    draw.line([(cx + int(bug_r * 0.3), cy - int(bug_r * 0.9)),
               (cx + int(bug_r * 0.7), cy - int(bug_r * 1.4))],
              fill="white", width=lw)

    # Legs
    for side in [-1, 1]:
        for yoff in [-0.1, 0.3, 0.7]:
            draw.line([(cx + side * bug_r, cy + int(bug_r * yoff)),
                       (cx + side * int(bug_r * 1.5), cy + int(bug_r * (yoff - 0.15)))],
                      fill="white", width=lw)

    return img.resize((size, size), Image.LANCZOS)


def _make_timeline_icon(size):
    """Create a timeline/clipboard icon (yellow circle with lines)."""
    scale = 4
    s = size * scale
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    margin = s // 10
    draw.ellipse([margin, margin, s - margin, s - margin], fill="#FFC107")

    # Clipboard rectangle
    cx, cy = s // 2, s // 2
    rw, rh = int(s * 0.22), int(s * 0.28)
    draw.rounded_rectangle([cx - rw, cy - rh, cx + rw, cy + rh],
                           radius=s // 20, fill="white")

    # Lines on clipboard
    lw = max(2, s // 30)
    line_color = "#666666"
    for yoff in [-0.12, -0.02, 0.08, 0.18]:
        y = cy + int(s * yoff)
        x_extent = rw * 0.7 if yoff == 0.18 else rw * 0.85
        draw.line([(cx - int(x_extent), y), (cx + int(x_extent), y)],
                  fill=line_color, width=lw)

    return img.resize((size, size), Image.LANCZOS)


def _svg_path_to_points(d: str, num_samples: int = 1000) -> list:
    """Parse an SVG path string and sample points along it."""
    path = parse_path(d)
    points = []
    for i in range(num_samples + 1):
        t = i / num_samples
        try:
            pt = path.point(t)
            points.append((pt.real, pt.imag))
        except Exception:
            pass
    return points


def _make_checkpoint_logo(size):
    """Render the official Check Point 2024 logo icon from its SVG path data.

    Source: Wikimedia Commons Check-Point-2024-logo-color.svg (icon extracted)
    """
    # Official SVG paths from the Check Point 2024 logo (viewBox 0 0 52 52)
    dot_d = ("m 50.9,12.46 c -2.7,3.3 -7.5,3.8 -10.8,1.2 "
             "-3.3,-2.7 -3.8,-7.5 -1.2,-10.8 2.7,-3.3 7.5,-3.8 "
             "10.8,-1.2 3.3,2.7 3.8,7.5 1.2,10.8 z")
    swoosh_d = (
        "m 40.5,24.46 c -2.1,1 -4.7,1 -6.9,-0.3 l -6,8 "
        "c 0.8,0.9 1.2,2 1.2,3.1 0,1 -0.2,2 -0.8,2.9 "
        "-1.5,2.3 -4.7,3 -7,1.5 -0.2,-0.2 -0.5,-0.3 -0.7,-0.5 "
        "0,0 -0.1,-0.1 -0.2,-0.2 -0.1,-0.1 -0.3,-0.3 -0.4,-0.5 "
        "0,0 -0.1,-0.1 -0.2,-0.2 -0.1,-0.2 -0.3,-0.4 -0.4,-0.7 "
        "0,0 0,-0.1 0,-0.2 0,-0.2 -0.2,-0.4 -0.2,-0.6 "
        "0,0 0,-0.1 0,-0.2 0,-0.2 0,-0.5 -0.1,-0.7 "
        "0,0 0,-0.1 0,-0.2 0,-0.2 0,-0.5 0,-0.7 "
        "0,0 0,0 0,-0.1 0,-0.3 0,-0.5 0.2,-0.8 "
        "0,0 0,-0.1 0,-0.2 0,-0.3 0.2,-0.5 0.3,-0.8 "
        "l -4.9,-3.7 -1.5,2 -5.6,-4.2 4.2,-5.6 5.6,4.2 -1.5,2 "
        "4.9,3.7 c 1.5,-1.3 3.7,-1.6 5.6,-0.6 l 6,-8 "
        "c -2.4,-2.4 -3,-6.1 -1.2,-9.2 0.3,-0.6 0.8,-1.1 1.2,-1.6 "
        "C 28.8,9.86 24.9,8.56 20.6,8.46 9.3,8.46 0.1,17.56 "
        "0,28.96 0,40.26 9.1,49.46 20.5,49.56 31.8,49.56 41,40.46 "
        "41.1,29.06 c 0,-1.7 -0.2,-3.3 -0.6,-4.8 z"
    )

    scale = 8  # high resolution for quality
    s = 52 * scale
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    def scale_pts(pts):
        return [(x * scale, y * scale) for x, y in pts]

    swoosh_pts = _svg_path_to_points(swoosh_d, 2000)
    dot_pts = _svg_path_to_points(dot_d, 200)

    draw.polygon(scale_pts(swoosh_pts), fill="#ee0c5d")
    draw.polygon(scale_pts(dot_pts), fill="white")

    return img.resize((size, size), Image.LANCZOS)


# Generate all icons as PNG data URIs
GREEN_CHECK = _img_to_data_uri(_make_circle_icon(32, "#4CAF50", "check"))
RED_X = _img_to_data_uri(_make_circle_icon(32, "#ef5350", "x"))
NA_BADGE = _img_to_data_uri(_make_na_badge(32))
WHITE_CHECK = _img_to_data_uri(_make_header_icon(44, "check"))
WHITE_X = _img_to_data_uri(_make_header_icon(44, "x"))
GREY_NA = _img_to_data_uri(_make_header_icon(44, "na"))
BUG_ICON = _img_to_data_uri(_make_bug_icon(40))
DOT_GREEN = _img_to_data_uri(_make_dot(14, "#4CAF50"))
DOT_RED = _img_to_data_uri(_make_dot(14, "#ef5350"))
DOT_GREY = _img_to_data_uri(_make_dot(14, "#9e9e9e"))
TIMELINE_ICON = _img_to_data_uri(_make_timeline_icon(40))
LOGO = _img_to_data_uri(_make_checkpoint_logo(50))
