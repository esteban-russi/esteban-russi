"""Generate the animated pixel-art banner for the GitHub profile README.

GitHub renders README images as static <img> tags with scripts stripped, but
CSS keyframes and SMIL animations inside an SVG still play. This script draws
each letter from a hand-made 5x7 bitmap font as individual <rect> "pixels",
so every pixel can be animated on its own.

Usage:  python scripts/make_banner.py   ->  writes assets/retro-banner.svg
"""

from pathlib import Path
import random

TITLE = "ESTEBAN RUSSI"
SUBTITLE = "> AI & PRODUCT ENGINEER - BUILDING..."

W, H = 900, 230
BG = "#0d0221"

# 5x7 bitmap font: each glyph is 7 rows of 5 bits.
FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "J": ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "10001", "11001", "10101", "10011", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    " ": ["00000"] * 7,
    "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    ",": ["00000", "00000", "00000", "00000", "01100", "00100", "01000"],
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    "&": ["01100", "10010", "10100", "01000", "10101", "10010", "01101"],
    ">": ["10000", "01000", "00100", "00010", "00100", "01000", "10000"],
    "'": ["00100", "00100", "01000", "00000", "00000", "00000", "00000"],
}


def pixels(text):
    """Yield (col, row) for every lit pixel; glyphs are 5 wide + 1 gap."""
    for i, ch in enumerate(text.upper()):
        for r, line in enumerate(FONT[ch]):
            for c, bit in enumerate(line):
                if bit == "1":
                    yield i * 6 + c, r


def text_width(text, px):
    return (len(text) * 6 - 1) * px


