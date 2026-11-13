#!/usr/bin/env python3
"""Build lain-preview.png: Lain poster art + palette swatches + theme name."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 800
BG = (18, 22, 29)          # #12161d
PANEL = (32, 38, 55)       # #202637
TEXT = (233, 230, 222)     # #e9e6de
MUTED = (154, 162, 180)    # #9aa2b4
GREEN = (127, 182, 133)    # #7fb685
LAV = (168, 156, 200)      # #a89cc8
BEIGE = (200, 169, 126)    # #c8a97e

FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_M = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'

img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

# left: poster art, cropped to 560x800
art = Image.open('/tmp/lain-candidates/tmdb-poster.jpg').convert('RGB')
aw, ah = art.size
target_ratio = 560 / 800
src_ratio = aw / ah
if src_ratio > target_ratio:
    nw = int(ah * target_ratio)
    # bias the crop left so Lain's face is whole and the title logo is
    # excluded rather than half-cut
    x_left = 200
    art = art.crop((x_left, 0, x_left + nw, ah))
else:
    nh = int(aw / target_ratio)
    art = art.crop((0, (ah - nh) // 2, aw, (ah + nh) // 2))
art = art.resize((560, 800), Image.LANCZOS)
img.paste(art, (0, 0))
d.line([(560, 0), (560, H)], fill=GREEN, width=4)

# right panel
x0 = 600
d.text((x0, 70), 'serial experiments', font=ImageFont.truetype(FONT, 30), fill=MUTED)
d.text((x0, 105), 'lain', font=ImageFont.truetype(FONT_B, 96), fill=TEXT)
d.text((x0, 215), 'KETTU MAX  •  custom theme', font=ImageFont.truetype(FONT, 26), fill=GREEN)
d.text((x0, 255), 'dark but soft — phosphor green,', font=ImageFont.truetype(FONT, 24), fill=MUTED)
d.text((x0, 288), 'lavender & warm beige', font=ImageFont.truetype(FONT, 24), fill=MUTED)

swatches = [
    ('Base', '#12161d', (18, 22, 29)),
    ('Raised', '#202637', (32, 38, 55)),
    ('Phosphor green', '#7fb685', GREEN),
    ('Lavender', '#a89cc8', LAV),
    ('Hair beige', '#c8a97e', BEIGE),
    ('Text', '#e9e6de', TEXT),
    ('Muted text', '#9aa2b4', MUTED),
    ('Danger rose', '#c07a7a', (192, 122, 122)),
]
y = 348
for name, hx, rgb in swatches:
    d.rounded_rectangle([x0, y, x0 + 64, y + 40], radius=8, fill=rgb,
                        outline=(58, 67, 86), width=1)
    d.text((x0 + 80, y + 3), name, font=ImageFont.truetype(FONT_B, 23), fill=TEXT)
    d.text((x0 + 330, y + 7), hx, font=ImageFont.truetype(FONT_M, 21), fill=MUTED)
    y += 47

d.text((x0, 748), 'install: paste the lain.json raw URL into Kettu > Themes',
       font=ImageFont.truetype(FONT, 18), fill=MUTED)

img.save('/home/hatch/workspace/projects/discord-mod/kettu-max/lain-preview.png')
print('saved lain-preview.png', img.size)
