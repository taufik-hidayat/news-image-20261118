#!/usr/bin/env python3
"""Compose the final 1024x1024 entry.png for news-image-20261118.

Layout (1024x1024):
  header  0-118   navy band: "18 NOVEMBER 2026" + "WORLD NEWS - WEDNESDAY"
  image   118-460 generated 4-panel strip, resized to 1024x342
  footer  464-1000 four numbered story rows (headline + one-line summary)
  credit  1000-1024 small source line
All text is drawn with PIL/DejaVu (no AI-generated text anywhere).
"""
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

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

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

canvas = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(canvas)

# --- header band ---
d.rectangle([0, 0, W, 118], fill=NAVY)
f_title = ImageFont.truetype(FONT_BOLD, 58)
f_sub = ImageFont.truetype(FONT_BOLD, 22)
title = "18 NOVEMBER 2026"
tw = d.textlength(title, font=f_title)
d.text(((W - tw) / 2, 22), title, font=f_title, fill=(255, 255, 255))
sub = "W O R L D   N E W S   —   W E D N E S D A Y"
sw = d.textlength(sub, font=f_sub)
d.text(((W - sw) / 2, 84), sub, font=f_sub, fill=GOLD)

# --- image band ---
base = Image.open(BASE).convert("RGB")  # 2736x912, four vertical panels
band = base.resize((1024, 342), Image.LANCZOS)
canvas.paste(band, (0, 118))
d.rectangle([0, 460, W, 464], fill=RED)

# --- footer story rows ---
f_head = ImageFont.truetype(FONT_BOLD, 33)
f_body = ImageFont.truetype(FONT_REG, 23)
f_num = ImageFont.truetype(FONT_BOLD, 34)
row_top, row_h = 464, 134
for i, (num, head, body, color) in enumerate(stories):
    y = row_top + i * row_h
    # number badge
    d.rectangle([28, y + 39, 84, y + 95], fill=color)
    nw = d.textlength(num, font=f_num)
    d.text((28 + (56 - nw) / 2, y + 44), num, font=f_num, fill=(255, 255, 255))
    # headline + summary
    d.text((104, y + 24), head, font=f_head, fill=INK)
    d.text((104, y + 70), body, font=f_body, fill=GREY)
    if i < 3:
        d.line([28, y + row_h - 1, W - 28, y + row_h - 1], fill=(210, 204, 190), width=2)

# --- credit strip ---
f_credit = ImageFont.truetype(FONT_REG, 15)
credit = "Sources: AP  ·  BBC  ·  DW  ·  Rappler  ·  CNBC  —  18 November 2026"
cw = d.textlength(credit, font=f_credit)
d.text(((W - cw) / 2, 1002), credit, font=f_credit, fill=(120, 116, 108))

canvas.save(OUT, "PNG", optimize=True)
print("saved", OUT)
