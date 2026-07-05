import io
import os
import hashlib
from typing import Dict, List, Tuple, Optional

import requests
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

# ═══════════════════════════════════════════════════════════════════
# 🔐 SECURITY SETTINGS
# ═══════════════════════════════════════════════════════════════════
APP_PASSWORD = "KDPGIFT2026"
BRAND_NAME = "KDPEasy Studio"
TOOL_NAME = "Cover Studio"
WELCOME_MESSAGE = "Welcome, VIP Creator!"
# ═══════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════
# 📖 Prompt Builder — dropdown options
# ═══════════════════════════════════════════════════════════════════
BOOK_TYPES = {
    "📖 Picture book (ages 3-8)":     "picture book cover illustration",
    "🎨 Coloring book — COVER (colorful)": "vibrant fully-colored painted book cover illustration, bright saturated colors that pop on Amazon thumbnails, showcasing a colored version of the coloring pages inside",
    "📝 Coloring book — INTERIOR page":    "black-and-white line-art coloring book interior page with bold clean outlines on plain white background, ready for children to color in, no shading, no grayscale",
    "📕 Chapter book / Novel":         "chapter book cover illustration",
    "📓 Journal / Notebook":           "journal cover design",
    "📗 Workbook / Activity book":     "activity workbook cover illustration",
    "📔 Planner":                      "planner cover design",
    "📘 Guide / How-to":               "instructional guide book cover",
    "📙 Recipe book":                  "recipe book cover design",
    "📚 Memoir / Personal essay":      "memoir book cover illustration",
    "📖 Devotional / Christian":       "devotional book cover design",
}

GENRES = {
    "🧚 Fantasy & Magic":              "magical fantasy",
    "🌙 Bedtime & Sleepy":             "cozy bedtime",
    "🗡️ Adventure & Quest":           "adventurous quest",
    "💝 SEL & Feelings":               "emotional social-learning",
    "🔍 Mystery":                      "mysterious",
    "❤️ Romance":                     "romantic",
    "🚀 Sci-Fi & Space":              "science-fiction space",
    "🏡 Cozy / Slice of life":         "cozy slice-of-life",
    "🎭 Dark / Gothic":               "dark gothic atmospheric",
    "📚 Educational":                  "educational",
    "😄 Humor / Silly":               "humorous silly",
    "✝️ Christian / Faith":           "faith-based Christian",
    "🐾 Animal characters":            "animal-character-focused",
    "🎄 Seasonal / Holiday":           "seasonal holiday",
}

STYLES = {
    "🎨 Watercolor storybook":         "soft watercolor illustration with painterly brushwork",
    "🖌️ Digital painting":            "polished digital painting",
    "📜 Vintage retro":                "vintage retro illustration with muted palette",
    "💥 Bold graphic":                 "bold graphic vector illustration with strong outlines",
    "⚪ Minimalist modern":            "minimalist modern illustration with clean lines",
    "✨ Whimsical dreamy":             "whimsical dreamy illustration with glowing details",
    "📷 Realistic detailed":           "highly detailed realistic illustration",
    "🎭 Cartoon animation":            "cheerful cartoon animation style",
    "✏️ Hand-drawn sketch":           "hand-drawn sketch style with pencil texture",
    "🖼️ Storybook classic":          "classic storybook illustration reminiscent of golden-age children's books",
}

MOODS = {
    "☀️ Warm & inviting":             "warm golden lighting, inviting atmosphere",
    "🌊 Cool & calm":                 "cool blue palette, calm serene mood",
    "⚡ Dramatic & intense":          "dramatic lighting, intense composition",
    "🍯 Cozy & soft":                 "soft ambient light, cozy comforting mood",
    "🌈 Bright & cheerful":           "bright saturated colors, cheerful playful mood",
    "🌫️ Muted & thoughtful":         "muted tones, quiet thoughtful mood",
}

AGE_GROUPS = {
    "👶 Ages 3-5":     "ages 3-5, simple shapes, high contrast, big friendly characters",
    "🧒 Ages 6-8":     "ages 6-8, more detail, expressive characters",
    "👦 Ages 9-12":    "ages 9-12, richer scenes, more nuanced storytelling",
    "🧑 Teens":        "young adult, mature themes but age-appropriate",
    "👨 Adults":       "adult reader",
}

SPECIAL_ELEMENTS = [
    "Main character in hero pose",
    "Landscape / establishing shot",
    "Multiple characters together",
    "Symbolic objects (crown, book, lantern, key…)",
    "Nature elements (trees, flowers, stars, moon)",
    "Empty space at top for title text",
    "Empty space at bottom for author name",
    "Frame or border decoration",
]

