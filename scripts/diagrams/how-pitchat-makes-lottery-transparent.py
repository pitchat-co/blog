"""Generate the SVG diagrams for how-pitchat-makes-lottery-transparent (zh + en).

Usage: python3 scripts/diagrams/how-pitchat-makes-lottery-transparent.py content/posts/how-pitchat-makes-lottery-transparent
Edit the text and layout here, then regenerate; don't edit the SVG files by hand.
"""
import sys
import unicodedata
from html import escape
from pathlib import Path

OUT = Path(sys.argv[1])

BLUE = "#2563EB"
NAVY = "#1E3A8A"
LIGHT = "#EEF3FE"
MID = "#C3D5FB"
LINE = "#D6E2FA"
INK = "#1F2937"
MUTED = "#5B6577"
RED = "#C2413B"
REDL = "#FDEDEC"

FONTS = {
    "zh": "'PingFang TC','Noto Sans TC','Microsoft JhengHei','Heiti TC',sans-serif",
    "en": "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif",
}
W = 600


def tw(s, size):
    """Rough text width: CJK glyphs are 1em, Latin about 0.55em."""
    w = 0.0
    for ch in s:
        if unicodedata.east_asian_width(ch) in "WF":
            w += 1.0
        elif ch in "il.,:;'|!·":
            w += 0.3
        elif ch.isupper() or ch in "mw#%":
            w += 0.7
        else:
            w += 0.6
    return w * size


def t(x, y, s, size=16, fill=INK, weight=400, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" '
            f'text-anchor="{anchor}">{escape(s)}</text>')


def rect(x, y, w, h, fill, stroke="none", rx=10, sw=1.5, dash=None, opacity=None):
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    extra += f' opacity="{opacity}"' if opacity else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"{extra}/>')


def arrow(x1, y1, x2, y2, color=BLUE):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2" '
            f'marker-end="url(#ah)"/>')


def check(cx, cy, r=14):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{BLUE}"/>'
            f'<path d="M{cx-6} {cy} l4.5 4.5 l8 -9" fill="none" stroke="#fff" stroke-width="2.6" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def cross(cx, cy, r=14):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{REDL}" stroke="{RED}" stroke-width="1.5"/>'
            f'<path d="M{cx-5} {cy-5} l10 10 M{cx+5} {cy-5} l-10 10" stroke="{RED}" stroke-width="2.4" '
            f'stroke-linecap="round"/>')


def chip(x, y, label, size=15, fill=LIGHT, stroke=MID, color=NAVY, pad=26):
    w = tw(label, size) + pad
    return rect(x, y, w, 34, fill, stroke, rx=17) + t(x + w / 2, y + 22, label, size, color, 500, "middle"), w


