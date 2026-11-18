#!/usr/bin/env python3
"""Compose the final 1024x1024 entry.png for news-image-20261118.

Layout (1024x1024):
  header  0-118   navy band: "18 NOVEMBER 2026" + "WORLD NEWS - WEDNESDAY"
  image   118-460 generated 4-panel strip, resized to 1024x342
  footer  464-1000 four numbered story rows (headline + one-line summary)
  credit  1000-1024 small source line
All text is drawn with PIL/DejaVu (no AI-generated text anywhere).

Layout numbers live in the constants below so the geometry can be
checked at a glance; the drawing itself is unchanged from the first
version, and re-running this script must reproduce entry.png byte
for byte.
"""
import os

from PIL import Image, ImageDraw, ImageFont

REPO = "/home/hatch/workspace/makefun-roblox-kit/news-image-20261118-repo"
BASE = REPO + "/work/media-generation-news-base-0-504c82b0-8e4a-4cb4-a6ce-960df20dbc14.png"
OUT = REPO + "/entry.png"

W, H = 1024, 1024
NAVY = (16, 35, 63)
GOLD = (201, 162, 39)
PAPER = (247, 243, 234)
INK = (16, 35, 63)
GREY = (58, 58, 58)
RED = (178, 58, 44)
WHITE = (255, 255, 255)
SEPARATOR = (210, 204, 190)
CREDIT_GREY = (120, 116, 108)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# --- layout geometry (all in pixels) ---
HEADER_H = 118
TITLE_Y = 22
SUB_Y = 84
BAND_H = 342
RULE_H = 4
ROWS_TOP = 464
ROW_H = 134
BADGE_X = 28
BADGE_SIZE = 56
BADGE_TOP = 39
NUM_Y = 44
TEXT_X = 104
HEAD_Y = 24
BODY_Y = 70
MARGIN = 28
CREDIT_Y = 1002

# Expected size of the generated 4-panel base image; composing against a
# different size would silently stretch the panels, so fail loudly instead.
BASE_SIZE = (2736, 912)

stories = [
    ("1", "TRUMP MEETS MARCOS IN MANILA",
     "APEC opens in Shenzhen; Xi-Putin talks Thursday", (31, 78, 121)),
    ("2", "UKRAINE HITS CRIMEA BRIDGE AGAIN",
     "Second day of strikes as Russia pounds Kyiv bridges", (122, 59, 46)),
    ("3", "NVIDIA POSTS $115.8B QUARTER",
     "Revenue up 103% as AI stocks slide worldwide", (46, 111, 106)),
    ("4", "CANADA AND CHINA CUT TARIFFS",
     "Xi meets Carney as leaders gather for APEC", (138, 109, 27)),
]

f_title = ImageFont.truetype(FONT_BOLD, 58)
f_sub = ImageFont.truetype(FONT_BOLD, 22)
f_head = ImageFont.truetype(FONT_BOLD, 33)
f_body = ImageFont.truetype(FONT_REG, 23)
f_num = ImageFont.truetype(FONT_BOLD, 34)
f_credit = ImageFont.truetype(FONT_REG, 15)


def centered_text(draw, y, text, font, fill):
    """Draw one line of text horizontally centred on the canvas."""
    w = draw.textlength(text, font=font)
    draw.text(((W - w) / 2, y), text, font=font, fill=fill)


def story_row(draw, i, num, head, body, color):
    """Draw one numbered footer row: colour badge, headline, summary."""
    y = ROWS_TOP + i * ROW_H
    draw.rectangle(
        [BADGE_X, y + BADGE_TOP,
         BADGE_X + BADGE_SIZE, y + BADGE_TOP + BADGE_SIZE],
        fill=color)
    nw = draw.textlength(num, font=f_num)
    draw.text((BADGE_X + (BADGE_SIZE - nw) / 2, y + NUM_Y), num,
              font=f_num, fill=WHITE)
    draw.text((TEXT_X, y + HEAD_Y), head, font=f_head, fill=INK)
    draw.text((TEXT_X, y + BODY_Y), body, font=f_body, fill=GREY)
    if i < len(stories) - 1:
        draw.line([MARGIN, y + ROW_H - 1, W - MARGIN, y + ROW_H - 1],
                  fill=SEPARATOR, width=2)


def load_base_image(path):
    """Return the generated panel strip, rejecting a wrong-sized one."""
    if not os.path.exists(path):
        raise SystemExit(f"base image missing: {path}")
    base = Image.open(path).convert("RGB")
    if base.size != BASE_SIZE:
        raise SystemExit(
            f"unexpected base image size {base.size}, expected {BASE_SIZE}")
    return base


canvas = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(canvas)

# --- header band ---
d.rectangle([0, 0, W, HEADER_H], fill=NAVY)
centered_text(d, TITLE_Y, "18 NOVEMBER 2026", f_title, WHITE)
centered_text(d, SUB_Y, "W O R L D   N E W S   —   W E D N E S D A Y",
              f_sub, GOLD)

# --- image band ---
base = load_base_image(BASE)
band = base.resize((W, BAND_H), Image.LANCZOS)
canvas.paste(band, (0, HEADER_H))
d.rectangle([0, HEADER_H + BAND_H, W, HEADER_H + BAND_H + RULE_H], fill=RED)

# --- footer story rows ---
for i, (num, head, body, color) in enumerate(stories):
    story_row(d, i, num, head, body, color)

# --- credit strip ---
centered_text(d, CREDIT_Y,
              "Sources: AP  ·  BBC  ·  DW  ·  Rappler  ·  CNBC  —  18 November 2026",
              f_credit, CREDIT_GREY)

canvas.save(OUT, "PNG", optimize=True)
print("saved", OUT)