# ═══════════════════════════════════════════════════════════════════
# 📐 KDP page sizes for composition
# ═══════════════════════════════════════════════════════════════════
KDP_SIZES: Dict[str, Tuple[float, float]] = {
    "6 × 9 in  (Standard novel)":       (6.0, 9.0),
    "6.14 × 9.21 in (Royal)":           (6.14, 9.21),
    "5 × 8 in (Digest novel)":          (5.0, 8.0),
    "5.5 × 8.5 in (Digest)":            (5.5, 8.5),
    "7 × 10 in (Workbook)":             (7.0, 10.0),
    "8 × 10 in (Picture book)":         (8.0, 10.0),
    "8.5 × 8.5 in (Square kids)":       (8.5, 8.5),
    "8.5 × 11 in (Letter)":             (8.5, 11.0),
    "A4 (210 × 297 mm)":                (8.27, 11.69),
    "A5 (148 × 210 mm)":                (5.83, 8.27),
}

# ═══════════════════════════════════════════════════════════════════
# 🔤 Fonts — downloaded from Google Fonts at runtime
# ═══════════════════════════════════════════════════════════════════
FONT_URLS = {
    "cinzel":        "https://raw.githubusercontent.com/google/fonts/main/ofl/cinzel/Cinzel%5Bwght%5D.ttf",
    "cormorant":     "https://raw.githubusercontent.com/google/fonts/main/ofl/cormorantgaramond/CormorantGaramond%5Bwght%5D.ttf",
    "fredoka":       "https://raw.githubusercontent.com/google/fonts/main/ofl/fredoka/Fredoka%5Bwdth,wght%5D.ttf",
    "quicksand":     "https://raw.githubusercontent.com/google/fonts/main/ofl/quicksand/Quicksand%5Bwght%5D.ttf",
    "caveat":        "https://raw.githubusercontent.com/google/fonts/main/ofl/caveat/Caveat%5Bwght%5D.ttf",
    "lora":          "https://raw.githubusercontent.com/google/fonts/main/ofl/lora/Lora%5Bwght%5D.ttf",
    "bangers":       "https://raw.githubusercontent.com/google/fonts/main/ofl/bangers/Bangers-Regular.ttf",
    "merriweather":  "https://raw.githubusercontent.com/google/fonts/main/ofl/merriweather/Merriweather%5Bopsz,wdth,wght%5D.ttf",
}

FONT_CHOICES = {
    "Cinzel (fairy tale, classic)":         ("cinzel",       800),
    "Fredoka (modern kids, playful)":       ("fredoka",      700),
    "Cormorant Garamond (elegant serif)":   ("cormorant",    600),
    "Quicksand (modern, friendly)":         ("quicksand",    600),
    "Caveat (handwritten)":                 ("caveat",       700),
    "Lora (readable elegant serif)":        ("lora",         600),
    "Bangers (bold comic)":                 ("bangers",      None),
    "Merriweather (traditional serif)":     ("merriweather", 700),
}

FONTS_DIR = "/tmp/kdpeasy_cover_fonts"

TEXT_POSITIONS = {
    "Top":     "top",
    "Center":  "center",
    "Bottom":  "bottom",
}

PANEL_STYLES = {
    "🚫 None (just shadow)":                "none",
    "🎨 Rounded panel behind text":         "rounded",
    "📏 Solid strip across cover":          "strip",
    "🌫️ Gradient darken title area":       "gradient",
}

# ═══════════════════════════════════════════════════════════════════
# Page config + CSS
# ═══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title=f"{BRAND_NAME} — {TOOL_NAME}",
    page_icon="🎨",
    layout="wide",
)