def svg(lang, h, body, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img">
<title>{escape(title)}</title>
<defs>
<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#EEF3FB" stroke-width="1"/></pattern>
<marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{BLUE}"/></marker>
<style>text{{font-family:{FONTS[lang]}}}</style>
</defs>
<rect width="{W}" height="{h}" rx="16" fill="#fff"/>
<rect width="{W}" height="{h}" rx="16" fill="url(#grid)" stroke="{LINE}" stroke-width="1.5"/>
{body}
</svg>
'''


# ---------------------------------------------------------------- 1. three stages
STAGES = {
    "zh": dict(
        title="Pitchat 抽獎流程三階段總覽",
        api_sub="逐頁回傳留言",
        browser="全部在你的瀏覽器中執行",
        stages=[
            ("1", "階段一・讀取與抽樣", "邊讀取邊篩選，用水塘抽樣保留約 1,000 則",
             ["排除自己", "重複留言", "時間範圍"], "抽獎名單（約 1,000 則）"),
            ("2", "階段二・條件篩選", "套用進階篩選條件，並確認人數足夠",
             ["封鎖名單", "關鍵字", "提及人數", "重複中獎"], "符合條件的候選人"),
            ("3", "階段三・隨機抽獎", "依「重複中獎」設定選擇抽獎方式",
             ["允許重複中獎 → 每次隨機抽，可能再抽中", "不允許重複中獎 → 洗牌後依序選出"], None),
        ],
        winners="得獎名單",
    ),
    "en": dict(
        title="Overview of Pitchat's three-stage giveaway draw",
        api_sub="Returns comments page by page",
        browser="Everything runs in your browser",
        stages=[
            ("1", "Stage 1 · Read and sample", "Filter as comments arrive; sample about 1,000",
             ["Exclude yourself", "Duplicate comments", "Time range"], "Candidate pool (about 1,000)"),
            ("2", "Stage 2 · Filter", "Apply detailed filters; check there are enough people",
             ["Blocklist", "Keywords", "Mentions", "Multiple wins"], "Qualifying candidates"),
            ("3", "Stage 3 · Draw", "Pick winners based on the multiple-wins setting",
             ["Multiple wins allowed → random pick, may repeat",
              "Not allowed → shuffle, then pick in order"], None),
        ],
        winners="Winners",
    ),
}


def trophy(cx, cy, color="#fff"):
    return (f'<path d="M{cx-9} {cy-10} h18 v6 a9 9 0 0 1 -18 0 z" fill="{color}"/>'
            f'<path d="M{cx-9} {cy-8} h-5 a5 5 0 0 0 5 7 M{cx+9} {cy-8} h5 a5 5 0 0 1 -5 7" fill="none" stroke="{color}" stroke-width="2"/>'
            f'<rect x="{cx-2}" y="{cy+4}" width="4" height="5" fill="{color}"/>'
            f'<rect x="{cx-7}" y="{cy+9}" width="14" height="3" rx="1" fill="{color}"/>')


def three_stages(lang):
    d = STAGES[lang]
    b = []
    # API source
    aw = max(220, tw(d["api_sub"], 15) + 44)
    b.append(rect(300 - aw / 2, 24, aw, 60, LIGHT, BLUE))
    b.append(t(300, 50, "Instagram API", 18, NAVY, 700, "middle"))
    b.append(t(300, 72, d["api_sub"], 15, MUTED, 400, "middle"))
    b.append(arrow(300, 84, 300, 120))
    frame_top = 124
    y = frame_top + 36 + 20
    cards = []
    for i, (num, title, sub, chips, out) in enumerate(d["stages"]):
        stacked = num == "3"
        h = 104 + (34 * len(chips) + 10 * (len(chips) - 1) if stacked else 34) + 6
        c = [rect(48, y, 504, h, "#fff", MID, rx=12)]
        c.append(f'<circle cx="82" cy="{y+36}" r="17" fill="{BLUE}"/>')
        c.append(t(82, y + 42, num, 17, "#fff", 700, "middle"))
        c.append(t(110, y + 42, title, 19, INK, 700))
        c.append(t(110, y + 68, sub, 15, MUTED))
        cy = y + 86
        if stacked:
            for label in chips:
                s, _ = chip(110, cy, label)
                c.append(s)
                cy += 44
        else:
            cx = 110
            csize, cpad = 15, 26
            while sum(tw(l, csize) + cpad + 8 for l in chips) - 8 > 426:
                csize, cpad = csize - 0.5, max(18, cpad - 2)
            for label in chips:
                s, w = chip(cx, cy, label, csize, pad=cpad)
                c.append(s)
                cx += w + 8
        b.extend(c)
        y += h
        if out:
            b.append(arrow(300, y, 300, y + 50))
            b.append(t(314, y + 31, out, 15, BLUE, 600))
            y += 54
    frame_bottom = y + 22
    frame = [rect(24, frame_top, 552, frame_bottom - frame_top, "#F8FAFF", BLUE, rx=14, sw=2),
             f'<path d="M24 {frame_top+36} H576" stroke="{MID}" stroke-width="1.5"/>']
    for k, col in enumerate(["#F87171", "#FBBF24", "#34D399"]):
        frame.append(f'<circle cx="{46+k*18}" cy="{frame_top+18}" r="5.5" fill="{col}"/>')
    frame.append(t(300, frame_top + 24, d["browser"], 15, NAVY, 700, "middle"))
    b = b[:4] + frame + b[4:]
    b.append(arrow(300, frame_bottom, 300, frame_bottom + 38))
    wy = frame_bottom + 42
    ww = max(160, tw(d["winners"], 18) + 80)
    b.append(rect(300 - ww / 2, wy, ww, 50, NAVY, rx=25))
    b.append(trophy(300 - ww / 2 + 34, wy + 23))
    b.append(t(300 + 14, wy + 31, d["winners"], 18, "#fff", 700, "middle"))
    return svg(lang, wy + 50 + 24, "\n".join(b), d["title"])


# ---------------------------------------------------------------- 2. reservoir sampling
RES = {
    "zh": dict(
        title="水塘抽樣示意圖：以 5 格候選池為例",
        pool="候選池（5 格）",
        p1="前 5 則留言：全部放進候選池",
        p2="第 6 則：有 5/6 的機率入選",
        p2sub=["入選後隨機取代其中一則（此例取代 #3）"],
        out="移出",
        p3="第 n 則：入選機率是 5/n",
        p3sub=["例如第 100 則的入選機率是 5%。",
               "越晚出現越難入選，但之後被取代的機會也越少，",
               "兩者剛好抵銷。"],
        concl=["讀完全部留言後，每則有效留言留在候選池的機率", "都相同：5 ÷ 有效留言總數"],
        note="Pitchat 實際使用的候選池有 1,000 格",
    ),
    "en": dict(
        title="Reservoir sampling explained with a five-slot candidate pool",
        pool="Candidate pool (5 slots)",
        p1="First 5 comments: all go into the pool",
        p2="Comment #6: gets in with a 5/6 chance",
        p2sub=["If it does, it replaces a random slot (#3 here)"],
        out="out",
        p3="Comment #n: gets in with a 5/n chance",
        p3sub=["For example, comment #100 has a 5% chance.",
               "Later comments are less likely to get in, but also",
               "less likely to be replaced afterwards, so the odds even out."],
        concl=["Once every comment is read, each valid comment has the",
               "same chance of being in the pool: 5 ÷ total valid comments"],
        note="Pitchat's real pool holds 1,000 slots",
    ),
}
def badge(cx, cy, n):
    return (f'<circle cx="{cx}" cy="{cy}" r="13" fill="{BLUE}"/>' + t(cx, cy + 5.5, n, 15, "#fff", 700, "middle"))


SX = [66 + i * 96 for i in range(5)]  # slot x, width 84


def slot(i, y, label, kind="filled"):
    x = SX[i]
    if kind == "new":
        return rect(x, y, 84, 52, BLUE, BLUE) + t(x + 42, y + 33, label, 18, "#fff", 700, "middle")
    return rect(x, y, 84, 52, LIGHT, MID) + t(x + 42, y + 33, label, 18, NAVY, 700, "middle")


def reservoir(lang):
    d = RES[lang]
    b = []
    y = 20
    # panel 1
    h1 = 182
    b.append(rect(20, y, 560, h1, "#fff", MID, rx=12))
    b.append(badge(57, y + 32, "1")); b.append(t(80, y + 38, d["p1"], 18, INK, 700))
    b.append(t(44, y + 70, d["pool"], 15, MUTED))
    for i in range(5):
        b.append(arrow(SX[i] + 42, y + 84, SX[i] + 42, y + 104))
        b.append(slot(i, y + 110, f"#{i+1}"))
    y += h1 + 16
    # panel 2
    sub_h = 24 * len(d["p2sub"])
    h2 = 236 + sub_h
    b.append(rect(20, y, 560, h2, "#fff", MID, rx=12))
    b.append(badge(57, y + 32, "2")); b.append(t(80, y + 38, d["p2"], 18, INK, 700))
    for k, line in enumerate(d["p2sub"]):
        b.append(t(44, y + 64 + 24 * k, line, 15, MUTED))
    ry = y + 64 + sub_h
    # incoming #6 above slot 3, outgoing #3 to the right
    b.append(slot(2, ry, "#6", "new"))
    b.append(rect(SX[3] + 10, ry + 6, 74, 40, "#F3F4F6", "#C9CED6", rx=8, dash="4 3"))
    b.append(t(SX[3] + 47, ry + 32, "#3", 16, "#9AA1AD", 700, "middle"))
    b.append(f'<line x1="{SX[3]+30}" y1="{ry+26}" x2="{SX[3]+64}" y2="{ry+26}" stroke="#9AA1AD" stroke-width="2"/>')
    b.append(t(SX[3] + 94, ry + 32, d["out"], 15, RED, 600))
    sy = ry + 96
    b.append(arrow(SX[2] + 42, ry + 54, SX[2] + 42, sy - 6))
    b.append(f'<path d="M{SX[2]+70} {sy-4} Q{SX[3]+10} {sy-20} {SX[3]+40} {ry+50}" fill="none" '
             f'stroke="#9AA1AD" stroke-width="2" stroke-dasharray="4 3" marker-end="url(#ahg)"/>')
    for i, lab in enumerate(["#1", "#2", "#6", "#4", "#5"]):
        b.append(slot(i, sy, lab, "new" if i == 2 else "filled"))
    y += h2 + 16
    # panel 3
    sub_h = 24 * len(d["p3sub"])
    h3 = 70 + sub_h + 52 + 26
    b.append(rect(20, y, 560, h3, "#fff", MID, rx=12))
    b.append(badge(57, y + 32, "3")); b.append(t(80, y + 38, d["p3"], 18, INK, 700))
    for k, line in enumerate(d["p3sub"]):
        b.append(t(44, y + 64 + 24 * k, line, 15, MUTED))
    sy = y + 64 + sub_h + 6
    for i, lab in enumerate(["#41", "#6", "#87", "#23", "#100"]):
        b.append(slot(i, sy, lab, "new" if lab == "#100" else "filled"))
    y += h3 + 16
    # conclusion
    hc = 30 + 26 * len(d["concl"]) + 34
    b.append(rect(20, y, 560, hc, NAVY, rx=12))
    for k, line in enumerate(d["concl"]):
        b.append(t(300, y + 36 + 26 * k, line, 16, "#fff", 700, "middle"))
    b.append(t(300, y + 36 + 26 * len(d["concl"]) + 8, d["note"], 15, "#C7D6FA", 400, "middle"))
    y += hc + 20
    body = "\n".join(b)
    body = (f'<defs><marker id="ahg" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto"><path d="M0 0L10 5L0 10z" fill="#9AA1AD"/></marker></defs>\n') + body
    return svg(lang, y, body, d["title"])


# ---------------------------------------------------------------- 3. funnel
FUN = {
    "zh": dict(
        title="從原始留言到得獎者的數量變化",
        bars=[("50,000", "原始留言", "Instagram API 回傳的所有留言"),
              ("10,000", "有效留言", None),
              ("1,000", "抽獎名單", None),
              (None, "符合條件的候選人", None),
              (None, "得獎者", None)],
        steps=[("排除 40,000 則：自己的、重複的、超出時間範圍", True),
               ("水塘抽樣：每則有 10% 的機率入選", False),
               ("封鎖名單・關鍵字・提及人數", False),
               ("隨機抽獎", False)],
        note="數字為文中的範例",
    ),
    "en": dict(
        title="How the number of comments shrinks from raw comments to winners",
        bars=[("50,000", "Raw comments", "Everything the Instagram API returns"),
              ("10,000", "Valid comments", None),
              ("1,000", "Candidate pool", None),
              (None, "Qualifying candidates", None),
              (None, "Winners", None)],
        steps=[("40,000 removed: your own, duplicates, outside the time range", True),
               ("Reservoir sampling: each has a 10% chance", False),
               ("Blocklist · Keywords · Mentions", False),
               ("Random draw", False)],
        note="Figures follow the example in the article",
    ),
}


def funnel(lang):
    d = FUN[lang]
    widths = [552, 452, 360, 280, 200]
    fills = ["#EEF3FE", "#DCE7FD", "#C3D5FB", "#9DBBF7", NAVY]
    b = []
    y = 24
    for i, (num, label, sub) in enumerate(d["bars"]):
        w = widths[i]
        x = 300 - w / 2
        color = "#fff" if i == 4 else NAVY
        b.append(rect(x, y, w, 64, fills[i], BLUE if i < 4 else NAVY, rx=12))
        main_y = y + (30 if sub else 40)
        if num:
            b.append(f'<text x="300" y="{main_y}" text-anchor="middle" fill="{color}">'
                     f'<tspan font-size="24" font-weight="800">{num}</tspan>'
                     f'<tspan dx="10" font-size="17" font-weight="600">{escape(label)}</tspan></text>')
        else:
            if i == 4:
                b.append(trophy(300 - tw(label, 18) / 2 - 18, y + 32, "#fff"))
                b.append(t(300 + 14, main_y, label, 18, color, 700, "middle"))
            else:
                b.append(t(300, main_y, label, 18, color, 700, "middle"))
        if sub:
            b.append(t(300, y + 52, sub, 14, MUTED, 400, "middle"))
        y += 64
        if i < 4:
            text, removed = d["steps"][i]
            b.append(f'<line x1="300" y1="{y}" x2="300" y2="{y+60}" stroke="{BLUE}" stroke-width="2" marker-end="url(#ah)"/>')
            pw = tw(text, 15) + 30
            fill, stroke, col = (REDL, RED, RED) if removed else ("#fff", MID, NAVY)
            b.append(rect(300 - pw / 2, y + 13, pw, 32, fill, stroke, rx=16))
            b.append(t(300, y + 34, text, 15, col, 600, "middle"))
            y += 62
    b.append(t(300, y + 32, d["note"], 14, MUTED, 400, "middle"))
    return svg(lang, y + 50, "\n".join(b), d["title"])


# ---------------------------------------------------------------- 4. keyword modes
KW = {
    "zh": dict(
        title="關鍵字篩選的「任一」與「全部」模式範例",
        kwlabel="關鍵字：",
        kws=["喜歡", "推薦"],
        head=("留言", ("任一模式", "包含其中一個"), ("全部模式", "兩個都要包含")),
        rows=[(["好", "*喜歡", "這個顏色！"], True, False),
              (["真心", "*推薦", "，我超", "*喜歡"], True, True),
              (["已追蹤，希望中獎"], False, False)],
    ),
    "en": dict(
        title="Example of the Any and All keyword modes",
        kwlabel="Keywords:",
        kws=["love", "recommend"],
        head=("Comment", ("Any mode", "contains one"), ("All mode", "contains both")),
        rows=[(["I ", "*love", " this colour!"], True, False),
              (["I ", "*love", " it and ", "*recommend", " it"], True, True),
              (["Followed! Hope I win"], False, False)],
    ),
}


def keywords(lang):
    d = KW[lang]
    b = []
    b.append(t(24, 50, d["kwlabel"], 17, INK, 700))
    cx = 24 + tw(d["kwlabel"], 17) + 12
    for k in d["kws"]:
        s, w = chip(cx, 27, k, 16, BLUE, BLUE, "#fff")
        b.append(s)
        cx += w + 10
    top = 84
    c0, c1, c2, c3 = 24, 336, 456, 576
    rows = len(d["rows"])
    b.append(rect(c0, top, c3 - c0, 64 + 64 * rows, "#fff", MID, rx=12))
    b.append(f'<path d="M{c0} {top+12} a12 12 0 0 1 12 -12 H{c3-12} a12 12 0 0 1 12 12 V{top+64} H{c0} z" fill="{LIGHT}"/>')
    b.append(t(c0 + 18, top + 39, d["head"][0], 16, NAVY, 700))
    for (title, sub), (xa, xb) in zip(d["head"][1:], [(c1, c2), (c2, c3)]):
        b.append(t((xa + xb) / 2, top + 29, title, 16, NAVY, 700, "middle"))
        b.append(t((xa + xb) / 2, top + 50, sub, 13.5, MUTED, 400, "middle"))
    for x in (c1, c2):
        b.append(f'<line x1="{x}" y1="{top}" x2="{x}" y2="{top+64+64*rows}" stroke="{LINE}" stroke-width="1.5"/>')
    for r, (parts, any_ok, all_ok) in enumerate(d["rows"]):
        y = top + 64 + 64 * r
        b.append(f'<line x1="{c0}" y1="{y}" x2="{c3}" y2="{y}" stroke="{LINE}" stroke-width="1.5"/>')
        spans = []
        for p in parts:
            if p.startswith("*"):
                spans.append(f'<tspan fill="{BLUE}" font-weight="700">{escape(p[1:])}</tspan>')
            else:
                spans.append(f'<tspan>{escape(p)}</tspan>')
        b.append(f'<text x="{c0+18}" y="{y+38}" font-size="16" fill="{INK}" xml:space="preserve">{"".join(spans)}</text>')
        b.append(check((c1 + c2) / 2, y + 32) if any_ok else cross((c1 + c2) / 2, y + 32))
        b.append(check((c2 + c3) / 2, y + 32) if all_ok else cross((c2 + c3) / 2, y + 32))
    return svg(lang, top + 64 + 64 * rows + 24, "\n".join(b), d["title"])


for name, fn in [("three-stages", three_stages), ("reservoir-sampling", reservoir),
                 ("comment-funnel", funnel), ("keyword-modes", keywords)]:
    for lang in ("zh", "en"):
        (OUT / f"{name}.{lang}.svg").write_text(fn(lang), encoding="utf-8")
        print("wrote", f"{name}.{lang}.svg")
