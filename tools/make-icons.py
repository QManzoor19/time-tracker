#!/usr/bin/env python3
"""Regenerate the app icons.

The dial is one whole day: each arc is a category's share of 24 hours, drawn in
the app's own categorical palette and in its slot order, so neighbouring arcs are
the pairs that were validated as distinguishable under colour-vision deficiency.

Writes .html wrappers next to the PNGs and rasterises them with headless Chrome —
no image libraries required. Run from the repo root:

    python3 tools/make-icons.py
"""
import io, math, os, subprocess, sys

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = os.path.dirname(os.path.abspath(__file__)) + "/.."

SEG = [
    ("#2a78d6", 8.0),   # sleep
    ("#eb6834", 4.5),   # deep work
    ("#1baf7a", 1.0),   # study
    ("#eda100", 1.5),   # admin
    ("#e87ba4", 4.0),   # health
    ("#008300", 1.5),   # people
    ("#4a3aa7", 3.0),   # leisure
    ("#e34948", 0.5),   # drift
]
BG = "#141413"
assert abs(sum(h for _, h in SEG) - 24.0) < 1e-9, "the dial must be exactly one day"


def pt(cx, cy, r, deg):
    a = math.radians(deg - 90)           # 0 degrees = 12 o'clock
    return cx + r * math.cos(a), cy + r * math.sin(a)


def donut(cx, cy, ro, ri, a0, a1):
    large = 1 if (a1 - a0) % 360 > 180 else 0
    x0, y0 = pt(cx, cy, ro, a0); x1, y1 = pt(cx, cy, ro, a1)
    x2, y2 = pt(cx, cy, ri, a1); x3, y3 = pt(cx, cy, ri, a0)
    return ("M%.2f %.2f A%.2f %.2f 0 %d 1 %.2f %.2f L%.2f %.2f A%.2f %.2f 0 %d 0 %.2f %.2f Z"
            % (x0, y0, ro, ro, large, x1, y1, x2, y2, ri, ri, large, x3, y3))


def svg(size, ring_frac, gap_deg, hands=True):
    S = 512.0
    c = S / 2
    ro = S * ring_frac / 2
    ri = ro * 0.60
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="%d" height="%d">' % (size, size),
         '<rect width="512" height="512" fill="%s"/>' % BG]
    ang = 0.0
    for col, hrs in SEG:
        span = hrs * 15.0                # 24h across 360 degrees
        a0, a1 = ang + gap_deg / 2, ang + span - gap_deg / 2
        if a1 > a0:
            p.append('<path d="%s" fill="%s"/>' % (donut(c, c, ro, ri, a0, a1), col))
        ang += span
    if hands:
        hx, hy = pt(c, c, ri * 0.62, 300)
        mx, my = pt(c, c, ri * 0.86, 55)
        for (x, y, w) in ((hx, hy, 15), (mx, my, 11)):
            p.append('<line x1="%.1f" y1="%.1f" x2="%.2f" y2="%.2f" stroke="#fcfcfb" '
                     'stroke-width="%d" stroke-linecap="round"/>' % (c, c, x, y, w))
        p.append('<circle cx="%.1f" cy="%.1f" r="10" fill="%s"/>' % (c, c, BG))
        p.append('<circle cx="%.1f" cy="%.1f" r="5.5" fill="#fcfcfb"/>' % (c, c))
    p.append("</svg>")
    return "\n".join(p)


SPECS = [
    ("icon-512.png",         512, 0.78, 2.2, True),
    ("icon-192.png",         192, 0.78, 2.2, True),
    ("apple-touch-icon.png", 180, 0.78, 2.2, True),
    ("icon-maskable.png",    512, 0.58, 2.2, True),   # Android crops to ~80%
    ("favicon.png",           64, 0.86, 3.0, False),  # hands vanish at this size
]

for name, size, frac, gap, hands in SPECS:
    body = svg(size, frac, gap, hands)
    tmp = os.path.join(OUT, name + ".html")
    io.open(tmp, "w", encoding="utf-8").write(
        '<meta charset="utf-8"><style>html,body{margin:0;padding:0;background:%s}'
        'svg{display:block}</style>%s' % (BG, body))
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--force-device-scale-factor=1",
                    "--hide-scrollbars", "--window-size=%d,%d" % (size, size),
                    "--screenshot=" + os.path.join(OUT, name), "file://" + tmp],
                   check=True, capture_output=True)
    os.remove(tmp)
    print("wrote", name, "%dx%d" % (size, size))

io.open(os.path.join(OUT, "icon.svg"), "w", encoding="utf-8").write(svg(512, 0.78, 2.2, True))
print("wrote icon.svg")