CUSTOM_CSS = """
<style>
    .main > div { padding-top: 2rem; }
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf3 100%); }
    .block-container { max-width: 1300px; }
    h1 { color: #1f2937; font-weight: 700; }
    h2, h3 { color: #1f2937; }
    .stButton>button {
        background-color: #4f46e5;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
    }
    .stButton>button:hover { background-color: #4338ca; color: white; }
    .stDownloadButton>button {
        background-color: #10b981;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.4rem;
        font-weight: 700;
    }
    .stDownloadButton>button:hover { background-color: #059669; color: white; }
    div[data-testid="stFileUploader"] {
        background-color: white;
        border-radius: 12px;
        padding: 1rem;
        border: 2px dashed #cbd5e1;
    }
    .info-card {
        background: white;
        padding: 1rem 1.2rem;
        border-radius: 10px;
        border-left: 4px solid #4f46e5;
        margin-bottom: 1rem;
    }
    .gift-card {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        padding: 1rem 1.2rem;
        border-radius: 10px;
        border-left: 4px solid #f59e0b;
        margin-bottom: 1rem;
        color: #78350f;
    }
    .login-card {
        background: white;
        padding: 2.5rem 2rem;
        border-radius: 16px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        max-width: 480px;
        margin: 3rem auto;
        text-align: center;
    }
    .login-card h2 { color: #1f2937; margin-bottom: 0.5rem; }
    .login-card .brand {
        color: #4f46e5;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        font-size: 0.85rem;
        margin-bottom: 1rem;
    }
    .prompt-box {
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        font-family: 'Consolas', 'Menlo', monospace;
        font-size: 0.9rem;
        color: #1f2937;
        margin-bottom: 1rem;
        white-space: pre-wrap;
    }
    .preview-box {
        background: white;
        padding: 0.8rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .template-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .template-card h4 {
        margin: 0 0 0.4rem 0;
        color: #4f46e5;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# 🔐 Password gate
# ═══════════════════════════════════════════════════════════════════
def check_password() -> bool:
    if st.session_state.get("auth_ok"):
        return True

    st.markdown(
        f"""
        <div class="login-card">
            <div class="brand">{BRAND_NAME} · 🎁 Free VIP Gift</div>
            <h2>🎨 {TOOL_NAME}</h2>
            <p style="color:#6b7280;margin-bottom:1.5rem;">
                Enter your VIP password to continue.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("login_form"):
        pw = st.text_input("Password", type="password",
                           label_visibility="collapsed",
                           placeholder="Enter password…")
        ok = st.form_submit_button("🔓 Unlock", use_container_width=True)

    if ok:
        if pw == APP_PASSWORD:
            st.session_state.auth_ok = True
            st.rerun()
        else:
            st.error("❌ Wrong password. Please try again.")
    return False


if not check_password():
    st.stop()


# ═══════════════════════════════════════════════════════════════════
# 🔤 Font manager
# ═══════════════════════════════════════════════════════════════════
@st.cache_resource(show_spinner="Loading fonts (first time only)…")
def ensure_fonts() -> Dict[str, str]:
    os.makedirs(FONTS_DIR, exist_ok=True)
    paths: Dict[str, str] = {}
    for name, url in FONT_URLS.items():
        local = os.path.join(FONTS_DIR, f"{name}.ttf")
        if not os.path.exists(local) or os.path.getsize(local) < 1000:
            try:
                r = requests.get(url, timeout=15, allow_redirects=True)
                r.raise_for_status()
                with open(local, "wb") as f:
                    f.write(r.content)
            except Exception:
                local = None
        paths[name] = local
    return paths


FONT_PATHS = ensure_fonts()


def load_font(kind: str, size: int, weight: Optional[int] = None) -> ImageFont.FreeTypeFont:
    path = FONT_PATHS.get(kind)
    if path and os.path.exists(path):
        try:
            font = ImageFont.truetype(path, size)
            if weight is not None:
                try:
                    font.set_variation_by_axes([weight])
                except Exception:
                    pass
            return font
        except Exception:
            pass
    return ImageFont.load_default()


# ═══════════════════════════════════════════════════════════════════
# Header + logout
# ═══════════════════════════════════════════════════════════════════
hl, hr = st.columns([5, 1])
with hl:
    st.markdown(
        f"<h1>🎨 {TOOL_NAME}  "
        f"<span style='color:#f59e0b;font-size:1rem;'>🎁 VIP gift</span></h1>"
        f"<p style='color:#6b7280;margin-top:-0.5rem;'>"
        f"{BRAND_NAME} — {WELCOME_MESSAGE}</p>",
        unsafe_allow_html=True,
    )
