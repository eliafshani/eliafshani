"""Draws the animated SVG cards for the GitHub profile README.
STATIC=1 python3 scripts/render_cards.py  -> final frame, no animation (for screenshots)."""
import math, os, pathlib

STATIC = os.environ.get("STATIC") == "1"
OUT = pathlib.Path(__file__).resolve().parent.parent / "cards"
OUT.mkdir(exist_ok=True)

NAVY, NAVY2, CREAM, BEIGE = "#1b2240", "#232c52", "#EEE8DF", "#C4BCB0"
MUTED = "#9a9fb5"
FONT = "ui-sans-serif,-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"

BASE_CSS = f"""
text{{font-family:{FONT}}}
@keyframes rise{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:none}}}}
@keyframes swing{{0%{{opacity:0;transform:translateY(34px) rotate(-3deg)}}60%{{opacity:1;transform:translateY(-5px) rotate(.6deg)}}100%{{opacity:1;transform:none}}}}
@keyframes draw{{from{{stroke-dashoffset:1}}to{{stroke-dashoffset:0}}}}
@keyframes pop{{from{{opacity:0;transform:scale(.85)}}to{{opacity:1;transform:none}}}}
@keyframes flow{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:-24}}}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
@keyframes nudge{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(3px,-3px)}}}}
.fb{{transform-box:fill-box;transform-origin:center}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""

def svg(w, h, body, extra_css=""):
    css = "" if STATIC else BASE_CSS + extra_css
    if STATIC:
        css = f"text{{font-family:{FONT}}}.fb{{transform-box:fill-box;transform-origin:center}}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{{label}}"><style>{css}</style>{body}</svg>')

def anim(cls, delay, dur=0.7, ease="cubic-bezier(.16,1,.3,1)"):
    if STATIC:
        return ""
    return f'style="animation:{cls} {dur}s {ease} {delay}s both"'

def write(name, label, w, h, body, css=""):
    (OUT / name).write_text(svg(w, h, body, css).replace("{label}", label))

# ---------- hero ----------
def hero():
    w, h = 960, 300
    dots = "".join(
        f'<circle cx="{x}" cy="{y}" r="1.4" fill="{BEIGE}" opacity=".13"/>'
        for x in range(24, w, 32) for y in range(24, h, 32))
    shine = "" if STATIC else (
        '<animateTransform attributeName="gradientTransform" type="translate" '
        'from="-1.2 0" to="1.6 0" dur="3.2s" begin="1.6s;s.end+4s" id="s" fill="freeze"/>')
    chips = ["Founder & CEO, FlowState", "Harvard CS50x", "Los Angeles, CA"]
    cx, chip_svg = 56, ""
    for i, c in enumerate(chips):
        cw = 14 * 0 + len(c) * 8.4 + 34
        chip_svg += (f'<g {anim("rise", 1.0 + i*0.12, .6)}><rect x="{cx}" y="214" width="{cw:.0f}" height="34" rx="17" '
                     f'fill="none" stroke="{BEIGE}" stroke-opacity=".45"/>'
                     f'<text x="{cx+17}" y="236" font-size="14" fill="{CREAM}">{c.replace("&","&amp;")}</text></g>')
        cx += cw + 12
    body = f"""
