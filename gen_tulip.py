#!/usr/bin/env python3
"""
Тюльпан: ресурс 15x15, чистый код, ноль нейронок.

  resource_tulip.png — стебель + два листа + чашечка из трёх лепестков.

Палитра = цвета игры:
  лепестки: ягодный куст (D44535 / AC395E / 933025) + светлый блик E8736B
  листья:   ягодный куст (449438 / 346D2C / 2E5E26 / 55B946 / 2A5723)
Юнит-стиль: плоская заливка без контура, свет сверху-слева,
            якорь = нижняя кромка канваса.
"""
import os
from PIL import Image, ImageDraw

W = H = 15
OUT = 'tulip'
os.makedirs(OUT, exist_ok=True)

# ---------------- палитра ----------------
PETAL_HI = (232, 115, 107)  # блик лепестка (свет сверху-слева)
PETAL    = (212, 69, 53)    # D44535 — основной красный (ягоды)
PETAL_MID= (172, 57, 94)    # AC395E — розовая тень
PETAL_D  = (147, 48, 37)    # 933025 — тёмный красный (кончики/край)
LEAF_L   = (85, 185, 70)    # 55B946 — светлый лист
LEAF     = (68, 148, 56)    # 449438 — основной лист
LEAF_D   = (52, 109, 44)    # 346D2C — тёмный лист
LEAF_XD  = (42, 87, 35)     # 2A5723 — самый тёмный (тень у земли)

PALETTE = {PETAL_HI, PETAL, PETAL_MID, PETAL_D,
           LEAF_L, LEAF, LEAF_D, LEAF_XD}

# ---------------- пиксельная карта ----------------
# . прозрачный; лепесток: H блик / R основной / M розовая тень / D тёмный
# лист: L светлый / G основной / E тёмный / K самый тёмный
MAP = [
    '...............',
    '...............',
    '....D.....D....',
    '...DRD...DRD...',
    '...DRRHDHRRD...',
    '..DRRHHHHMRD...',
    '..DRHHHHMMRD...',
    '..DRRMMMMMRD...',
    '...DRMMMMRD....',
    '....DRMMRD.....',
    '..L..EGGE......',
    '..LG..GE....L..',
    '...GG.GE...GE..',
    '....GGGE..GE...',
    '.....KGEEK.....',
]

SYM = {'H': PETAL_HI, 'R': PETAL, 'M': PETAL_MID, 'D': PETAL_D,
       'L': LEAF_L, 'G': LEAF, 'E': LEAF_D, 'K': LEAF_XD}

assert all(len(r) == W for r in MAP) and len(MAP) == H

# ---------------- сборка ----------------
def to_image(rows, w=W, h=H):
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    px = im.load()
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in SYM:
                px[x, y] = SYM[ch] + (255,)
    return im

im = to_image(MAP)
im.save(f'{OUT}/resource_tulip.png')

data = [p for p in im.getdata() if p[3] > 0]
bad = [p for p in data if p[:3] not in PALETTE]
ys = [i // im.width for i, p in enumerate(im.getdata()) if p[3] > 0]
xs = [i % im.width for i, p in enumerate(im.getdata()) if p[3] > 0]
print(f'resource_tulip.png  пикс {len(data)}  мусор {len(bad)}  bbox {(min(xs), min(ys), max(xs), max(ys))}')

# ---------------- превью (поправь пути под свои ассеты / или скрипт пропустит) ----------------
ASSETS = 'assets'   # здесь лежат terrain4.png (луга) / terrain5.png (лес)
try:
    MEADOW = Image.open(f'{ASSETS}/terrain4.png').convert('RGBA')
    FOREST = Image.open(f'{ASSETS}/terrain5.png').convert('RGBA')
    BERRY  = Image.open(f'{ASSETS}/resource_berry.png').convert('RGBA')
except FileNotFoundError:
    print('превью пропущено: нет terrain4/terrain5/resource_berry в', ASSETS)
    raise SystemExit

Z = 10
tiles = [('луга', MEADOW), ('лес', FOREST)]
img = Image.new('RGB', (2 * (15 * Z + 16) + 8, 15 * Z + 90), (24, 22, 20))
d = ImageDraw.Draw(img)
for i, (name, soil) in enumerate(tiles):
    t = soil.resize((30 * Z, 30 * Z), Image.NEAREST)
    t.alpha_composite(im.resize((15 * Z, 15 * Z), Image.NEAREST), (0, 0))
    img.paste(t, (8 + i * (15 * Z + 16), 18))
    d.text((8 + i * (15 * Z + 16), 3), f'tulip {name}', fill=(220, 215, 205))

# рядом — референс ягодного куста в том же масштабе клетки
zb = 5
tb = MEADOW.resize((30 * zb, 30 * zb), Image.NEAREST)
tb.alpha_composite(BERRY.resize((30 * zb, 30 * zb), Image.NEAREST))
img.paste(tb, (8, 15 * Z + 34))
d.text((8, 15 * Z + 20), 'ref: berry (клетка 30)', fill=(220, 215, 205))
img.save('tulip_preview.png')
print('preview: tulip_preview.png')
