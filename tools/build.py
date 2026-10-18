# Profil README'sindeki SVG'leri üretir: hareketli başlık, 6 proje kartı, parça listesi.
# Her görsel açık ve koyu tema için ayrı yazılır (README'de <picture> ile GitHub temasına göre seçilir).
# GitHub, <img> ile açılan SVG'ye dış font yüklemediği için Barlow Condensed alt kümesi SVG'ye gömülür.
# Kullanım: python tools/build.py   (fonttools + brotli gerekir)
import base64, io, math, pathlib, random, re
from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent / "assets"
FONT = "font-family=\"'Barlow Condensed','Arial Narrow',sans-serif\""

THEMES = {
    "light": ".bg{fill:#FCFCFA}.ink{fill:#1C1C1C}.mute{fill:#6B6B68}.s{stroke:#1C1C1C;fill:none}"
             ".l{stroke:rgba(28,28,28,.22);fill:none}.d{stroke:#2E7556;fill:none}.df{fill:#2E7556}"
             ".a{stroke:#C8102E;fill:none}.af{fill:#C8102E}.soft{fill:rgba(46,117,86,.12)}",
    "dark": ".bg{fill:#0D1117}.ink{fill:#ECEAE4}.mute{fill:#9C9993}.s{stroke:#ECEAE4;fill:none}"
            ".l{stroke:rgba(236,234,228,.22);fill:none}.d{stroke:#86C9AC;fill:none}.df{fill:#86C9AC}"
            ".a{stroke:#F0707A;fill:none}.af{fill:#F0707A}.soft{fill:rgba(134,201,172,.14)}",
}
theme = "light"     # üretim döngüsünde değiştirilir
font_css = ""       # ilk geçişte boş; karakterler toplandıktan sonra doldurulur


def svg(w, h, body, extra_css=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" {FONT}>'
            f"<style>{font_css}{THEMES[theme]}{extra_css}</style>"
            f'<rect class="bg" width="{w}" height="{h}"/>' + body + "</svg>")