<rect width="{w}" height="{h}" rx="16" fill="{NAVY}"/>{dots}
<defs><linearGradient id="g" x1="0" x2="1" gradientUnits="objectBoundingBox">
<stop offset="0" stop-color="{BEIGE}"/><stop offset=".45" stop-color="#ffffff"/><stop offset=".55" stop-color="#ffffff"/><stop offset="1" stop-color="{BEIGE}"/>
{shine.replace('id="s"','id="s"')}</linearGradient></defs>
<g {anim("rise",0.1)}><text x="56" y="96" font-size="64" font-weight="900" letter-spacing="-3" fill="{CREAM}">Eli</text></g>
<g {anim("rise",0.25)}><text x="56" y="164" font-size="64" font-weight="900" letter-spacing="-3" fill="url(#g)">Afshani</text></g>
<g {anim("rise",0.6,.6)}><text x="56" y="196" font-size="17" fill="{MUTED}">I build apps people use. Student builder in Los Angeles.</text></g>
{chip_svg}
<g {anim("pop",0.4)} class="fb"><text x="{w-120}" y="92" font-size="64" font-weight="900" letter-spacing="-5" fill="{CREAM}">E<tspan fill="{BEIGE}" dx="-6">A</tspan></text></g>
"""
    write("hero.svg", "Eli Afshani. I build apps people use. Student builder in Los Angeles.", w, h, body)

# ---------- hub ----------
def hub():
    w, h = 960, 380
    cx, cy = w / 2, h / 2
    items = ["Peak", "Afshani Home", "Jarvis", "Ensemble", "FlowState"]
    pts = []
    for i, name in enumerate(items):
        a = math.radians(-90 + 360 / len(items) * i)
        pts.append((name, cx + 330 * math.cos(a) * (1 if i not in (0,) else 0), cy + 135 * math.sin(a)))
    pts[0] = ("Peak", cx, cy - 135)
    parts = [f'<rect width="{w}" height="{h}" rx="16" fill="{NAVY}"/>',
             f'<text x="40" y="52" font-size="13" letter-spacing="3" fill="{MUTED}">WHAT I RUN</text>']
    for i, (name, x, y) in enumerate(pts):
        d = 0.9 + i * 0.1
        line = (f'<line x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}" stroke="{BEIGE}" stroke-opacity=".5" stroke-width="1.5" pathLength="1" '
                + ('' if STATIC else f'stroke-dasharray="1" style="animation:draw .8s ease {d}s both" ') + '/>')
        flow = ('' if STATIC else
                f'<line x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}" stroke="{CREAM}" stroke-width="2" stroke-linecap="round" '
                f'stroke-dasharray="3 21" style="animation:flow 1.6s linear {d+0.9}s infinite both;opacity:.9"/>')
        parts.append(line + flow)
    for i, (name, x, y) in enumerate(pts):
        d = 1.3 + i * 0.1
        pw = len(name) * 9.5 + 40
        parts.append(f'<g {anim("pop", d, .5)} class="fb"><rect x="{x-pw/2:.0f}" y="{y-20:.0f}" width="{pw:.0f}" height="40" rx="12" fill="{NAVY2}" stroke="{BEIGE}" stroke-opacity=".6"/>'
                     f'<text x="{x:.0f}" y="{y+6:.0f}" text-anchor="middle" font-size="16" font-weight="600" fill="{CREAM}">{name}</text></g>')
    parts.append(f'<g {anim("pop", 0.6, .5)} class="fb"><rect x="{cx-52}" y="{cy-24}" width="104" height="48" rx="14" fill="{CREAM}"/>'
                 f'<text x="{cx}" y="{cy+7}" text-anchor="middle" font-size="19" font-weight="900" letter-spacing="-.5" fill="{NAVY}">Eli</text></g>')
    write("hub.svg", "Eli connects to five things he builds: Peak, Afshani Home, Jarvis, Ensemble and FlowState.", w, h, "".join(parts))

# ---------- tiles ----------
def tile(name, kicker, big, label, delay):
    w, h = 310, 210
    if isinstance(big, int):
        if STATIC:
            number = f'<text x="28" y="128" font-size="84" font-weight="900" letter-spacing="-4" fill="{CREAM}">{big}</text>'
        else:
            number = ""
            for k in range(big + 1):
                begin = f"{delay+0.5+k*0.14:.2f}s"
                last = k == big
                number += (f'<text x="28" y="128" font-size="84" font-weight="900" letter-spacing="-4" fill="{CREAM}" opacity="0">'
                           f'<set attributeName="opacity" to="1" begin="{begin}" '
                           + ('fill="freeze"' if last else 'dur="0.14s"') + '/>' + str(k) + '</text>')
    else:
        number = f'<text x="28" y="116" font-size="52" font-weight="900" letter-spacing="-2.5" fill="{CREAM}">{big}</text>'
    ring = '' if STATIC else (f'<circle cx="{w-34}" cy="34" r="6" fill="none" stroke="{BEIGE}" stroke-width="2" '
                              f'style="transform-box:fill-box;transform-origin:center;animation:pop 1.8s ease-out {delay+0.8}s infinite both"/>')
    body = f"""
<g {anim("swing", delay, .9)} class="fb">
<rect width="{w}" height="{h}" rx="16" fill="{NAVY2}" stroke="{BEIGE}" stroke-opacity=".3"/>
<text x="28" y="44" font-size="12" letter-spacing="3" fill="{MUTED}">{kicker}</text>
{number}
<text x="28" y="164" font-size="16" fill="{BEIGE}">{label}</text>
<circle cx="{w-34}" cy="34" r="5" fill="{BEIGE}"/>{ring}
<g style="{'' if STATIC else 'animation:nudge 2.4s ease-in-out infinite'}"><path d="M{w-52} {h-34} L{w-30} {h-56} M{w-46} {h-56} H{w-30} V{h-40}" stroke="{CREAM}" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
</g>"""
    write(name, f"{kicker}: {big} {label}", w, h, body)

def main():
    hero(); hub()
    tile("tile-apps.svg", "APPS", 4, "apps I build for myself", 1.6)
    tile("tile-credentials.svg", "CREDENTIALS", 5, "certificates and milestones", 1.75)
    tile("tile-writing.svg", "WRITING", "Notes", "on what I build and learn", 1.9)

main()
