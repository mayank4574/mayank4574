#!/usr/bin/env python3
"""
build_banners.py - Generates dark.svg and light.svg for Mayank Yadav's GitHub profile.
Features:
- Perfectly looped 8.0s animation cycle for GIF rendering
- Organic scattered dot portrait materialization
- Subtle floating data particles and breathing accents
- Synchronized LIVE pulse and terminal cursor
- High-res SVG source assets matching cyan/violet/emerald palette
"""

import math
from PIL import Image, ImageEnhance
from rembg import remove, new_session
import numpy as np

def generate_masks():
    """Ensure dither masks are up to date from myimg.jpeg."""
    try:
        im = Image.open('myimg.jpeg')
        im.thumbnail((800, 1200))
        session = new_session('u2netp')
        nobg = remove(im, session=session)
        # Head center = 355, top = 255
        crop_box = (65, 215, 645, 872)
        cropped = nobg.crop(crop_box)
        target_w, target_h = 280, 320
        img_small = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
        alpha = np.array(img_small)[:, :, 3]

        gray = img_small.convert('L')
        gray = ImageEnhance.Contrast(gray).enhance(1.4)
        gray = ImageEnhance.Sharpness(gray).enhance(1.8)

        arr = np.array(gray, dtype=float)
        dither = arr.copy()
        for y in range(target_h):
            for x in range(target_w):
                old_val = dither[y, x]
                new_val = 255 if old_val > 128 else 0
                dither[y, x] = new_val
                err = old_val - new_val
                if x + 1 < target_w:
                    dither[y, x + 1] += err * 7 / 16
                if y + 1 < target_h:
                    if x - 1 >= 0:
                        dither[y + 1, x - 1] += err * 3 / 16
                    dither[y + 1, x] += err * 5 / 16
                    if x + 1 < target_w:
                        dither[y + 1, x + 1] += err * 1 / 16

        dither_high = (dither >= 128).astype(np.uint8) * 255
        dither_high[alpha < 50] = 0
        Image.fromarray(dither_high).save('dither_high_features.png')

        dither_dark = (dither < 128).astype(np.uint8) * 255
        dither_dark[alpha < 50] = 0
        Image.fromarray(dither_dark).save('dither_dark_features.png')
    except Exception as e:
        print("Note on mask generation:", e)

def get_runs(binary_mask):
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
    parts = []
    for x, y, w in runs_subset:
        if w == 1:
            parts.append(f"M{x} {y}h1v1h-1z")
        else:
            parts.append(f"M{x} {y}h{w}v1h-{w}z")
    return "".join(parts)