with hr:
    st.write("")
    if st.button("Logout", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()


# ═══════════════════════════════════════════════════════════════════
# 🎨 Text rendering helpers
# ═══════════════════════════════════════════════════════════════════
def text_size(draw, text, font):
    if not text:
        return (0, 0)
    bbox = draw.textbbox((0, 0), text, font=font)
    return (bbox[2] - bbox[0], bbox[3] - bbox[1])


def wrap_lines(draw, text, font, max_width):
    if not text:
        return []
    lines: List[str] = []
    for para in text.splitlines() or [text]:
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if text_size(draw, trial, font)[0] <= max_width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def fit_font_size(draw, text, font_kind, font_weight, max_width, max_height,
                  start_size, min_size=20):
    """Shrink font size until text fits within box."""
    size = start_size
    while size > min_size:
        font = load_font(font_kind, size, font_weight)
        lines = wrap_lines(draw, text, font, max_width)
        line_h = int(text_size(draw, "Ag", font)[1] * 1.25)
        total_h = line_h * len(lines)
        widest = max([text_size(draw, ln, font)[0] for ln in lines] or [0])
        if total_h <= max_height and widest <= max_width:
            return font, lines, line_h
        size -= max(2, size // 20)
    font = load_font(font_kind, min_size, font_weight)
    return font, wrap_lines(draw, text, font, max_width), int(text_size(draw, "Ag", font)[1] * 1.25)


def draw_text_with_shadow(draw, xy, text, font, fill, shadow=True):
    x, y = xy
    if shadow:
        shadow_offset = max(1, font.size // 40)
        draw.text((x + shadow_offset, y + shadow_offset), text,
                  font=font, fill=(0, 0, 0, 120))
    draw.text((x, y), text, font=font, fill=fill)


def hex_to_rgb(hex_str):
    h = hex_str.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def average_luminance(image, box=None):
    """Return average brightness (0-255) of image or box region."""
    im = image.convert("RGB")
    if box:
        im = im.crop(box)
    im = im.resize((30, 30))
    px = list(im.getdata())
    if not px:
        return 128
    total = sum(0.299 * r + 0.587 * g + 0.114 * b for r, g, b in px)
    return total / len(px)


# ═══════════════════════════════════════════════════════════════════
# 🖼️ Cover composition
# ═══════════════════════════════════════════════════════════════════
def compose_cover(art_bytes: bytes, page_w_in: float, page_h_in: float,
                  dpi: int, title: str, subtitle: str, author: str,
                  title_font_kind: str, title_font_weight: Optional[int],
                  body_font_kind: str, body_font_weight: Optional[int],
                  title_position: str, text_color: str,
                  auto_contrast: bool, add_bleed: bool,
                  add_shadow: bool,
                  panel_style: str = "none",
                  panel_color: str = "#000000",
                  panel_opacity: float = 0.55) -> Image.Image:
    bleed_in = 0.125 if add_bleed else 0.0
    trim_w_px = int(round(page_w_in * dpi))
    trim_h_px = int(round(page_h_in * dpi))
    bleed_px = int(round(bleed_in * dpi))
    final_w = trim_w_px + 2 * bleed_px
    final_h = trim_h_px + 2 * bleed_px

    # Fill canvas with art (fill mode to cover bleed area)
    art = Image.open(io.BytesIO(art_bytes))
    art = ImageOps.exif_transpose(art)
    if art.mode != "RGB":
        art = art.convert("RGB")

    sw, sh = art.size
    scale = max(final_w / sw, final_h / sh)
    new_w = int(round(sw * scale))
    new_h = int(round(sh * scale))
    fitted = art.resize((new_w, new_h), Image.LANCZOS)
    x = (final_w - new_w) // 2
    y = (final_h - new_h) // 2
    canvas = Image.new("RGB", (final_w, final_h), (30, 30, 30))
    canvas.paste(fitted, (x, y))

    draw = ImageDraw.Draw(canvas)

    # Text layout — inside trim + safe area
    safe_pad = int(trim_w_px * 0.08)
    safe_left = bleed_px + safe_pad
    safe_right = final_w - bleed_px - safe_pad
    safe_top = bleed_px + safe_pad
    safe_bottom = final_h - bleed_px - safe_pad
    safe_w = safe_right - safe_left

    # Vertical zones based on title_position
    if title_position == "top":
        title_zone_top = safe_top
        title_zone_bottom = safe_top + int(trim_h_px * 0.28)
    elif title_position == "bottom":
        title_zone_top = safe_bottom - int(trim_h_px * 0.35)
        title_zone_bottom = safe_bottom
    else:  # center
        cy = final_h // 2
        title_zone_top = cy - int(trim_h_px * 0.16)
        title_zone_bottom = cy + int(trim_h_px * 0.16)

    # Auto-contrast text color
    if auto_contrast:
        zone_box = (safe_left, title_zone_top, safe_right, title_zone_bottom)
        avg_lum = average_luminance(canvas, zone_box)
        text_fill = (255, 255, 255) if avg_lum < 130 else (25, 25, 45)
    else:
        text_fill = hex_to_rgb(text_color)

    # Draw text background panel (if enabled) BEFORE the text
    if panel_style != "none":
        panel_rgb = hex_to_rgb(panel_color)
        alpha = int(255 * max(0.0, min(1.0, panel_opacity)))
        overlay = Image.new("RGBA", (final_w, final_h), (0, 0, 0, 0))
        over_draw = ImageDraw.Draw(overlay)
        pad_x = int(trim_w_px * 0.04)
        pad_y = int(trim_h_px * 0.02)

        if panel_style == "rounded":
            box = (
                max(bleed_px, safe_left - pad_x),
                max(bleed_px, title_zone_top - pad_y),
                min(final_w - bleed_px, safe_right + pad_x),
                min(final_h - bleed_px, title_zone_bottom + pad_y),
            )
            radius = int(min(box[2] - box[0], box[3] - box[1]) * 0.08)
            over_draw.rounded_rectangle(box, radius=radius,
                                         fill=panel_rgb + (alpha,))
        elif panel_style == "strip":
            box = (
                0,
                max(bleed_px, title_zone_top - pad_y),
                final_w,
                min(final_h - bleed_px, title_zone_bottom + pad_y),
            )
            over_draw.rectangle(box, fill=panel_rgb + (alpha,))
        elif panel_style == "gradient":
            # Vertical gradient darkening across the title zone
            grad_top = max(bleed_px, title_zone_top - pad_y * 2)
            grad_bottom = min(final_h - bleed_px, title_zone_bottom + pad_y * 2)
            grad_h = max(1, grad_bottom - grad_top)
            for row in range(grad_top, grad_bottom):
                # Ease-in-out alpha peak in middle
                t = (row - grad_top) / grad_h
                bell = 1 - abs(2 * t - 1)
                row_alpha = int(alpha * bell)
                over_draw.line([(0, row), (final_w, row)],
                                fill=panel_rgb + (row_alpha,))

        canvas = Image.alpha_composite(
            canvas.convert("RGBA"), overlay
        ).convert("RGB")
        draw = ImageDraw.Draw(canvas)

    # Title
    if title.strip():
        title_max_h = int((title_zone_bottom - title_zone_top) * 0.7)
        start_size = int(trim_w_px * 0.13)
        t_font, t_lines, t_line_h = fit_font_size(
            draw, title, title_font_kind, title_font_weight,
            safe_w, title_max_h, start_size,
        )
        block_h = t_line_h * len(t_lines)
        y_cur = title_zone_top + max(0, (title_zone_bottom - title_zone_top - block_h) // 2)
        for ln in t_lines:
            w = text_size(draw, ln, t_font)[0]
            x_ln = safe_left + (safe_w - w) // 2
            draw_text_with_shadow(draw, (x_ln, y_cur), ln, t_font, text_fill,
                                   shadow=add_shadow)
            y_cur += t_line_h

    # Subtitle — right below title
    if subtitle.strip() and title.strip():
        sub_start_size = int(trim_w_px * 0.055)
        sub_font, sub_lines, sub_line_h = fit_font_size(
            draw, subtitle, body_font_kind, body_font_weight,
            safe_w, int(trim_h_px * 0.08), sub_start_size,
        )
        y_sub = y_cur + int(sub_line_h * 0.3)
        for ln in sub_lines:
            w = text_size(draw, ln, sub_font)[0]
            x_ln = safe_left + (safe_w - w) // 2
            draw_text_with_shadow(draw, (x_ln, y_sub), ln, sub_font, text_fill,
                                   shadow=add_shadow)
            y_sub += sub_line_h

    # Author — bottom of safe area (unless title is at bottom, then above title)
    if author.strip():
        author_font_size = int(trim_w_px * 0.055)
        a_font, a_lines, a_line_h = fit_font_size(
            draw, author, body_font_kind, body_font_weight,
            safe_w, int(trim_h_px * 0.08), author_font_size,
        )
        if title_position == "bottom":
            y_author = title_zone_top - a_line_h - int(trim_w_px * 0.03)
        else:
            block_h = a_line_h * len(a_lines)
            y_author = safe_bottom - block_h
        for ln in a_lines:
            w = text_size(draw, ln, a_font)[0]
            x_ln = safe_left + (safe_w - w) // 2
            draw_text_with_shadow(draw, (x_ln, y_author), ln, a_font, text_fill,
                                   shadow=add_shadow)
            y_author += a_line_h

    return canvas


@st.cache_data(show_spinner=False, max_entries=40)
def compose_cover_cached(art_bytes: bytes, page_w_in: float, page_h_in: float,
                          dpi: int, title: str, subtitle: str, author: str,
                          title_font_kind: str, title_font_weight: Optional[int],
                          body_font_kind: str, body_font_weight: Optional[int],
                          title_position: str, text_color: str,
                          auto_contrast: bool, add_bleed: bool,
                          add_shadow: bool,
                          panel_style: str = "none",
                          panel_color: str = "#000000",
                          panel_opacity: float = 0.55,
                          _v: int = 2) -> bytes:
    img = compose_cover(
        art_bytes, page_w_in, page_h_in, dpi, title, subtitle, author,
        title_font_kind, title_font_weight, body_font_kind, body_font_weight,
        title_position, text_color, auto_contrast, add_bleed, add_shadow,
        panel_style, panel_color, panel_opacity,
    )
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def preview_bytes(png: bytes, max_edge: int = 700) -> bytes:
    img = Image.open(io.BytesIO(png))
    w, h = img.size
    long_edge = max(w, h)
    if long_edge > max_edge:
        scale = max_edge / long_edge
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="JPEG", quality=88)
    return buf.getvalue()


# ═══════════════════════════════════════════════════════════════════
# 🪄 Prompt Builder logic
# ═══════════════════════════════════════════════════════════════════
def build_prompt(book_type: str, genre: str, style: str, mood: str,
                 age: str, elements: List[str], custom_add: str,
                 kdp_size_label: str) -> str:
    book_frag = BOOK_TYPES[book_type]
    genre_frag = GENRES[genre]
    style_frag = STYLES[style]
    mood_frag = MOODS[mood]
    age_frag = AGE_GROUPS[age]

    element_frag = ""
    if elements:
        element_frag = ". Include: " + ", ".join(el.lower() for el in elements)

    # Size hint
    w, h = KDP_SIZES.get(kdp_size_label, (6.0, 9.0))
    if abs(w - h) < 0.5:
        size_hint = "square 1:1 aspect ratio"
    elif h > w:
        size_hint = f"portrait aspect ratio approximately {w}:{h}"
    else:
        size_hint = f"landscape aspect ratio approximately {w}:{h}"

    prompt = (
        f"A {style_frag} for a {genre_frag} {book_frag}. "
        f"{mood_frag}. "
        f"Targeted at {age_frag}"
        f"{element_frag}. "
        f"Composition uses {size_hint}. "
        f"High detail, print-ready quality. "
        f"Do NOT include any text, letters, words, title, or logo in the image "
        f"— text will be added later separately."
    )
    if custom_add.strip():
        prompt += f" Additional details: {custom_add.strip()}"
    return prompt


# ═══════════════════════════════════════════════════════════════════
# UI — 3 tabs
# ═══════════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs([
    "🪄 Prompt Builder",
    "🖼️ Cover Composer",
    "📚 Template Gallery",
])


# ═══════════════════════════════════════════════════════════════════
# TAB 1 — Prompt Builder
# ═══════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### Turn your book idea into a ready-to-paste ChatGPT / Midjourney prompt")
    st.caption("Pick your options → get a professional-quality prompt in seconds.")

    c1, c2 = st.columns(2)
    with c1:
        pb_book_type = st.selectbox("📖 Book type", list(BOOK_TYPES.keys()), index=0, key="pb_book")
        pb_genre = st.selectbox("🎭 Genre / theme", list(GENRES.keys()), index=0, key="pb_genre")
        pb_style = st.selectbox("🎨 Illustration style", list(STYLES.keys()), index=0, key="pb_style")
        pb_size = st.selectbox("📐 Target KDP trim size", list(KDP_SIZES.keys()), index=0, key="pb_size")
    with c2:
        pb_mood = st.selectbox("🌈 Mood", list(MOODS.keys()), index=0, key="pb_mood")
        pb_age = st.selectbox("👶 Age group", list(AGE_GROUPS.keys()), index=1, key="pb_age")
        pb_elements = st.multiselect(
            "✨ Elements to include",
            SPECIAL_ELEMENTS,
            default=[SPECIAL_ELEMENTS[0], SPECIAL_ELEMENTS[5]],
            key="pb_elements",
        )
        pb_custom = st.text_input(
            "➕ Anything else? (character name, colour, object…)",
            placeholder="e.g. main character is a small orange dragon named Ember",
            key="pb_custom",
        )

    prompt = build_prompt(
        pb_book_type, pb_genre, pb_style, pb_mood, pb_age,
        pb_elements, pb_custom, pb_size,
    )

    st.markdown("### 📋 Your ready-to-paste prompt")
    st.markdown(f'<div class="prompt-box">{prompt}</div>', unsafe_allow_html=True)

    ppc1, ppc2 = st.columns([1, 2])
    with ppc1:
        st.download_button(
            "⬇️ Download as .txt",
            data=prompt,
            file_name="cover-prompt.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with ppc2:
        st.caption(
            "👉 Copy the prompt above, paste it into **ChatGPT Image** "
            "(or Midjourney / DALL-E / Leonardo). "
            "Then bring the resulting art into the **Cover Composer** tab "
            "to add title, subtitle, and author."
        )


# ═══════════════════════════════════════════════════════════════════
# TAB 2 — Cover Composer
# ═══════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### Turn your AI art into a KDP-ready cover with title, subtitle & author")

    left, right = st.columns([1, 1])

    with left:
        st.markdown("#### 1️⃣ Upload cover art")
        art_file = st.file_uploader(
            "PNG / JPG / WEBP — ideally the AI illustration from Tab 1",
            type=["png", "jpg", "jpeg", "webp"],
            accept_multiple_files=False,
            key="cc_art",
        )

        st.markdown("#### 2️⃣ Book text")
        cc_title = st.text_input("Title", placeholder="Ember and the Moonlit Book",
                                  key="cc_title")
        cc_subtitle = st.text_input("Subtitle (optional)",
                                     placeholder="A bedtime story for brave dreamers",
                                     key="cc_subtitle")
        cc_author = st.text_input("Author name", placeholder="Lucky Smith",
                                   key="cc_author")

        st.markdown("#### 3️⃣ Design")
        cc_size_label = st.selectbox("KDP trim size", list(KDP_SIZES.keys()),
                                      index=6, key="cc_size")
        cc_w_in, cc_h_in = KDP_SIZES[cc_size_label]

        cc_title_font_label = st.selectbox(
            "Title font",
            list(FONT_CHOICES.keys()),
            index=0,
            key="cc_title_font",
        )
        title_font_kind, title_font_weight = FONT_CHOICES[cc_title_font_label]

        cc_body_font_label = st.selectbox(
            "Subtitle & author font",
            list(FONT_CHOICES.keys()),
            index=2,
            key="cc_body_font",
        )
        body_font_kind, body_font_weight = FONT_CHOICES[cc_body_font_label]

        cc_position = st.radio(
            "Title position",
            list(TEXT_POSITIONS.keys()),
            index=0,
            horizontal=True,
            key="cc_position",
        )

        cc_auto = st.checkbox(
            "🪄 Auto-contrast text colour",
            value=True,
            help="Automatically picks white or dark text based on the art.",
            key="cc_auto",
        )
        if not cc_auto:
            cc_color = st.color_picker("Text colour", "#FFFFFF", key="cc_color")
        else:
            cc_color = "#FFFFFF"

        cc_shadow = st.checkbox("Add subtle text shadow (recommended)",
                                 value=True, key="cc_shadow")

        st.markdown("**Text background panel** (recommended for busy art)")
        cc_panel_label = st.selectbox(
            "Panel style",
            list(PANEL_STYLES.keys()),
            index=1,
            label_visibility="collapsed",
            key="cc_panel_label",
            help="A semi-transparent panel behind the title makes text readable "
                 "even when the art has busy details in the title area.",
        )
        cc_panel_style = PANEL_STYLES[cc_panel_label]

        if cc_panel_style != "none":
            pcol1, pcol2 = st.columns([1, 1])
            with pcol1:
                cc_panel_color = st.color_picker("Panel colour", "#000000",
                                                  key="cc_panel_color")
            with pcol2:
                cc_panel_opacity = st.slider("Opacity", 0.0, 1.0, 0.55, 0.05,
                                              key="cc_panel_opacity")
        else:
            cc_panel_color = "#000000"
            cc_panel_opacity = 0.55

        cc_bleed = st.checkbox("Include KDP bleed (0.125\")",
                                value=True, key="cc_bleed")

        cc_dpi = st.number_input("Output DPI (300 = KDP standard)",
                                  min_value=150, max_value=600, value=300, step=50,
                                  key="cc_dpi")

    with right:
        st.markdown("#### 👀 Live preview")
        if art_file is None:
            st.info("👈 Upload cover art on the left to see the preview.")
        else:
            try:
                art_bytes = art_file.getvalue()
                png = compose_cover_cached(
                    art_bytes, float(cc_w_in), float(cc_h_in), int(cc_dpi),
                    cc_title, cc_subtitle, cc_author,
                    title_font_kind, title_font_weight,
                    body_font_kind, body_font_weight,
                    TEXT_POSITIONS[cc_position], cc_color,
                    bool(cc_auto), bool(cc_bleed), bool(cc_shadow),
                    cc_panel_style, cc_panel_color, float(cc_panel_opacity),
                )
                st.markdown('<div class="preview-box">', unsafe_allow_html=True)
                st.image(preview_bytes(png), use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

                bleed_note = " + 0.125\" bleed each side" if cc_bleed else ""
                out_w = cc_w_in + (0.25 if cc_bleed else 0)
                out_h = cc_h_in + (0.25 if cc_bleed else 0)
                st.caption(
                    f"Output PNG: **{int(out_w * cc_dpi)} × {int(out_h * cc_dpi)} px**  •  "
                    f"{out_w:.3f}\" × {out_h:.3f}\" @ {cc_dpi} DPI{bleed_note}"
                )

                slug = "".join(c if c.isalnum() or c in "-_" else "-"
                                for c in (cc_title or "cover")).strip("-").lower()
                if not slug:
                    slug = "cover"

                st.download_button(
                    f"⬇️ Download {slug}-front-cover.png",
                    data=png,
                    file_name=f"{slug}-front-cover.png",
                    mime="image/png",
                    use_container_width=True,
                )
            except Exception as e:
                st.error(f"Preview error: {e}")


# ═══════════════════════════════════════════════════════════════════
# TAB 3 — Template Gallery
# ═══════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### Layout ideas — proven title positions & style combos")
    st.caption("Use these as inspiration when configuring your cover in the Composer tab.")

    templates = [
        {
            "title": "🌙 Classic Bedtime Storybook",
            "position": "Top",
            "font_title": "Cinzel (fairy tale, classic)",
            "font_body": "Cormorant Garamond (elegant serif)",
            "note": "Big title at top, character centred, author subtle at bottom.",
        },
        {
            "title": "🎨 Modern Kids Picture Book",
            "position": "Bottom",
            "font_title": "Fredoka (modern kids, playful)",
            "font_body": "Quicksand (modern, friendly)",
            "note": "Full-bleed illustration up top, chunky title at bottom.",
        },
        {
            "title": "🧚 Fairy Tale with Gold Accents",
            "position": "Top",
            "font_title": "Cinzel (fairy tale, classic)",
            "font_body": "Lora (readable elegant serif)",
            "note": "Ornate title, warm palette, subtitle below title.",
        },
        {
            "title": "🎨 Coloring Book Cover",
            "position": "Top",
            "font_title": "Fredoka (modern kids, playful)",
            "font_body": "Quicksand (modern, friendly)",
            "note": "Colour version of your line art. Big bold title. Show 1-2 sample pages if space.",
        },
        {
            "title": "📓 Journal / Notebook Elegant",
            "position": "Center",
            "font_title": "Cormorant Garamond (elegant serif)",
            "font_body": "Lora (readable elegant serif)",
            "note": "Minimalist, centred title on soft background. Author on the spine.",
        },
        {
            "title": "🗡️ Adventure Chapter Book",
            "position": "Top",
            "font_title": "Bangers (bold comic)",
            "font_body": "Merriweather (traditional serif)",
            "note": "Bold title impact, dramatic art, series number as subtitle.",
        },
        {
            "title": "📝 Handwritten Journal",
            "position": "Center",
            "font_title": "Caveat (handwritten)",
            "font_body": "Quicksand (modern, friendly)",
            "note": "Feels personal, best for gratitude journals & memoirs.",
        },
        {
            "title": "🌫️ Muted SEL Storybook",
            "position": "Bottom",
            "font_title": "Cormorant Garamond (elegant serif)",
            "font_body": "Lora (readable elegant serif)",
            "note": "Emotional theme books — muted palette, quiet composition.",
        },
        {
            "title": "🚀 Sci-Fi / Space Chapter Book",
            "position": "Top",
            "font_title": "Bangers (bold comic)",
            "font_body": "Quicksand (modern, friendly)",
            "note": "Dark cosmic art, glowing title, series-appropriate subtitle.",
        },
        {
            "title": "❤️ Cozy Family Story",
            "position": "Bottom",
            "font_title": "Fredoka (modern kids, playful)",
            "font_body": "Lora (readable elegant serif)",
            "note": "Warm, hug-worthy art. Rounded title at bottom, character front and centre.",
        },
    ]

    cols = st.columns(2)
    for i, tpl in enumerate(templates):
        col = cols[i % 2]
        with col:
            st.markdown(
                f'<div class="template-card">'
                f'<h4>{tpl["title"]}</h4>'
                f'<b>Position:</b> {tpl["position"]}<br>'
                f'<b>Title font:</b> {tpl["font_title"]}<br>'
                f'<b>Body font:</b> {tpl["font_body"]}<br>'
                f'<em>{tpl["note"]}</em>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="gift-card" style="margin-top:1rem;">'
        "💡 <b>How to use:</b> Pick a template that matches your book's mood, "
        "then jump to the <b>Cover Composer</b> tab and use the same title "
        "position + font pairing. You'll get a professional cover in 2 minutes."
        "</div>",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════
# Footer
# ═══════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    f"<div style='text-align:center;color:#9ca3af;font-size:0.85rem;'>"
    f"{BRAND_NAME} — {TOOL_NAME} 🎁  •  "
    f"Made with ❤️ for KDP & Etsy creators"
    f"</div>",
    unsafe_allow_html=True,
)
