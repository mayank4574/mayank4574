#!/usr/bin/env python3
"""
build_banners.py - Generates dark.svg and light.svg for Mayank Yadav's GitHub profile.
Features:
- Futuristic terminal window (1180x610)
- Left panel (~38% width): Tasteful dithered developer-art portrait of Mayank Yadav
- Staggered organic dot appearance animation + subtle floating data nodes
- Right panel: SYSTEM.INFO developer panel with monospace dotted leaders
- Cyan + Violet + Emerald accents
- Full dark and light theme compliance
"""

import math
from PIL import Image
import numpy as np

def get_runs(binary_mask):
    """Convert a 2D boolean numpy array to RLE (x, y, width) runs."""
    H, W = binary_mask.shape
    runs = []
    for y in range(H):
        in_run = False
        start = 0
        for x in range(W):
            if binary_mask[y, x] and not in_run:
                in_run = True
                start = x
            elif not binary_mask[y, x] and in_run:
                in_run = False
                runs.append((start, y, x - start))
        if in_run:
            runs.append((start, y, W - start))
    return runs

def format_path(runs_subset):
    """Format runs into SVG path d attribute."""
    parts = []
    for x, y, w in runs_subset:
        if w == 1:
            parts.append(f"M{x} {y}h1v1h-1z")
        else:
            parts.append(f"M{x} {y}h{w}v1h-{w}z")
    return "".join(parts)