def build_banner(theme="dark"):
    is_dark = (theme == "dark")
    
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

    mask_file = "dither_high_features.png" if is_dark else "dither_dark_features.png"
    mask = np.array(Image.open(mask_file)) > 128
    
    H, W = mask.shape
    runs = get_runs(mask)
    
    NUM_GROUPS = 14
    groups = [[] for _ in range(NUM_GROUPS)]
    for run in runs:
        x, y, w = run
        gid = (x // 3 + y * 7 + (x ^ y) * 3) % NUM_GROUPS
        groups[gid].append(run)

    scale_x = 360.0 / W
    scale_y = 448.0 / H
    trans_x = 36 + (400 - W * scale_x) / 2
    trans_y = 84 + (492 - H * scale_y) / 2

    # Loop period T = 8.0s
    LOOP_DUR = "8s"

    svg = []
    a = svg.append

    a(f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="610" viewBox="0 0 1180 610" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace" role="img" aria-label="Mayank Yadav — profile.sh --live">
<defs>
  <linearGradient id="accent_{theme}" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{GRAD_STOP1}"><animate attributeName="stop-color" values="{GRAD_STOP1};{GRAD_STOP2};{GRAD_STOP3};{GRAD_STOP1}" dur="{LOOP_DUR}" repeatCount="indefinite"/></stop>
    <stop offset="0.5" stop-color="{GRAD_STOP2}"><animate attributeName="stop-color" values="{GRAD_STOP2};{GRAD_STOP3};{GRAD_STOP1};{GRAD_STOP2}" dur="{LOOP_DUR}" repeatCount="indefinite"/></stop>
    <stop offset="1" stop-color="{GRAD_STOP3}"><animate attributeName="stop-color" values="{GRAD_STOP3};{GRAD_STOP1};{GRAD_STOP2};{GRAD_STOP3}" dur="{LOOP_DUR}" repeatCount="indefinite"/></stop>
  </linearGradient>
  <linearGradient id="panelGrad_{theme}" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{PANEL_START}"/>
    <stop offset="1" stop-color="{PANEL_END}"/>
  </linearGradient>
  <filter id="glow8_{theme}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="8"/></filter>
  <filter id="glow3_{theme}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3"/></filter>
  <filter id="txtGlow_{theme}" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="0.9" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <clipPath id="winClip_{theme}"><rect x="2" y="2" width="1176" height="606" rx="18"/></clipPath>
  <circle id="particle_{theme}" r="2" fill="{PORTRAIT_COLOR}"/>
  <circle id="node_{theme}" r="3" fill="{CYAN}"/>
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
  <rect x="36" y="84" width="400" height="492" rx="10" fill="none" stroke="{CORNER_ACCENT}" stroke-width="2" opacity="0.4" filter="url(#glow3_{theme})"/>
  <rect x="36" y="84" width="400" height="492" rx="10" fill="{CARD_BG}" stroke="{CARD_BORDER}"/>

  <!-- Corner Brackets on Portrait Card -->
  <path d="M 50 84 L 36 84 L 36 98" fill="none" stroke="{CORNER_ACCENT}" stroke-width="2" opacity="0.8"/>
  <path d="M 422 84 L 436 84 L 436 98" fill="none" stroke="{CORNER_ACCENT}" stroke-width="2" opacity="0.8"/>
  <path d="M 50 576 L 36 576 L 36 562" fill="none" stroke="{CORNER_ACCENT}" stroke-width="2" opacity="0.8"/>
  <path d="M 422 576 L 436 576 L 436 562" fill="none" stroke="{CORNER_ACCENT}" stroke-width="2" opacity="0.8"/>

  <!-- Dithered Portrait Elements (Looping organic materialization and breathing) -->
  <g transform="translate({trans_x:.1f},{trans_y:.1f}) scale({scale_x:.4f},{scale_y:.4f})" fill="{PORTRAIT_COLOR}" shape-rendering="crispEdges">''')

    for gid in range(NUM_GROUPS):
        # 8s loop: appears between 0s and 1.2s, stays, subtle wave at 5.5s-6.5s, loops smoothly
        t_in = 0.05 + gid * 0.07 # 0.05s to ~0.96s
        t_hold = 5.2
        t_morph = 5.8 + (gid % 4) * 0.15
        group_runs = groups[gid]
        path_data = format_path(group_runs)
        
        # Opacity animation keytimes across 8.0s
        # 0s: 0.1 -> t_in: 1.0 -> 5.2s: 1.0 -> t_morph: 0.3 -> 7.2s: 0.85 -> 8s: 0.1
        k0 = 0.0
        k1 = t_in / 8.0
        k2 = t_hold / 8.0
        k3 = t_morph / 8.0
        k4 = 0.88
        k5 = 1.00
        
        a(f'''    <g opacity="0">
      <animate attributeName="opacity" values="0;1;1;0.45;0.95;0" keyTimes="{k0:.3f};{k1:.3f};{k2:.3f};{k3:.3f};{k4:.3f};{k5:.3f}" dur="{LOOP_DUR}" repeatCount="indefinite" calcMode="spline" keySplines=".4 0 .2 1;.4 0 .2 1;.4 0 .2 1;.4 0 .2 1;.4 0 .2 1"/>
      <path d="{path_data}"/>
    </g>''')

    a('''  </g>''')

    # Ambient moving data nodes / morphing particle network
    a(f'''  <!-- Dynamic Floating Node Network (8.0s Seamless Loop) -->
  <g transform="translate({trans_x:.1f},{trans_y:.1f})">''')
    
    # 12 animated data particles that float and morph
    node_configs = [
        (45, 60, "0 0; 8 -18; 20 -8; 0 0", "8s", "0.0s"),
        (235, 80, "0 0; -12 16; -24 0; 0 0", "8s", "0.4s"),
        (35, 270, "0 0; 15 -20; 5 -35; 0 0", "8s", "0.8s"),
        (245, 250, "0 0; -18 -15; -30 10; 0 0", "8s", "1.2s"),
        (140, 30, "0 0; 16 10; -10 20; 0 0", "8s", "0.2s"),
        (210, 300, "0 0; -14 -22; 8 -15; 0 0", "8s", "1.6s"),
        (90, 180, "0 0; -10 15; 15 25; 0 0", "8s", "1.0s"),
        (190, 170, "0 0; 12 -14; -15 -25; 0 0", "8s", "1.4s"),
        (120, 240, "0 0; 20 -10; -10 -20; 0 0", "8s", "0.6s"),
        (160, 270, "0 0; -15 15; 10 25; 0 0", "8s", "1.8s"),
        (70, 120, "0 0; 14 18; -8 10; 0 0", "8s", "0.5s"),
        (210, 130, "0 0; -16 -12; 10 -20; 0 0", "8s", "1.1s"),
    ]
    for px, py, vals, dur, beg in node_configs:
        a(f'''    <use href="#node_{theme}" x="{px}" y="{py}" opacity="0">
      <animate attributeName="opacity" values="0;0.75;0.9;0.5;0" keyTimes="0;0.25;0.5;0.75;1" dur="{dur}" begin="{beg}" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="translate" values="{vals}" dur="{dur}" begin="{beg}" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.33;0.66;1" keySplines=".4 0 .6 1;.4 0 .6 1;.4 0 .6 1"/>
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
  <rect x="470" y="116" width="220" height="20" rx="4" fill="{BADGE_BG}"/>
  <text x="480" y="130" font-size="13" font-weight="700" fill="{BADGE_TXT}">@mayank4574</text>
  <line x1="700" y1="126" x2="1125" y2="126" stroke="{LINE_BORDER}"/>
''')

    # Monospace Rows with lengthAdjust="spacingAndGlyphs" textLength="655"
    rows_data = [
        ("item", "SUBJECT", "Mayank Yadav"),
        ("item", "ROLE", "MERN Stack Developer"),
        ("item", "ORIGIN", "Gujarat, India"),
        ("item", "EDUCATION", "Parul University"),
        ("item", "STATUS", "BUILDING + LEARNING + SHIPPING"),
        ("item", "TOOLCHAIN", "VS Code · Git · GitHub · Docker"),
        
        ("sep", "- CORE ARCHITECTURE", "--------------------------------------------------------"),
        ("item", "CORE.LANG", "JavaScript · Python · Java"),
        ("item", "CORE.FRONTEND", "React · Tailwind CSS · EJS"),
        ("item", "CORE.BACKEND", "Node.js · Express.js"),
        ("item", "CORE.DATABASE", "MongoDB · MySQL"),
        ("item", "CORE.AI", "Data Science · GenAI · Agentic AI"),
        ("item", "CORE.TOOLS", "Git · GitHub · Postman · Docker"),
        
        ("sep", "- NETWORK MATRIX", "------------------------------------------------------------"),
        ("item", "GRID.MAIL", "mayankyadav4574@gmail.com"),
        ("item", "GRID.PORTFOLIO", "https://mayankyadav.in"),
        ("item", "GRID.LINKEDIN", "in/mayank-yadav-8a55992a3"),
        ("item", "GRID.GITHUB", "@mayank4574"),
        ("item", "GRID.LEETCODE", "leetcode.com/u/Mayank4574/"),
    ]

    cur_y = 156
    for row in rows_data:
        rtype = row[0]
        if rtype == "sep":
            header_txt, line_dashes = row[1], row[2]
            a(f'''  <text x="470" y="{cur_y}" font-size="13" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="{MUTED}">{header_txt} </tspan><tspan fill="{DOT_COLOR}">{line_dashes}</tspan></text>''')
            cur_y += 21
        else:
            label, val = row[1], row[2]
            dots = "." * 60
            a(f'''  <text x="470" y="{cur_y}" font-size="13.5" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="{CYAN}">{label} </tspan><tspan fill="{DOT_COLOR}">{dots}</tspan><tspan fill="{TEXT}" font-weight="600"> {val}</tspan></text>''')
            cur_y += 21

    # Footer interactive cue with 1.0s blinking cursor
    a(f'''
  <!-- Footer Interactive Cue -->
  <text x="470" y="575" font-size="13.5" fill="{MUTED}">&#9656; More about me &amp; projects below in README &#8595; <tspan fill="{CYAN}">&#9608;<animate attributeName="fill-opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></tspan></text>
</g>

<!-- Animated Glowing Outer Border (8.0s synchronized loop) -->
<rect x="3" y="3" width="1174" height="604" rx="17" fill="none" stroke="url(#accent_{theme})" stroke-width="3" opacity="0.55" filter="url(#glow8_{theme})"/>
<rect x="3" y="3" width="1174" height="604" rx="17" fill="none" stroke="url(#accent_{theme})" stroke-width="1.6"/>
</svg>''')

    return "\n".join(svg)

if __name__ == "__main__":
    generate_masks()
    dark_svg = build_banner("dark")
    with open("dark.svg", "w", encoding="utf-8") as f:
        f.write(dark_svg)
    print(f"Generated dark.svg: {len(dark_svg)//1024} KB")

    light_svg = build_banner("light")
    with open("light.svg", "w", encoding="utf-8") as f:
        f.write(light_svg)
    print(f"Generated light.svg: {len(light_svg)//1024} KB")
