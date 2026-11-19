#!/usr/bin/env python3
"""Animated icon for Apocalypse Begins [BETA], stamped with the current modpack version.

The send-off icon's method: the night shot of the twin towers (src/towers.webp) is cropped square,
blurred and darkened behind blocky pixel letters. The loop: the towers' lights are on, flicker and
go out from the ground up, "BETA <version>" fades in over the dark city, then the power comes back
and the loop starts again. A slow push-in runs under all of it.

Writes to out/<version>/: icon.webp (animated, 400x400), icon.gif (fallback, half the frame rate),
still.png and still_dark.png (one lit and one dark frame), sheet.png (eight moments of the loop),
preview_64.png (the lit frame as a small thumbnail, enlarged), static.png (the lit frame with the
version showing, 400x400) and server-icon.png (the same, 64x64, the only size and format a server
list accepts).

With --place it also copies them into the pack: CLIENT/profileImage/icon.webp and icon.png, and
SERVER/server-icon.png.

Usage: python tools/icon/make_icon.py [version, default the one in CLIENT/manifest.json] [--place]
"""
import json
import math
import os
import random
import shutil
import sys

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
SOURCE = os.path.join(HERE, "src", "towers.webp")
MANIFEST = os.path.join(ROOT, "CLIENT", "manifest.json")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
PLACE = "--place" in sys.argv[1:]

SIZE = 400            # output edge
WORK = 800            # render edge (downscaled at the end for clean edges)
FPS = 15
SECONDS = 5.2
FRAMES = int(FPS * SECONDS)

TITLE = ["APOCALYPSE", "BEGINS"]
WHITE = (255, 255, 255)
OUTLINE = (12, 14, 22)
TEAL = (70, 225, 190)

# 6x7 bold glyphs, two-pixel strokes
GLYPHS = {
    "A": [".####.", "##..##", "##..##", "######", "##..##", "##..##", "##..##"],
    "B": ["#####.", "##..##", "##..##", "#####.", "##..##", "##..##", "#####."],
    "C": [".#####", "##....", "##....", "##....", "##....", "##....", ".#####"],
    "E": ["######", "##....", "##....", "#####.", "##....", "##....", "######"],
    "G": [".#####", "##....", "##....", "##.###", "##..##", "##..##", ".#####"],
    "I": ["######", "..##..", "..##..", "..##..", "..##..", "..##..", "######"],
    "L": ["##....", "##....", "##....", "##....", "##....", "##....", "######"],
    "N": ["##..##", "###.##", "######", "##.###", "##..##", "##..##", "##..##"],
    "O": [".####.", "##..##", "##..##", "##..##", "##..##", "##..##", ".####."],
    "P": ["#####.", "##..##", "##..##", "#####.", "##....", "##....", "##...."],
    "S": [".#####", "##....", "##....", ".####.", "....##", "....##", "#####."],
    "T": ["######", "..##..", "..##..", "..##..", "..##..", "..##..", "..##.."],
    "Y": ["##..##", "##..##", "##..##", ".####.", "..##..", "..##..", "..##.."],
    "0": [".####.", "##..##", "##..##", "##..##", "##..##", "##..##", ".####."],
    "1": ["..##..", ".###..", "..##..", "..##..", "..##..", "..##..", "######"],
    "2": ["#####.", "....##", "....##", ".####.", "##....", "##....", "######"],
    "3": ["#####.", "....##", "....##", ".####.", "....##", "....##", "#####."],
    "4": ["##..##", "##..##", "##..##", "######", "....##", "....##", "....##"],
    "5": ["######", "##....", "##....", "#####.", "....##", "....##", "#####."],
    "6": [".#####", "##....", "##....", "#####.", "##..##", "##..##", ".####."],
    "7": ["######", "....##", "...##.", "..##..", "..##..", "..##..", "..##.."],
    "8": [".####.", "##..##", "##..##", ".####.", "##..##", "##..##", ".####."],
    "9": [".####.", "##..##", "##..##", ".#####", "....##", "....##", "#####."],
    ".": ["..", "..", "..", "..", "..", "##", "##"],
    " ": ["...", "...", "...", "...", "...", "...", "..."],
}