def embed_fonts(text):
    """Yalnız kullanılan karakterleri içeren woff2 alt kümelerini @font-face olarak döndürür."""
    css = ""
    for weight, name in ((400, "Regular"), (600, "SemiBold")):
        font = TTFont(ROOT / "fonts" / f"BarlowCondensed-{name}.ttf")
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["kern", "liga"]
        sub = subset.Subsetter(opts)
        sub.populate(text=text)
        sub.subset(font)
        buf = io.BytesIO()
        font.flavor = "woff2"
        font.save(buf)
        b64 = base64.b64encode(buf.getvalue()).decode()
        css += (f"@font-face{{font-family:'Barlow Condensed';font-weight:{weight};"
                f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
    return css


# ---------- başlık: kontrol grafiği kendini çizer, sonda kural-1 ihlali kırmızı yanar ----------
def header():
    random.seed(7)
    pts, x = [], 0
    for i in range(25):
        y = 46 + random.uniform(-14, 14)
        pts.append((i * 23, y))
    pts[-2] = (pts[-2][0], 4)  # ÜKS dışı nokta
    poly = " ".join(f"{a:.0f},{b:.1f}" for a, b in pts)
    length = sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
    ox, oy = pts[-2]
    css = (f".draw{{stroke-dasharray:{length:.0f};stroke-dashoffset:{length:.0f};animation:dr 3.2s ease-out .4s forwards}}"
           "@keyframes dr{to{stroke-dashoffset:0}}"
           ".pop{opacity:0;animation:pp .5s 3.4s forwards}.blink{opacity:0;animation:pp .5s 3.4s forwards,bl 1.6s 3.9s infinite}"
           "@keyframes pp{to{opacity:1}}@keyframes bl{50%{opacity:.25}}"
           ".typ{opacity:0;animation:pp .8s .1s forwards}")
    zones = "".join(f'<text x="{101+i*159.6:.0f}" y="17">{i+1}</text>' for i in range(6))
    body = f'''
<rect class="l" x="6" y="6" width="988" height="288"/><rect class="s" x="22" y="22" width="956" height="256" stroke-width="1.6"/>
<g class="mute" font-size="11" text-anchor="middle">{zones}<text x="14" y="69">A</text><text x="14" y="154">B</text><text x="14" y="239">C</text></g>
<path class="l" d="M181 6v16M340 6v16M500 6v16M660 6v16M820 6v16M6 107h16M6 192h16"/>
<g class="typ"><text class="ink" x="52" y="98" font-size="58" font-weight="600" letter-spacing="1">İSMAİL BİLGEHAN KAZANCI</text>
<text class="mute" x="54" y="128" font-size="18" letter-spacing="1.4">MANUFACTURING ENGINEER  —  STATISTICAL PROCESS CONTROL · QUALITY · LINE BALANCING</text></g>
<g class="d"><path d="M52 146v12M612 146v12M52 152h560"/></g><path class="df" d="M52 152l9-3v6zM612 152l-9-3v6z"/>
<g transform="translate(52,176)">
 <path class="l" d="M0 10h560M0 82h560" stroke-dasharray="5 4"/><path class="l" d="M0 46h560"/>
 <g class="mute" font-size="11"><text x="566" y="14">UCL</text><text x="566" y="50">X̄</text><text x="566" y="86">LCL</text></g>
 <polyline class="d draw" stroke-width="1.6" points="{poly}"/>
 <g class="blink"><circle class="a" cx="{ox:.0f}" cy="{oy}" r="7" stroke-width="1.4"/><circle class="af" cx="{ox:.0f}" cy="{oy}" r="3"/></g>
 <text class="af pop" x="{ox-14:.0f}" y="{oy-6}" font-size="12" text-anchor="end">RULE 1</text>
</g>
<g transform="translate(680,170)">
 <rect class="s" width="298" height="108" stroke-width="1.2"/><path class="s" d="M0 36h298M0 72h298M96 0v108M200 72v36" stroke-width=".8"/>
 <g class="mute" font-size="10" letter-spacing="1.2"><text x="8" y="14">DRAWN BY</text><text x="8" y="50">LOCATION</text><text x="8" y="86">SHEET</text><text x="208" y="86">SCALE</text></g>
 <g class="ink" font-size="17"><text x="104" y="27">DailyDana</text><text x="104" y="63">Bursa, Türkiye</text><text x="104" y="99">github.com</text><text x="246" y="99">1 : 1</text></g>
</g>'''
    return svg(1000, 300, body, css)


# ---------- proje kartı iskeleti ----------
def card(no, title, line1, line2, drawing, dashed=False):
    frame = 'stroke-dasharray="6 4"' if dashed else ""
    body = f'''
<rect class="s" x="10" y="10" width="460" height="260" stroke-width="1.3" {frame}/>
<text class="mute" x="24" y="32" font-size="11" letter-spacing="1.5">DETAIL {no}</text>
<g transform="translate(24,44)">{drawing}</g>
<path class="s" d="M10 206h460M330 206v64" stroke-width=".9"/>
<text class="ink" x="24" y="232" font-size="22" font-weight="600">{title}</text>
<text class="mute" x="24" y="256" font-size="14">{line1}</text>
<text class="mute" x="340" y="224" font-size="10" letter-spacing="1.2">EVIDENCE</text>
<text class="ink" x="340" y="246" font-size="15">{line2}</text>'''
    return svg(480, 280, body)


def spc():
    # histogram + normal eğri + ASL/ÜSL
    mu, sd, bars = 216, 26, ""
    for i in range(-4, 4):
        x0 = mu + i * 14
        h = 140 * math.exp(-((x0 + 7 - mu) / sd) ** 2 / 2)
        bars += f'<rect class="soft" x="{x0}" y="{150-h:.0f}" width="13" height="{h:.0f}"/>'
    curve = " ".join(f"{x},{150-140*math.exp(-((x-mu)/sd)**2/2):.1f}" for x in range(130, 303, 3))
    return (bars + f'<polyline class="d" stroke-width="1.6" points="{curve}"/>'
            '<path class="l" d="M0 150h432"/><path class="a" d="M96 20v134M352 20v134" stroke-dasharray="4 3"/>'
            '<g class="mute" font-size="11"><text x="80" y="16">LSL</text><text x="340" y="16">USL</text></g>'
            '<text class="ink" x="364" y="80" font-size="20">Cpk 1.67</text><text class="mute" x="364" y="98" font-size="12">Gage R&amp;R</text>')


def hoffmann():
    stations = [[14, 22, 18, 30], [36, 28, 20], [26, 40, 12, 10], [44, 30, 14], [20, 24, 30, 12]]
    out = '<path class="a" d="M0 30h400" stroke-dasharray="5 3"/><text class="af" x="404" y="34" font-size="12">c</text>'
    for i, tasks in enumerate(stations):
        y, x = 150, 20 + i * 76
        for t in tasks:
            out += f'<rect class="soft" x="{x}" y="{y-t}" width="44" height="{t}"/><rect class="d" x="{x}" y="{y-t}" width="44" height="{t}" stroke-width=".8"/>'
            y -= t
        out += f'<text class="mute" x="{x+22}" y="146" font-size="0"/><text class="mute" x="{x+16}" y="166" font-size="12">S{i+1}</text>'
    return out + '<path class="l" d="M0 150h432"/>'


def cad():
    # basit kademeli mil, ön görünüş + ölçü
    return ('<path class="s" stroke-width="1.4" d="M40 60h80v-20h160v20h80v60h-80v20h-160v-20h-80z"/>'
            '<path class="l" d="M20 90h400" stroke-dasharray="14 3 3 3"/>'
            '<path class="d" d="M40 160v-12M360 160v-12M40 156h320"/><text class="df" x="186" y="152" font-size="12">320</text>'
            '<path class="d" d="M400 60h-14M400 120h-14M396 60v60"/><text class="df" x="404" y="94" font-size="12">Ø60</text>'
            '<text class="mute" x="0" y="16" font-size="11">SolidWorks · Siemens NX</text>')


def codec():
    random.seed(3)
    a = [(x, 24 + 0.16 * x + random.uniform(-5, 5)) for x in range(0, 401, 8)]
    b = [(x, y + (0 if x < 280 else (x - 280) * 0.35)) for x, y in a]
    pa = " ".join(f"{x},{y:.1f}" for x, y in a)
    pb = " ".join(f"{x},{y:.1f}" for x, y in b)
    fill = pa + " " + " ".join(f"{x},{y:.1f}" for x, y in reversed(b))
    return (f'<polygon class="soft" points="{fill}"/><polyline class="s" stroke-width="1" points="{pa}"/>'
            f'<polyline class="d" stroke-width="1.6" points="{pb}"/><path class="l" d="M0 150h432"/>'
            '<text class="mute" x="340" y="10" font-size="11">16 kHz cutoff</text><text class="mute" x="0" y="10" font-size="11">FLAC ↔ Opus</text>')


def aniflow():
    out = ""
    for i, x in enumerate([10, 150, 290]):
        dash = 'stroke-dasharray="5 3"' if i == 1 else ""
        cls = "d" if i == 1 else "s"
        out += f'<rect class="{cls}" x="{x}" y="20" width="120" height="90" stroke-width="1.2" {dash}/>'
        cx = x + 30 + i * 30
        out += f'<circle class="{"df" if i==1 else "ink"}" cx="{cx}" cy="65" r="12" opacity="{.6 if i==1 else 1}"/>'
    return (out + '<g class="mute" font-size="12"><text x="56" y="130">t</text><text x="186" y="130">t + ½</text><text x="334" y="130">t + 1</text></g>'
            '<text class="mute" x="0" y="150" font-size="11">RIFE in-between frames · Anime4K / FSRCNNX</text>')


def site():
    return ('<rect class="s" x="60" y="10" width="300" height="140" stroke-width="1.2"/>'
            '<rect class="l" x="70" y="20" width="280" height="120"/>'
            '<text class="ink" x="84" y="62" font-size="22" font-weight="600">İ. B. KAZANCI</text>'
            '<path class="d" d="M84 76h180"/><rect class="s" x="250" y="104" width="94" height="30" stroke-width=".8"/>'
            '<text class="mute" x="256" y="123" font-size="10">TITLE BLOCK</text>')


def bom():
    rows = [("1", "Python", "Language", "NumPy · SciPy · pandas"), ("2", "Streamlit", "Interface", "2 live demos"),
            ("3", "pytest + GitHub Actions", "Verification", "1,600+ tests, CI green"),
            ("4", "SolidWorks", "CAD", "assemblies + drawings"), ("5", "Siemens NX", "CAD", "assemblies"),
            ("6", "GLSL · Lua", "Image processing", "mpv shaders"), ("7", "HTML · CSS · JS", "Web", "dependency-free portfolio")]
    W, rh = 1000, 30
    H = 40 + rh * (len(rows) + 1) + 20
    xs = [22, 82, 412, 592, 978]
    head = ["ITEM", "PART", "CLASS", "NOTE"]
    out = f'<rect class="s" x="22" y="30" width="956" height="{rh*(len(rows)+1)}" stroke-width="1.3"/>'
    out += '<text class="mute" x="22" y="20" font-size="11" letter-spacing="1.5">BILL OF MATERIALS</text>'
    for x in xs[1:-1]:
        out += f'<path class="s" d="M{x} 30v{rh*(len(rows)+1)}" stroke-width=".8"/>'
    for j, h in enumerate(head):
        out += f'<text class="mute" x="{xs[j]+10}" y="{30+20}" font-size="12" letter-spacing="1.2">{h}</text>'
    for i, r in enumerate(rows):
        y = 30 + rh * (i + 1)
        out += f'<path class="l" d="M22 {y}h956"/>'
        for j, v in enumerate(r):
            cls = "ink" if j else "mute"
            out += f'<text class="{cls}" x="{xs[j]+10}" y="{y+20}" font-size="16">{v}</text>'
    return svg(W, H, out)


CARDS = [("A", "process-capability-analyzer", "SPC · Cp/Cpk · Gage R&amp;R · live demo", "890 tests", spc),
         ("B", "hoffmann-line-balancing", "SALBP-1 line balancing · 5 languages · live demo", "127 tests", hoffmann),
         ("C", "CAD work", "cannon models, assemblies, drawings", "drawing PDFs", cad),
         ("D", "CodecDelta", "lossy audio codec comparison tool", "617 tests", codec),
         ("E", "Aniflow", "anime upscaling + interpolation GUI", "v1.5", aniflow),
         ("F", "dailydana.github.io", "portfolio site · TR / EN", "no dependencies", site)]


def render_all():
    files = {"header": header(), "bom": bom()}
    for no, t, l1, l2, draw in CARDS:
        files[f"card-{no.lower()}"] = card(no, t, l1, l2, draw())
    return files


# 1. geçiş: fontsuz üret, <text> içindeki karakterleri topla; 2. geçiş: gömülü fontla her tema için yaz
chars = set()
for doc in render_all().values():
    for t in re.findall(r"<text[^>]*>([^<]*)</text>", doc):
        chars.update(t.replace("&amp;", "&"))
font_css = embed_fonts("".join(sorted(chars)))

OUT.mkdir(exist_ok=True)
for theme in THEMES:
    for name, doc in render_all().items():
        (OUT / f"{name}-{theme}.svg").write_text(doc, encoding="utf-8")
print(f"{len(list(OUT.glob('*.svg')))} SVG yazıldı -> {OUT}")
