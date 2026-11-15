#!/usr/bin/env python3
"""Draw the original off-season pixel lettering. Regeneration requires Pillow."""

import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent.parent
TITLE = "МЕЖСЕЗОНЬЕ"
DISPLAY_HEIGHT = 22
DISPLAY_ASCENT = 20
GLYPHS = {
    "М": ["1100011", "1110111", "1111111", "1101011", "1100011",
          "1100011", "1100011", "1100011", "1100011"],
    "Е": ["1111111", "1111111", "1100000", "1100000", "1111100",
          "1100000", "1100000", "1111111", "1111111"],
    "Ж": ["1101011", "1101011", "0111110", "0011100", "0011100",
          "0011100", "0111110", "1101011", "1101011"],
    "С": ["0111111", "1111111", "1100000", "1100000", "1100000",
          "1100000", "1100000", "1111111", "0111111"],
    "З": ["1111110", "1111111", "0000011", "0000011", "0011110",
          "0000011", "0000011", "1111111", "1111110"],
    "О": ["0111110", "1111111", "1100011", "1100011", "1100011",
          "1100011", "1100011", "1111111", "0111110"],
    "Н": ["1100011", "1100011", "1100011", "1100011", "1111111",
          "1100011", "1100011", "1100011", "1100011"],
    "Ь": ["1100000", "1100000", "1100000", "1100000", "1111110",
          "1111111", "1100011", "1111111", "1111110"],
}
STOPS = [(0.0, (163, 185, 166)), (0.48, (224, 222, 211)), (1.0, (188, 155, 166))]


def color_at(position):
    for (left, a), (right, b) in zip(STOPS, STOPS[1:]):
        if position <= right:
            t = (position - left) / (right - left)
            return tuple(round(x + (y - x) * t) for x, y in zip(a, b))
    return STOPS[-1][1]


def offset_mask(mask, x, y):
    result = Image.new("L", mask.size)
    result.paste(mask, (x, y))
    return result


def main():
    # Wide stems, clipped corners, a shallow bevel and a quiet, three-color fade.
    # The width stays below 330 GUI pixels even with the large bitmap provider.
    mask = Image.new("L", (324, 34))
    draw = ImageDraw.Draw(mask)
    for index, character in enumerate(TITLE):
        for row, line in enumerate(GLYPHS[character]):
            for column, pixel in enumerate(line):
                if pixel == "1":
                    x, y = 2 + index * 32 + column * 4, 2 + row * 3
                    draw.rectangle((x, y, x + 3, y + 2), fill=255)

    title = Image.new("RGBA", mask.size)
    outline = mask.filter(ImageFilter.MaxFilter(3))
    title.paste((28, 35, 33, 255), (0, 0), outline)
    for distance in (3, 2, 1):
        title.paste((47, 54, 49, 255), (0, 0), offset_mask(outline, distance, distance))

    top_edge = ImageChops.subtract(mask, offset_mask(mask, 0, 1))
    bottom_edge = ImageChops.subtract(mask, offset_mask(mask, 0, -1))
    for y in range(mask.height):
        for x in range(mask.width):
            if not mask.getpixel((x, y)):
                continue
            color = color_at(max(0, min(1, (x - 2) / 315)))
            factor = 1.12 if top_edge.getpixel((x, y)) else 0.70 if bottom_edge.getpixel((x, y)) else 1 - y / 160
            title.putpixel((x, y), (*[min(255, round(channel * factor)) for channel in color], 255))

    texture = ROOT / "assets/domsmp/textures/font/off_season_title.png"
    texture.parent.mkdir(parents=True, exist_ok=True)
    title.save(texture)
    font = ROOT / "assets/domsmp/font/off_season.json"
    font.parent.mkdir(parents=True, exist_ok=True)
    font.write_text(json.dumps({"providers": [{
        "type": "bitmap", "file": "domsmp:font/off_season_title.png",
        # Two 162px cells fit Minecraft's 256px glyph atlas; one 324px cell does not.
        "height": DISPLAY_HEIGHT, "ascent": DISPLAY_ASCENT, "chars": ["\ue110\ue111"],
    }]}, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

    # A lettering preview, not an in-game screenshot. It never enters the pack.
    preview = Image.new("RGBA", (364, 80), (25, 29, 27, 255))
    displayed = title.resize((round(title.width * DISPLAY_HEIGHT / title.height), DISPLAY_HEIGHT),
                             Image.Resampling.NEAREST)
    preview.alpha_composite(displayed, ((preview.width - displayed.width) // 2, 14))
    label = ImageDraw.Draw(preview)
    face = ImageFont.truetype("DejaVuSans.ttf", 10)
    label.text((182, 54), "Общий онлайн: 1", font=face, fill=(190, 200, 189), anchor="mm")
    (ROOT / "dist").mkdir(exist_ok=True)
    preview.resize((1092, 240), Image.Resampling.NEAREST).save(ROOT / "dist/off-season-preview.png")
    print(f"Generated {texture.relative_to(ROOT)} and {font.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