def read_version():
    """The version from the command line, otherwise from the client manifest; digits and dots only."""
    if ARGS:
        version = ARGS[0]
    else:
        with open(MANIFEST, encoding="utf-8") as f:
            version = json.load(f)["version"]
    if not version or any(ch not in "0123456789." for ch in version):
        sys.exit(f"Can't draw version {version!r}: only digits and dots have glyphs")
    return version


def text_mask(text):
    """Glyph cells for a line of text, one cell apart, as a set of (x, y)."""
    cells, x = set(), 0
    for ch in text:
        g = GLYPHS[ch]
        for y, row in enumerate(g):
            for gx, c in enumerate(row):
                if c == "#":
                    cells.add((x + gx, y))
        x += len(g[0]) + 1
    return cells, x - 1, 7


def draw_text(img, text, cell, centre_x, top, fill, alpha=1.0, glow=None):
    """Pixel letters with a one-cell dark outline and a drop shadow; alpha fades the whole line."""
    cells, w, h = text_mask(text)
    outline = {(x + dx, y + dy) for x, y in cells for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
    shadow = {(x + 1, y + 1) for x, y in outline}
    left = centre_x - (w * cell) // 2
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    def paint(points, colour, a):
        for x, y in points:
            x0, y0 = left + x * cell, top + y * cell
            d.rectangle([x0, y0, x0 + cell - 1, y0 + cell - 1], fill=colour + (int(255 * a),))

    paint(shadow - outline, (0, 0, 0), 0.55 * alpha)
    paint(outline, OUTLINE, alpha)
    paint(cells, fill, alpha)
    if glow:
        halo = Image.new("RGBA", img.size, (0, 0, 0, 0))
        hd = ImageDraw.Draw(halo)
        for x, y in cells:
            x0, y0 = left + x * cell, top + y * cell
            hd.rectangle([x0, y0, x0 + cell - 1, y0 + cell - 1], fill=glow + (int(180 * alpha),))
        halo = halo.filter(ImageFilter.GaussianBlur(cell * 2.2))
        img.alpha_composite(halo)
    img.alpha_composite(layer)
    return top + (h + 1) * cell


def square_crop(im):
    w, h = im.size
    s = min(w, h)
    return im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))