def build():
    rnd = random.Random(7)
    out = []
    a = out.append

    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
      f'viewBox="0 0 {W} {H}" role="img" aria-label="{TITLE}">')
    a(f"<title>{TITLE}</title>")
    a("""<defs>
  <linearGradient id="sun" x1="0" y1="0" x2="900" y2="0" gradientUnits="userSpaceOnUse" spreadMethod="repeat">
    <stop offset="0" stop-color="#ff2a6d"/>
    <stop offset="0.25" stop-color="#ffb800"/>
    <stop offset="0.5" stop-color="#05d9e8"/>
    <stop offset="0.75" stop-color="#d16bff"/>
    <stop offset="1" stop-color="#ff2a6d"/>
    <animateTransform attributeName="gradientTransform" type="translate"
      values="-900 0; 0 0" dur="6s" repeatCount="indefinite"/>
  </linearGradient>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="2" fill="#000" opacity="0.28"/>
  </pattern>
  <linearGradient id="grid" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ff2a6d" stop-opacity="0"/>
    <stop offset="1" stop-color="#ff2a6d" stop-opacity="0.55"/>
  </linearGradient>
  <filter id="glow" x="-10%" y="-30%" width="120%" height="160%">
    <feGaussianBlur stdDeviation="3" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>""")

    a("""<style>
  .px  { opacity: 0; animation: drop .55s cubic-bezier(.2,1.6,.4,1) forwards; }
  .sh  { opacity: 0; animation: fade .3s steps(2) forwards; }
  .star{ animation: twinkle 2.4s steps(3) infinite; }
  .cur { animation: blink 1s steps(1) infinite; }
  .glitch { animation: glitch 7s steps(1) infinite 3.5s; }
  @keyframes drop { 0% { opacity: 0; transform: translateY(-60px); }
                    100% { opacity: 1; transform: translateY(0); } }
  @keyframes fade { to { opacity: 1; } }
  @keyframes twinkle { 0%,100% { opacity: .2; } 50% { opacity: 1; } }
  @keyframes blink { 0%,50% { opacity: 1; } 51%,100% { opacity: 0; } }
  @keyframes glitch {
    0%   { transform: translate(0,0); }
    92%  { transform: translate(4px,0); }
    93%  { transform: translate(-6px,0); }
    94%  { transform: translate(3px,0); }
    95%  { transform: translate(0,0); }
  }
  @media (prefers-reduced-motion: reduce) {
    .px, .sh { animation: none; opacity: 1; }
    .star, .cur, .glitch { animation: none; }
  }
</style>""")

    # Background, retro horizon grid and stars.
    a(f'<rect width="{W}" height="{H}" rx="10" fill="{BG}"/>')
    a('<g stroke="url(#grid)" stroke-width="1">')
    horizon = 150
    for i in range(-14, 15):
        a(f'<line x1="{W/2 + i*12:.0f}" y1="{horizon}" x2="{W/2 + i*90:.0f}" y2="{H}"/>')
    for y in (154, 160, 168, 179, 194, 213):
        a(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>')
    a("</g>")
    a('<g fill="#fff">')
    for _ in range(45):
        x, y = rnd.randint(8, W - 8), rnd.randint(8, horizon - 6)
        s = rnd.choice((2, 2, 3))
        d = rnd.uniform(0, 2.4)
        a(f'<rect class="star" x="{x}" y="{y}" width="{s}" height="{s}" '
          f'style="animation-delay:{d:.2f}s"/>')
    a("</g>")

    # Title: shadow layer + gradient pixel layer that drops in column by column.
    px = 10
    tx = (W - text_width(TITLE, px)) // 2
    ty = 38
    pts = list(pixels(TITLE))
    ncols = len(TITLE) * 6

    a('<g class="glitch">')
    a('<g fill="#7a04eb">')
    for c, r in pts:
        d = 0.9 + c / ncols * 1.6
        a(f'<rect class="sh" x="{tx + c*px + 5}" y="{ty + r*px + 5}" width="{px}" '
          f'height="{px}" style="animation-delay:{d:.2f}s"/>')
    a("</g>")
    a('<g fill="url(#sun)" filter="url(#glow)">')
    for c, r in pts:
        d = c / ncols * 1.6 + rnd.uniform(0, 0.25)
        a(f'<rect class="px" x="{tx + c*px}" y="{ty + r*px}" width="{px - 1}" '
          f'height="{px - 1}" style="animation-delay:{d:.2f}s"/>')
    a("</g></g>")

    # Subtitle: typed out via a stepping clip rectangle, then a blinking cursor.
    sp = 3
    sw = text_width(SUBTITLE, sp)
    sx = (W - sw) // 2
    sy = 160
    chars = len(SUBTITLE)
    start, dur = 2.4, chars * 0.06
    a(f'<clipPath id="type"><rect x="{sx}" y="{sy - 2}" height="{7*sp + 4}" width="0">'
      f'<animate attributeName="width" from="0" to="{sw + 4}" begin="{start}s" '
      f'dur="{dur:.2f}s" calcMode="discrete" values="'
      + ";".join(str(round((sw + 4) * k / chars)) for k in range(chars + 1))
      + '" fill="freeze"/></rect></clipPath>')
    a(f'<g clip-path="url(#type)" fill="#05d9e8">')
    a("<path d=\"" + "".join(
        f"M{sx + c*sp},{sy + r*sp}h{sp}v{sp}h-{sp}z" for c, r in pixels(SUBTITLE)
    ) + '"/>')
    a("</g>")
    a(f'<g opacity="0"><set attributeName="opacity" to="1" begin="{start:.2f}s" fill="freeze"/>'
      f'<rect class="cur" x="{sx + sw + 6}" y="{sy}" width="{2*sp}" height="{7*sp}" '
      f'fill="#05d9e8"/></g>')

    # CRT scanlines on top.
    a(f'<rect width="{W}" height="{H}" rx="10" fill="url(#scan)" pointer-events="none"/>')
    a("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    dest = Path(__file__).resolve().parent.parent / "assets" / "retro-banner.svg"
    dest.write_text(build(), encoding="utf-8")
    print(f"wrote {dest} ({dest.stat().st_size // 1024} KB)")