def build_banner(theme="dark"):
    is_dark = (theme == "dark")
    
    # Palette definition
    if is_dark:
        BG = "#0A101F"
        PANEL_TOP = "#0B1222"
        PANEL_START = "#0A101F"
        PANEL_END = "#0C1426"
        CARD_BG = "#0A101F"
        CYAN = "#22D3EE"
        VIOLET = "#A78BFA"
        VIOLET2 = "#7C3AED"
        EMERALD = "#10B981"
        TEXT = "#F8FAFC"
        MUTED = "#94A3B8"
        DIM = "#475569"
        PORTRAIT_COLOR = "#A78BFA"
        LINE_BORDER = "rgba(255,255,255,0.10)"
        CARD_BORDER = "rgba(34,211,238,0.35)"
        CORNER_ACCENT = "#22D3EE"
        BADGE_BG = "#4C1D95"
        BADGE_TXT = "#E9D5FF"
        GRAD_STOP1 = "#7C3AED"
        GRAD_STOP2 = "#22D3EE"
        GRAD_STOP3 = "#10B981"
        DOT_COLOR = "rgba(148,163,184,0.35)"
    else:
        BG = "#F8FAFC"
        PANEL_TOP = "#F1F5F9"
        PANEL_START = "#F8FAFC"
        PANEL_END = "#EEF2F7"
        CARD_BG = "#FFFFFF"
        CYAN = "#0891B2"
        VIOLET = "#7C3AED"
        VIOLET2 = "#6D28D9"
        EMERALD = "#059669"
        TEXT = "#0F172A"
        MUTED = "#475569"
        DIM = "#94A3B8"
        PORTRAIT_COLOR = "#7C3AED"
        LINE_BORDER = "rgba(15,23,42,0.10)"
        CARD_BORDER = "rgba(8,145,178,0.40)"
        CORNER_ACCENT = "#0891B2"
        BADGE_BG = "#DDD6FE"
        BADGE_TXT = "#5B21B6"
        GRAD_STOP1 = "#2563EB"
        GRAD_STOP2 = "#0891B2"
        GRAD_STOP3 = "#059669"
        DOT_COLOR = "rgba(100,116,139,0.35)"

    # Load pre-processed dither image
    if is_dark:
        mask = np.array(Image.open("dither_high_features.png")) > 128
    else:
        mask = np.array(Image.open("dither_dark_features.png")) > 128
    
    H, W = mask.shape # 320 x 280
    runs = get_runs(mask)
    
    # Partition runs into 14 interleaved groups for organic appearance
    NUM_GROUPS = 14
    groups = [[] for _ in range(NUM_GROUPS)]
    for run in runs:
        x, y, w = run
        gid = (x // 3 + y * 7 + (x ^ y) * 3) % NUM_GROUPS
        groups[gid].append(run)

    # Scale and translate portrait into the visual card (card is 400x492 at x=36, y=84)
    # Available area: ~360 wide x 448 high
    scale_x = 360.0 / W # ~1.2857
    scale_y = 448.0 / H # ~1.4000
    trans_x = 36 + (400 - W * scale_x) / 2 # ~56
    trans_y = 84 + (492 - H * scale_y) / 2 # ~106

    svg = []
    a = svg.append

    a(f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="610" viewBox="0 0 1180 610" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace" role="img" aria-label="Mayank Yadav — profile.sh --live">
<defs>
  <linearGradient id="accent_{theme}" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{GRAD_STOP1}"><animate attributeName="stop-color" values="{GRAD_STOP1};{GRAD_STOP2};{GRAD_STOP3};{GRAD_STOP1}" dur="10s" repeatCount="indefinite"/></stop>
    <stop offset="0.5" stop-color="{GRAD_STOP2}"><animate attributeName="stop-color" values="{GRAD_STOP2};{GRAD_STOP3};{GRAD_STOP1};{GRAD_STOP2}" dur="10s" repeatCount="indefinite"/></stop>
    <stop offset="1" stop-color="{GRAD_STOP3}"><animate attributeName="stop-color" values="{GRAD_STOP3};{GRAD_STOP1};{GRAD_STOP2};{GRAD_STOP3}" dur="10s" repeatCount="indefinite"/></stop>
  </linearGradient>
  <linearGradient id="panelGrad_{theme}" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{PANEL_START}"/>
    <stop offset="1" stop-color="{PANEL_END}"/>
  </linearGradient>
  <filter id="glow8_{theme}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="8"/></filter>
  <filter id="glow3_{theme}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3"/></filter>
  <filter id="txtGlow_{theme}" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="0.9" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <clipPath id="winClip_{theme}"><rect x="2" y="2" width="1176" height="606" rx="18"/></clipPath>
  <rect id="particle_{theme}" width="2.4" height="2.4" rx="1.2" fill="{PORTRAIT_COLOR}"/>
</defs>

<!-- Main Terminal Frame -->
<rect x="2" y="2" width="1176" height="606" rx="18" fill="{BG}"/>
<g clip-path="url(#winClip_{theme})">
  <rect x="2" y="2" width="1176" height="606" fill="url(#panelGrad_{theme})"/>
  
  <!-- Terminal Top Bar -->
  <rect x="2" y="2" width="1176" height="46" fill="{PANEL_TOP}"/>
  <line x1="2" y1="48" x2="1178" y2="48" stroke="{LINE_BORDER}"/>
  <circle cx="30" cy="25" r="5.5" fill="#ff5f56"/>
  <circle cx="50" cy="25" r="5.5" fill="#ffbd2e"/>
  <circle cx="70" cy="25" r="5.5" fill="#27c93f"/>
  <text x="590" y="29" text-anchor="middle" font-size="12" fill="{MUTED}">mayankyadav4574@gmail.com - % ./profile.sh --live</text>

  <!-- LEFT PANEL: VISUAL.MAP / PORTRAIT -->
  <text x="38" y="74" font-size="10" letter-spacing="3" fill="{DIM}">VISUAL.MAP</text>
  <rect x="36" y="84" width="400" height="492" rx="10" fill="none" stroke="{CORNER_ACCENT}" stroke-width="2" opacity="0.35" filter="url(#glow3_{theme})"/>
  <rect x="36" y="84" width="400" height="492" rx="10" fill="{CARD_BG}" stroke="{CARD_BORDER}"/>

  <!-- Corner Brackets on Portrait Card -->
  <path d="M 50 84 L 36 84 L 36 98" fill="none" stroke="{CORNER_ACCENT}" stroke-width="2" opacity="0.8"/>
  <path d="M 422 84 L 436 84 L 436 98" fill="none" stroke="{CORNER_ACCENT}" stroke-width="2" opacity="0.8"/>
  <path d="M 50 576 L 36 576 L 36 562" fill="none" stroke="{CORNER_ACCENT}" stroke-width="2" opacity="0.8"/>
  <path d="M 422 576 L 436 576 L 436 562" fill="none" stroke="{CORNER_ACCENT}" stroke-width="2" opacity="0.8"/>

  <!-- Dithered Portrait Elements -->
  <g transform="translate({trans_x:.1f},{trans_y:.1f}) scale({scale_x:.4f},{scale_y:.4f})" fill="{PORTRAIT_COLOR}" shape-rendering="crispEdges">''')

    # Add each interleaved group with staggered entrance
    for gid in range(NUM_GROUPS):
        delay = 0.20 + gid * 0.04
        group_runs = groups[gid]
        path_data = format_path(group_runs)
        a(f'''    <g opacity="0">
      <animate attributeName="opacity" values="0;1" dur="0.8s" begin="{delay:.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".4 0 .2 1"/>
      <path d="{path_data}"/>
    </g>''')

    a('''  </g>''')

    # Subtle floating particles around the portrait for living motion
    a(f'''  <!-- Subtle Ambient Data Particles -->
  <g transform="translate({trans_x:.1f},{trans_y:.1f})">''')
    particles = [
        (40, 60, "0 0; 0 -12; 0 0", "6s", "0.5s"),
        (240, 90, "0 0; 0 10; 0 0", "7s", "1.0s"),
        (30, 260, "0 0; 0 -15; 0 0", "8s", "0.2s"),
        (250, 240, "0 0; 0 14; 0 0", "6.5s", "1.5s"),
        (140, 20, "0 0; 8 0; 0 0", "9s", "0.8s"),
        (220, 290, "0 0; -6 -6; 0 0", "7.5s", "2.0s"),
    ]
    for px, py, vals, dur, beg in particles:
        a(f'''    <use href="#particle_{theme}" x="{px}" y="{py}" opacity="0">
      <animate attributeName="opacity" values="0;0.6;0" dur="{dur}" begin="{beg}" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="translate" values="{vals}" dur="{dur}" begin="{beg}" repeatCount="indefinite"/>
    </use>''')
    a('''  </g>''')

    # RIGHT PANEL: SYSTEM.INFO
    a(f'''
  <!-- RIGHT PANEL: SYSTEM.INFO -->
  <text x="470" y="104" font-size="13" letter-spacing="2" fill="{CYAN}" filter="url(#txtGlow_{theme})">SYSTEM.INFO</text>
  <line x1="566" y1="100" x2="1055" y2="100" stroke="{LINE_BORDER}"/>
  <text x="1125" y="104" text-anchor="end" font-size="12" fill="#F87171" font-weight="700">
    <tspan>&#9679;</tspan> LIVE
    <animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/>
  </text>

  <!-- Identity Pill Header -->
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.5s" fill="freeze"/>
    <rect x="470" y="116" width="220" height="20" rx="4" fill="{BADGE_BG}"/>
    <text x="480" y="130" font-size="13" font-weight="700" fill="{BADGE_TXT}">@mayank4574</text>
    <line x1="700" y1="126" x2="1125" y2="126" stroke="{LINE_BORDER}"/>
  </g>
''')

    # Monospace Rows with lengthAdjust="spacingAndGlyphs" textLength="655"
    # Starting at y=156, step=21 px
    rows_data = [
        # (type, label, value, delay)
        ("item", "SUBJECT", "Mayank Yadav", 0.70),
        ("item", "ROLE", "MERN Stack Developer", 0.76),
        ("item", "ORIGIN", "Gujarat, India", 0.82),
        ("item", "EDUCATION", "Parul University", 0.88),
        ("item", "STATUS", "BUILDING + LEARNING + SHIPPING", 0.94),
        ("item", "TOOLCHAIN", "VS Code · Git · GitHub · Docker", 1.00),
        
        ("sep", "- CORE ARCHITECTURE", "--------------------------------------------------------", 1.06),
        ("item", "CORE.LANG", "JavaScript · Python · Java", 1.12),
        ("item", "CORE.FRONTEND", "React · Tailwind CSS · EJS", 1.18),
        ("item", "CORE.BACKEND", "Node.js · Express.js", 1.24),
        ("item", "CORE.DATABASE", "MongoDB · MySQL", 1.30),
        ("item", "CORE.AI", "Data Science · GenAI · Agentic AI", 1.36),
        ("item", "CORE.TOOLS", "Git · GitHub · Postman · Docker", 1.42),
        
        ("sep", "- NETWORK MATRIX", "------------------------------------------------------------", 1.48),
        ("item", "GRID.MAIL", "mayankyadav4574@gmail.com", 1.54),
        ("item", "GRID.PORTFOLIO", "https://mayankyadav.in", 1.60),
        ("item", "GRID.LINKEDIN", "in/mayank-yadav-8a55992a3", 1.66),
        ("item", "GRID.GITHUB", "@mayank4574", 1.72),
        ("item", "GRID.LEETCODE", "leetcode.com/u/Mayank4574/", 1.78),
    ]

    cur_y = 156
    for row in rows_data:
        rtype = row[0]
        delay = row[3]
        if rtype == "sep":
            header_txt, line_dashes = row[1], row[2]
            a(f'''  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{delay:.2f}s" fill="freeze"/>
    <text x="470" y="{cur_y}" font-size="13" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="{MUTED}">{header_txt} </tspan><tspan fill="{DOT_COLOR}">{line_dashes}</tspan></text>
  </g>''')
            cur_y += 21
        else:
            label, val = row[1], row[2]
            dots = "." * 60
            a(f'''  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{delay:.2f}s" fill="freeze"/>
    <animateTransform attributeName="transform" type="translate" values="-6 0;0 0" dur="0.4s" begin="{delay:.2f}s" fill="freeze"/>
    <text x="470" y="{cur_y}" font-size="13.5" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="{CYAN}">{label} </tspan><tspan fill="{DOT_COLOR}">{dots}</tspan><tspan fill="{TEXT}" font-weight="600"> {val}</tspan></text>
  </g>''')
            cur_y += 21

    # Footer call to action
    a(f'''
  <!-- Footer Interactive Cue -->
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="1.95s" fill="freeze"/>
    <text x="470" y="575" font-size="13.5" fill="{MUTED}">&#9656; More about me &amp; projects below in README &#8595; <tspan fill="{CYAN}">&#9608;<animate attributeName="fill-opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></tspan></text>
  </g>
</g>

<!-- Animated Glowing Outer Border -->
<rect x="3" y="3" width="1174" height="604" rx="17" fill="none" stroke="url(#accent_{theme})" stroke-width="3" opacity="0.55" filter="url(#glow8_{theme})"/>
<rect x="3" y="3" width="1174" height="604" rx="17" fill="none" stroke="url(#accent_{theme})" stroke-width="1.6"/>
</svg>''')

    return "\n".join(svg)

if __name__ == "__main__":
    dark_svg = build_banner("dark")
    with open("dark.svg", "w", encoding="utf-8") as f:
        f.write(dark_svg)
    print(f"Generated dark.svg: {len(dark_svg)//1024} KB")

    light_svg = build_banner("light")
    with open("light.svg", "w", encoding="utf-8") as f:
        f.write(light_svg)
    print(f"Generated light.svg: {len(light_svg)//1024} KB")