def smooth(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def main():
    version = read_version()
    subtitle = "BETA " + version
    out = os.path.join(HERE, "out", version)
    os.makedirs(out, exist_ok=True)
    base = square_crop(Image.open(SOURCE).convert("RGB")).resize((WORK, WORK), Image.LANCZOS)
    base = ImageEnhance.Color(ImageEnhance.Contrast(base).enhance(1.18)).enhance(1.25)

    # The towers' light strips: the brightest parts of the shot
    lum = base.convert("L")
    lights = lum.point(lambda v: 0 if v < 175 else min(255, (v - 175) * 4)).filter(ImageFilter.GaussianBlur(3))

    # Lights-off version: strips dimmed to the night around them, the whole scene a little darker
    r, g, b = base.split()
    dark_scene = Image.merge("RGB", (r.point(lambda v: int(v * 0.24)), g.point(lambda v: int(v * 0.28)), b.point(lambda v: int(v * 0.40))))
    # Bloom: the strips' own colour, spread wide
    glow_src = Image.composite(base, Image.new("RGB", (WORK, WORK), (0, 0, 0)), lights)
    vignette = Image.radial_gradient("L").resize((WORK, WORK)).point(lambda v: int(255 - v * 0.75))

    rng = random.Random(7)
    flicker = [rng.random() for _ in range(FRAMES)]
    sub_cell = min(10, 640 // text_mask(subtitle)[1])

    def render(i, shown=None):
        """Frame i of the loop at output size; shown overrides how visible the subtitle is."""
        t = i / FRAMES * SECONDS

        # Light level per row: 1 = on, 0 = off. Off sweeps from the ground up (1.4 s to 2.3 s),
        # back on from the top down (4.3 s to 5.0 s), with flicker at the edges.
        off_front = smooth((t - 1.4) / 0.9)
        on_front = smooth((t - 4.3) / 0.7)
        row_level = []
        for y in range(WORK):
            up = 1 - y / WORK
            level = 0.0 if up < off_front * 1.15 else 1.0
            if on_front > 0 and (1 - up) < on_front * 1.15:
                level = 1.0
            row_level.append(level)
        flick = 1.0
        if 1.1 < t < 1.5 or 4.1 < t < 4.4:
            flick = 0.35 if flicker[i] < 0.5 else 1.0
        rows = Image.new("L", (1, WORK))
        rows.putdata([int(255 * v * flick) for v in row_level])
        rows = rows.resize((WORK, WORK))

        # Strips follow their row; everything else dims with the city as a whole
        lit_mask = ImageChops.multiply(lights, rows)
        darkness = off_front * (1 - on_front)
        ambient = Image.new("L", (WORK, WORK), int(255 * (1 - darkness)))
        frame = Image.composite(base, dark_scene, ImageChops.lighter(lit_mask, ambient))
        bloom = Image.composite(glow_src, Image.new("RGB", (WORK, WORK), (0, 0, 0)), lit_mask).filter(ImageFilter.GaussianBlur(26))
        frame = ImageChops.add(frame, Image.eval(bloom, lambda v: int(v * 1.5)))

        # Slow push-in and out, so the loop joins
        z = 1.0 + 0.05 * (1 - math.cos(2 * math.pi * i / FRAMES)) / 2
        s = int(WORK / z)
        o = (WORK - s) // 2
        frame = frame.crop((o, o, o + s, o + s)).resize((WORK, WORK), Image.LANCZOS)

        frame = frame.filter(ImageFilter.GaussianBlur(5))
        frame = Image.composite(frame, Image.new("RGB", (WORK, WORK), (0, 0, 0)), vignette)
        frame = frame.convert("RGBA")

        # Dark band behind the title for contrast
        band = Image.new("L", (WORK, WORK), 0)
        bd = ImageDraw.Draw(band)
        bd.rectangle([0, 210, WORK, 470], fill=120)
        band = band.filter(ImageFilter.GaussianBlur(40))
        frame = Image.composite(Image.new("RGBA", (WORK, WORK), (0, 0, 0, 255)), frame, band)

        y = draw_text(frame, TITLE[0], 10, WORK // 2, 230, WHITE)
        draw_text(frame, TITLE[1], 14, WORK // 2, y + 6, WHITE)

        sub = smooth((t - 2.3) / 0.6) * (1 - smooth((t - 4.25) / 0.35)) if shown is None else shown
        if sub > 0.01:
            draw_text(frame, subtitle, sub_cell, WORK // 2, 610, TEAL, alpha=sub, glow=TEAL)

        return frame.convert("RGB").resize((SIZE, SIZE), Image.LANCZOS)

    frames = [render(i) for i in range(FRAMES)]
    static = render(0, shown=1.0)

    frames[0].save(os.path.join(out, "still.png"))
    frames[int(3.4 * FPS)].save(os.path.join(out, "still_dark.png"))
    static.save(os.path.join(out, "static.png"))
    static.resize((64, 64), Image.LANCZOS).save(os.path.join(out, "server-icon.png"))
    sheet = Image.new("RGB", (SIZE * 2, SIZE))
    for k, sec in enumerate((0.5, 1.3, 1.8, 2.2, 3.0, 4.0, 4.5, 4.9)):
        sheet.paste(frames[int(sec * FPS)].resize((SIZE // 2, SIZE // 2)), ((k % 4) * SIZE // 2, (k // 4) * SIZE // 2))
    sheet.save(os.path.join(out, "sheet.png"))
    static.resize((64, 64), Image.LANCZOS).resize((256, 256), Image.NEAREST).save(os.path.join(out, "preview_64.png"))
    frames[0].save(os.path.join(out, "icon.webp"), save_all=True, append_images=frames[1:],
                   duration=int(1000 / FPS), loop=0, quality=82, method=6)
    gif = frames[::2]
    gif[0].save(os.path.join(out, "icon.gif"), save_all=True, append_images=gif[1:],
                duration=int(2000 / FPS), loop=0, optimize=True)
    for f in ("icon.webp", "icon.gif"):
        print(f, os.path.getsize(os.path.join(out, f)) // 1024, "KB,", FRAMES, "frames")

    if PLACE:
        os.makedirs(os.path.join(ROOT, "CLIENT", "profileImage"), exist_ok=True)
        for name, target in (("icon.webp", "CLIENT/profileImage/icon.webp"), ("static.png", "CLIENT/profileImage/icon.png"),
                             ("server-icon.png", "SERVER/server-icon.png")):
            shutil.copyfile(os.path.join(out, name), os.path.join(ROOT, target))
            print("placed", target)


if __name__ == "__main__":
    main()
