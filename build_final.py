import os, subprocess

repo_dir = r'c:\Users\Sarath Babu\OneDrive\Documents\AI Agents\Paperclip Project\sarathbabu123'

# Load base64 images (already generated from prior runs)
b64_char_path = os.path.join(repo_dir, 'b64_char.txt')
b64_avatar_path = os.path.join(repo_dir, 'b64_avatar.txt')

if not os.path.exists(b64_char_path) or not os.path.exists(b64_avatar_path):
    import base64, io
    from PIL import Image, ImageFilter, ImageDraw
    import numpy as np

    img_path = r'C:\Users\Sarath Babu\.gemini\antigravity-ide\brain\5d40df26-c6a2-4a06-9a4d-06a5fa629b6e\media__1785436262426.jpg'
    img = Image.open(img_path).convert('RGBA')

    arr = np.array(img, dtype=float)
    corner_bg = np.mean(arr[:40, :40, :3], axis=(0,1))
    diff = np.linalg.norm(arr[:, :, :3] - corner_bg, axis=2)
    alpha = np.clip((diff - 28.0) / 25.0, 0, 1) * 255.0
    alpha_img = Image.fromarray(alpha.astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    arr[:, :, 3] = np.array(alpha_img)
    char_img = Image.fromarray(arr.astype(np.uint8))
    char_img.thumbnail((440, 540), Image.Resampling.LANCZOS)
    buffer_char = io.BytesIO()
    char_img.save(buffer_char, format='PNG', optimize=True)
    b64_char = base64.b64encode(buffer_char.getvalue()).decode('utf-8')

    w, h = img.size
    head_crop = img.crop((w//2 - 200, 30, w//2 + 200, 430))
    head_crop = head_crop.resize((240, 240), Image.Resampling.LANCZOS)
    mask = Image.new('L', (240, 240), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 240, 240), fill=255)
    avatar_img = Image.new('RGBA', (240, 240), (0,0,0,0))
    avatar_img.paste(head_crop, (0, 0), mask)
    buffer_avatar = io.BytesIO()
    avatar_img.save(buffer_avatar, format='PNG', optimize=True)
    b64_avatar = base64.b64encode(buffer_avatar.getvalue()).decode('utf-8')
    open(b64_char_path, 'w').write(b64_char)
    open(b64_avatar_path, 'w').write(b64_avatar)
else:
    b64_char = open(b64_char_path, 'r', encoding='utf-8').read().strip()
    b64_avatar = open(b64_avatar_path, 'r', encoding='utf-8').read().strip()

print(f"Images ready — char: {len(b64_char)} chars, avatar: {len(b64_avatar)} chars")

# ─────────────────────────────────────────────────────────────────────────────
# 1. BANNER.SVG  — minimalist, warm, nocturnal
#    Layout: left column = text identity; right column = Ghibli portrait
#    Palette: #080c08 bg / #eee9da cream / #d4c49a warm-amber / #a3b899 sage
#    NO terminal prompts, NO code snippets, NO badge cards, NO neon lines.
# ─────────────────────────────────────────────────────────────────────────────
banner_dark = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
  <defs>
    <radialGradient id="bg" cx="42%" cy="78%" r="110%">
      <stop offset="0%"  stop-color="#0b1009"/>
      <stop offset="55%" stop-color="#07090600"/>
      <stop offset="100%" stop-color="#050705"/>
    </radialGradient>

    <linearGradient id="nameGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"  stop-color="#eee9da"/>
      <stop offset="100%" stop-color="#d4c49a"/>
    </linearGradient>

    <!-- Vignette on portrait edges -->
    <linearGradient id="fadeLeft" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"  stop-color="#07090600" stop-opacity="0"/>
      <stop offset="18%" stop-color="#070906" stop-opacity="0.82"/>
      <stop offset="100%" stop-color="#070906" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="fadeBottom" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="50%" stop-color="#070906" stop-opacity="0"/>
      <stop offset="100%" stop-color="#070906" stop-opacity="1"/>
    </linearGradient>

    <filter id="glow" color-interpolation-filters="sRGB" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="22" result="b"/>
      <feComposite in="SourceGraphic" in2="b" operator="over"/>
    </filter>

    <clipPath id="bgClip">
      <rect width="1200" height="630" rx="0"/>
    </clipPath>
    <clipPath id="portraitClip">
      <rect x="640" y="0" width="560" height="630"/>
    </clipPath>
  </defs>

  <style>
    /* EB Garamond: serif elegance matching the portfolio */
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&amp;family=Fira+Code:wght@400;500&amp;display=swap');

    /* Firefly drift — two slow orbs for atmosphere */
    .orb1 {{ animation: drift1 14s ease-in-out infinite alternate; }}
    @keyframes drift1 {{
      from {{ transform: translate(0,0)  scale(1);   opacity: .07; }}
      to   {{ transform: translate(30px,-22px) scale(1.08); opacity: .13; }}
    }}
    .orb2 {{ animation: drift2 19s ease-in-out infinite alternate; }}
    @keyframes drift2 {{
      from {{ transform: translate(0,0)  scale(1);   opacity: .06; }}
      to   {{ transform: translate(-20px,18px) scale(.93); opacity: .11; }}
    }}

    /* Firefly motes — tiny glowing dots */
    .mote {{ animation: mote 7s ease-in-out infinite alternate; }}
    @keyframes mote {{
      from {{ opacity: .15; transform: translateY(0); }}
      to   {{ opacity: .55; transform: translateY(-12px); }}
    }}

    /* Blinking cursor */
    .cursor {{ animation: blink .95s step-end infinite; }}
    @keyframes blink {{ 0%,100%{{opacity:1}} 50%{{opacity:0}} }}
  </style>

  <g clip-path="url(#bgClip)">
    <!-- Base -->
    <rect width="1200" height="630" fill="#070906"/>
    <rect width="1200" height="630" fill="url(#bg)"/>

    <!-- Ambient warm bloom (left) -->
    <circle cx="200" cy="420" r="300" fill="#c8a96e" class="orb1" filter="url(#glow)" opacity=".09"/>
    <!-- Ambient cool bloom (right) -->
    <circle cx="980" cy="180" r="280" fill="#7da68a" class="orb2" filter="url(#glow)" opacity=".08"/>

    <!-- Firefly motes -->
    <circle cx="88"  cy="312" r="2.2" fill="#d4c49a" class="mote" style="animation-delay:0s"/>
    <circle cx="310" cy="145" r="1.8" fill="#c8e6c9" class="mote" style="animation-delay:2.3s"/>
    <circle cx="520" cy="490" r="2.5" fill="#d4c49a" class="mote" style="animation-delay:1.1s"/>
    <circle cx="420" cy="75"  r="1.5" fill="#c8e6c9" class="mote" style="animation-delay:4.7s"/>
    <circle cx="195" cy="560" r="2"   fill="#d4c49a" class="mote" style="animation-delay:3.2s"/>

    <!-- ── Portrait (right half) ─────────────────────────────────────── -->
    <g clip-path="url(#portraitClip)">
      <!-- Portrait image — natural placement, full height -->
      <image
        href="data:image/png;base64,{b64_char}"
        x="648" y="40" width="510" height="590"
        preserveAspectRatio="xMidYMax meet"
        opacity=".92"/>

      <!-- Subtle left-edge fade so portrait blends into content -->
      <rect x="640" width="180" height="630" fill="url(#fadeLeft)" opacity=".9"/>
      <!-- Bottom fade into background -->
      <rect x="640" y="0" width="560" height="630" fill="url(#fadeBottom)" opacity=".6"/>
    </g>

    <!-- ── Left content column ─────────────────────────────────────────── -->
    <!-- Overline label -->
    <text x="62" y="118"
          font-family="'Fira Code', monospace"
          font-size="11" font-weight="500"
          fill="#a3b899" letter-spacing="3"
          opacity=".8">DATA SCIENTIST  ·  BENGALURU, INDIA</text>

    <!-- Divider rule -->
    <line x1="62" y1="130" x2="340" y2="130" stroke="#a3b899" stroke-width=".8" opacity=".3"/>

    <!-- Name — big, warm, serif -->
    <text x="60" y="202"
          font-family="'EB Garamond', Georgia, serif"
          font-size="74" font-weight="600"
          fill="url(#nameGrad)"
          letter-spacing=".5">Sarath Babu P</text>

    <!-- Sub-role line -->
    <text x="62" y="234"
          font-family="'EB Garamond', Georgia, serif"
          font-size="19" font-weight="400" font-style="italic"
          fill="#a3b899" letter-spacing=".3">Applied Machine Learning Engineer</text>

    <!-- Thin rule separating name block from body -->
    <line x1="62" y1="256" x2="580" y2="256" stroke="#eee9da" stroke-width=".6" opacity=".1"/>

    <!-- Short bio — original, not copied -->
    <text x="62" y="290"
          font-family="'EB Garamond', Georgia, serif"
          font-size="16" fill="#cec8b8" letter-spacing=".2">I find signal in noise — the real kind, not the</text>
    <text x="62" y="313"
          font-family="'EB Garamond', Georgia, serif"
          font-size="16" fill="#cec8b8" letter-spacing=".2">cleaned, pre-packaged kind. That takes patience.</text>

    <!-- Second bio line -->
    <text x="62" y="347"
          font-family="'EB Garamond', Georgia, serif"
          font-size="16" fill="#a39e92" letter-spacing=".2">Currently: ML pipelines for EV fleets @ Mooving</text>
    <text x="62" y="369"
          font-family="'EB Garamond', Georgia, serif"
          font-size="16" fill="#a39e92" letter-spacing=".2">Formerly: IoT telemetry at Livguard Drivetrain</text>

    <!-- Thin rule -->
    <line x1="62" y1="392" x2="440" y2="392" stroke="#eee9da" stroke-width=".6" opacity=".08"/>

    <!-- Philosophy quote — professional -->
    <text x="62" y="418"
          font-family="'EB Garamond', Georgia, serif"
          font-size="20" font-style="italic" font-weight="500"
          fill="#eee9da" opacity=".65"
          letter-spacing=".3">"Finding the ground truth</text>
    <text x="62" y="442"
          font-family="'EB Garamond', Georgia, serif"
          font-size="20" font-style="italic" font-weight="500"
          fill="#eee9da" opacity=".65"
          letter-spacing=".3"> in a noisy world."</text>

    <!-- Stack row — small pill-like chips using pure SVG text + rect -->
    <!-- Python -->
    <g transform="translate(62, 478)">
      <rect width="68"  height="22" rx="11" fill="#d4c49a" fill-opacity=".08" stroke="#d4c49a" stroke-width=".7" stroke-opacity=".35"/>
      <text x="34" y="15" text-anchor="middle" font-family="'Fira Code', monospace" font-size="10" fill="#d4c49a" fill-opacity=".8">Python</text>
    </g>
    <g transform="translate(140, 478)">
      <rect width="72"  height="22" rx="11" fill="#d4c49a" fill-opacity=".08" stroke="#d4c49a" stroke-width=".7" stroke-opacity=".35"/>
      <text x="36" y="15" text-anchor="middle" font-family="'Fira Code', monospace" font-size="10" fill="#d4c49a" fill-opacity=".8">PyTorch</text>
    </g>
    <g transform="translate(222, 478)">
      <rect width="64"  height="22" rx="11" fill="#d4c49a" fill-opacity=".08" stroke="#d4c49a" stroke-width=".7" stroke-opacity=".35"/>
      <text x="32" y="15" text-anchor="middle" font-family="'Fira Code', monospace" font-size="10" fill="#d4c49a" fill-opacity=".8">pandas</text>
    </g>
    <g transform="translate(296, 478)">
      <rect width="92"  height="22" rx="11" fill="#d4c49a" fill-opacity=".08" stroke="#d4c49a" stroke-width=".7" stroke-opacity=".35"/>
      <text x="46" y="15" text-anchor="middle" font-family="'Fira Code', monospace" font-size="10" fill="#d4c49a" fill-opacity=".8">scikit-learn</text>
    </g>
    <g transform="translate(398, 478)">
      <rect width="74"  height="22" rx="11" fill="#d4c49a" fill-opacity=".08" stroke="#d4c49a" stroke-width=".7" stroke-opacity=".35"/>
      <text x="37" y="15" text-anchor="middle" font-family="'Fira Code', monospace" font-size="10" fill="#d4c49a" fill-opacity=".8">MongoDB</text>
    </g>
    <g transform="translate(62, 508)">
      <rect width="62"  height="22" rx="11" fill="#d4c49a" fill-opacity=".08" stroke="#d4c49a" stroke-width=".7" stroke-opacity=".35"/>
      <text x="31" y="15" text-anchor="middle" font-family="'Fira Code', monospace" font-size="10" fill="#d4c49a" fill-opacity=".8">YOLOv8</text>
    </g>
    <g transform="translate(134, 508)">
      <rect width="66"  height="22" rx="11" fill="#d4c49a" fill-opacity=".08" stroke="#d4c49a" stroke-width=".7" stroke-opacity=".35"/>
      <text x="33" y="15" text-anchor="middle" font-family="'Fira Code', monospace" font-size="10" fill="#d4c49a" fill-opacity=".8">OpenCV</text>
    </g>
    <g transform="translate(210, 508)">
      <rect width="54"  height="22" rx="11" fill="#d4c49a" fill-opacity=".08" stroke="#d4c49a" stroke-width=".7" stroke-opacity=".35"/>
      <text x="27" y="15" text-anchor="middle" font-family="'Fira Code', monospace" font-size="10" fill="#d4c49a" fill-opacity=".8">Flask</text>
    </g>
    <g transform="translate(274, 508)">
      <rect width="58"  height="22" rx="11" fill="#d4c49a" fill-opacity=".08" stroke="#d4c49a" stroke-width=".7" stroke-opacity=".35"/>
      <text x="29" y="15" text-anchor="middle" font-family="'Fira Code', monospace" font-size="10" fill="#d4c49a" fill-opacity=".8">Plotly</text>
    </g>
    <g transform="translate(342, 508)">
      <rect width="54"  height="22" rx="11" fill="#d4c49a" fill-opacity=".08" stroke="#d4c49a" stroke-width=".7" stroke-opacity=".35"/>
      <text x="27" y="15" text-anchor="middle" font-family="'Fira Code', monospace" font-size="10" fill="#d4c49a" fill-opacity=".8">Linux</text>
    </g>

    <!-- Bottom mono tag -->
    <text x="62" y="597"
          font-family="'Fira Code', monospace"
          font-size="10.5" fill="#a3b899" opacity=".45" letter-spacing="1.2">github.com/sarathbabu123  ·  Bengaluru, India</text>
  </g>
</svg>'''

with open(os.path.join(repo_dir, 'banner.svg'), 'w', encoding='utf-8') as f:
    f.write(banner_dark)
print("✓ banner.svg")


# ─────────────────────────────────────────────────────────────────────────────
# 2. BANNER-LIGHT.SVG — same layout, cream/parchment background
# ─────────────────────────────────────────────────────────────────────────────
banner_light = banner_dark \
    .replace('stop-color="#0b1009"', 'stop-color="#f8f5ed"') \
    .replace('stop-color="#07090600"', 'stop-color="#f2ede200"') \
    .replace('stop-color="#050705"', 'stop-color="#ece7d8"') \
    .replace('fill="#070906"', 'fill="#f4f0e6"') \
    .replace("fill='#070906'", "fill='#f4f0e6'") \
    .replace('fill="#c8a96e"', 'fill="#8b6914"') \
    .replace('fill="#7da68a"', 'fill="#2d7a4f"') \
    .replace('fill="#eee9da"', 'fill="#2c2410"') \
    .replace('fill="#cec8b8"', 'fill="#3d3828"') \
    .replace('fill="#a39e92"', 'fill="#6b6452"') \
    .replace('fill="#a3b899"', 'fill="#4a6b55"') \
    .replace('fill="#d4c49a"', 'fill="#7a5c1e"')

with open(os.path.join(repo_dir, 'banner-light.svg'), 'w', encoding='utf-8') as f:
    f.write(banner_light)
print("✓ banner-light.svg")


# ─────────────────────────────────────────────────────────────────────────────
# 3. LANYARD.SVG — warm, minimal. No neon, no "SARC", no gimmicks.
#    The badge reads: DATA SCIENTIST  ·  MOOVING  ·  BENGALURU
# ─────────────────────────────────────────────────────────────────────────────
lanyard = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 560" width="440" height="560">
  <defs>
    <linearGradient id="strap" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%"  stop-color="#c8a96e"/>
      <stop offset="100%" stop-color="#7da68a"/>
    </linearGradient>

    <linearGradient id="card" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%"  stop-color="#131810"/>
      <stop offset="100%" stop-color="#090c07"/>
    </linearGradient>

    <linearGradient id="topbar" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"  stop-color="#c8a96e" stop-opacity=".25"/>
      <stop offset="100%" stop-color="#7da68a" stop-opacity=".15"/>
    </linearGradient>

    <linearGradient id="avatarRing" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%"  stop-color="#c8a96e"/>
      <stop offset="100%" stop-color="#7da68a"/>
    </linearGradient>

    <filter id="cardDrop" x="-15%" y="-10%" width="130%" height="120%">
      <feGaussianBlur stdDeviation="10" result="b"/>
      <feOffset dx="0" dy="12"/>
      <feComponentTransfer><feFuncA type="linear" slope=".35"/></feComponentTransfer>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@500&amp;family=EB+Garamond:ital,wght@0,500;0,600;1,400&amp;display=swap');
    text {{ font-family: "EB Garamond", Georgia, serif; }}
    .mono {{ font-family: "Fira Code", monospace; }}

    /* Pendulum on load, then gentle sway */
    .badge-group {{ transform-origin: 220px 0; }}
    .badge-group {{
      animation: pendulum 3.2s cubic-bezier(.4,0,.2,1) forwards,
                 sway 6s 3.2s ease-in-out infinite alternate;
    }}
    @keyframes pendulum {{
      0%   {{ rotate: -10deg; }}
      28%  {{ rotate:  7deg; }}
      54%  {{ rotate: -4deg; }}
      76%  {{ rotate:  2deg; }}
      90%  {{ rotate: -0.5deg; }}
      100% {{ rotate:  0deg; }}
    }}
    @keyframes sway {{
      from {{ rotate: -1.5deg; }}
      to   {{ rotate:  1.5deg; }}
    }}

    /* Status dot pulse */
    .status {{ animation: pulse 2.4s ease-in-out infinite; }}
    @keyframes pulse {{
      0%,100% {{ opacity:1; r:5; }}
      50%     {{ opacity:.4; r:3.5; }}
    }}
  </style>

  <g class="badge-group">
    <!-- Straps -->
    <path d="M 182 -20 L 205 108 L 214 108 L 192 -20 Z" fill="url(#strap)" opacity=".9"/>
    <path d="M 258 -20 L 235 108 L 226 108 L 248 -20 Z" fill="url(#strap)" opacity=".9"/>

    <!-- Strap text -->
    <text font-size="8.5" fill="rgba(255,255,255,.7)" letter-spacing="2"
          font-family="'Fira Code', monospace"
          transform="translate(193,18) rotate(80)">DATA SCIENTIST  ·  MOOVING  ·  BENGALURU</text>

    <!-- Metal clasp ring -->
    <circle cx="220" cy="108" r="12" fill="none" stroke="#c8b89a" stroke-width="3.5"/>
    <rect x="213" y="116" width="14" height="18" rx="3" fill="#556b5b"/>
    <circle cx="220" cy="140" r="6.5" fill="#131810" stroke="#b8c4b0" stroke-width="2.5"/>

    <!-- ── Badge card ────────────────────────────────────────────── -->
    <g transform="translate(80,148)" filter="url(#cardDrop)">
      <rect width="280" height="376" rx="16" fill="url(#card)"
            stroke="rgba(200,169,110,.3)" stroke-width="1.4"/>
      <rect width="272" height="368" x="4" y="4" rx="12"
            fill="none" stroke="rgba(255,255,255,.04)" stroke-width="1"/>

      <!-- Top accent bar -->
      <rect width="280" height="38" rx="16" fill="url(#topbar)"/>
      <rect y="22" width="280" height="16" fill="url(#topbar)" opacity=".5"/>
      <text x="140" y="24" text-anchor="middle" class="mono"
            font-size="9.5" fill="#c8a96e" letter-spacing="2.5">
        MOOVING  ·  DATA SCIENCE R&amp;D
      </text>

      <!-- Avatar ring -->
      <circle cx="140" cy="132" r="56" fill="none" stroke="url(#avatarRing)" stroke-width="2"/>
      <circle cx="140" cy="132" r="51" fill="#1a2018"/>
      <image href="data:image/png;base64,{b64_avatar}"
             x="89" y="81" width="102" height="102"
             clip-path="circle(51px at 51px 51px)"/>

      <!-- Status dot — alive, not just decorative -->
      <circle cx="182" cy="174" r="8" fill="#131810"/>
      <circle cx="182" cy="174" r="5" fill="#7da68a" class="status"/>

      <!-- Name & role -->
      <text x="140" y="214" text-anchor="middle"
            font-family="'EB Garamond',serif" font-size="22" font-weight="600" fill="#eee9da">
        Sarath Babu P
      </text>
      <text x="140" y="234" text-anchor="middle"
            font-family="'EB Garamond',serif" font-size="13" font-style="italic" fill="#a3b899">
        Data Scientist &amp; ML Engineer
      </text>
      <text x="140" y="252" text-anchor="middle" class="mono"
            font-size="10.5" fill="#c8a96e" letter-spacing=".5">@sarathbabu123</text>

      <!-- Thin rule -->
      <line x1="40" y1="265" x2="240" y2="265" stroke="#eee9da" stroke-width=".6" opacity=".1"/>

      <!-- Tags — Python, PyTorch, pandas -->
      <g transform="translate(40,276)">
        <rect width="58" height="20" rx="10"
              fill="rgba(200,169,110,.12)" stroke="#c8a96e" stroke-width=".8" stroke-opacity=".5"/>
        <text x="29" y="14" text-anchor="middle" class="mono"
              font-size="9.5" fill="#c8a96e">Python</text>
      </g>
      <g transform="translate(108,276)">
        <rect width="60" height="20" rx="10"
              fill="rgba(125,166,138,.12)" stroke="#7da68a" stroke-width=".8" stroke-opacity=".5"/>
        <text x="30" y="14" text-anchor="middle" class="mono"
              font-size="9.5" fill="#7da68a">PyTorch</text>
      </g>
      <g transform="translate(178,276)">
        <rect width="60" height="20" rx="10"
              fill="rgba(200,169,110,.12)" stroke="#c8a96e" stroke-width=".8" stroke-opacity=".5"/>
        <text x="30" y="14" text-anchor="middle" class="mono"
              font-size="9.5" fill="#c8a96e">pandas</text>
      </g>

      <!-- Barcode — minimalist, decorative -->
      <g transform="translate(36,312)">
        <!-- bars -->
        <rect x="0"   y="0" width="2.5" height="24" fill="#eee9da" opacity=".18"/>
        <rect x="4.5" y="0" width="1"   height="24" fill="#eee9da" opacity=".18"/>
        <rect x="7.5" y="0" width="3.5" height="24" fill="#eee9da" opacity=".18"/>
        <rect x="13"  y="0" width="1.5" height="24" fill="#eee9da" opacity=".18"/>
        <rect x="17"  y="0" width="4"   height="24" fill="#eee9da" opacity=".18"/>
        <rect x="23.5"y="0" width="1"   height="24" fill="#eee9da" opacity=".18"/>
        <rect x="27"  y="0" width="2.5" height="24" fill="#eee9da" opacity=".18"/>
        <rect x="32"  y="0" width="5"   height="24" fill="#eee9da" opacity=".18"/>
        <rect x="40"  y="0" width="1.5" height="24" fill="#eee9da" opacity=".18"/>
        <rect x="44"  y="0" width="3"   height="24" fill="#eee9da" opacity=".18"/>
        <rect x="50"  y="0" width="1"   height="24" fill="#eee9da" opacity=".18"/>
        <rect x="54"  y="0" width="4"   height="24" fill="#eee9da" opacity=".18"/>
        <rect x="61"  y="0" width="2"   height="24" fill="#eee9da" opacity=".18"/>
        <rect x="66"  y="0" width="3.5" height="24" fill="#eee9da" opacity=".18"/>
        <rect x="73"  y="0" width="1"   height="24" fill="#eee9da" opacity=".18"/>
        <rect x="77"  y="0" width="2.5" height="24" fill="#eee9da" opacity=".18"/>
        <rect x="82.5"y="0" width="5"   height="24" fill="#eee9da" opacity=".18"/>
        <rect x="91"  y="0" width="1.5" height="24" fill="#eee9da" opacity=".18"/>
        <rect x="95"  y="0" width="3"   height="24" fill="#eee9da" opacity=".18"/>
        <rect x="101" y="0" width="1"   height="24" fill="#eee9da" opacity=".18"/>
        <rect x="105" y="0" width="4.5" height="24" fill="#eee9da" opacity=".18"/>
        <rect x="113" y="0" width="1.5" height="24" fill="#eee9da" opacity=".18"/>
        <rect x="118" y="0" width="3.5" height="24" fill="#eee9da" opacity=".18"/>
        <rect x="125" y="0" width="1"   height="24" fill="#eee9da" opacity=".18"/>
        <rect x="129" y="0" width="2.5" height="24" fill="#eee9da" opacity=".18"/>
        <rect x="135" y="0" width="4"   height="24" fill="#eee9da" opacity=".18"/>
        <rect x="143" y="0" width="1.5" height="24" fill="#eee9da" opacity=".18"/>
        <rect x="148" y="0" width="3"   height="24" fill="#eee9da" opacity=".18"/>
        <rect x="154" y="0" width="1"   height="24" fill="#eee9da" opacity=".18"/>
        <rect x="158" y="0" width="4.5" height="24" fill="#eee9da" opacity=".18"/>
        <rect x="166" y="0" width="1.5" height="24" fill="#eee9da" opacity=".18"/>
        <rect x="170" y="0" width="3"   height="24" fill="#eee9da" opacity=".18"/>
        <rect x="176" y="0" width="1"   height="24" fill="#eee9da" opacity=".18"/>
        <rect x="180" y="0" width="3.5" height="24" fill="#eee9da" opacity=".18"/>
        <rect x="187" y="0" width="5"   height="24" fill="#eee9da" opacity=".18"/>
        <rect x="196" y="0" width="1.5" height="24" fill="#eee9da" opacity=".18"/>
        <rect x="200" y="0" width="2.5" height="24" fill="#eee9da" opacity=".18"/>
        <!-- barcode ID -->
        <text x="101" y="36" text-anchor="middle"
              font-family="'Fira Code',monospace" font-size="8.5"
              fill="#a3b899" opacity=".45" letter-spacing="1.2">DS-SB-MOOVING-2026</text>
      </g>

      <!-- Bottom shine pass — holographic shimmer -->
      <rect x="0" y="0" width="180" height="600"
            fill="linear-gradient(135deg,transparent 40%,rgba(255,255,255,.18) 50%,transparent 60%)"
            rx="16" opacity=".6"
            style="animation: shinePass 4.5s ease-in-out infinite">
        <animateTransform attributeName="transform" type="translate"
          values="-300,-300; 500,500" dur="4.5s" repeatCount="indefinite"/>
      </rect>
    </g>
  </g>
</svg>'''

with open(os.path.join(repo_dir, 'lanyard.svg'), 'w', encoding='utf-8') as f:
    f.write(lanyard)
print("✓ lanyard.svg")


# ─────────────────────────────────────────────────────────────────────────────
# 4. Remove the fake static SVG stat files — using live APIs in README instead
# ─────────────────────────────────────────────────────────────────────────────
for dead_file in ['stats.svg', 'langs.svg', 'trophies.svg']:
    p = os.path.join(repo_dir, dead_file)
    if os.path.exists(p):
        os.remove(p)
        print(f"✓ removed {dead_file} (replaced by live API)")


# ─────────────────────────────────────────────────────────────────────────────
# 5. GitHub Snake Workflow (Firefly Amber palette)
# ─────────────────────────────────────────────────────────────────────────────
workflows_dir = os.path.join(repo_dir, '.github', 'workflows')
os.makedirs(workflows_dir, exist_ok=True)

snake_yml = '''name: snake

on:
  schedule:
    - cron: "0 6 * * *"
  workflow_dispatch:
  push:
    branches: [main]

jobs:
  generate:
    permissions:
      contents: write
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: Platane/snk/svg-only@v3
        with:
          github_user_name: ${{ github.repository_owner }}
          outputs: |
            dist/snake.svg?color_snake=#d4c49a&color_dots=#0b1009,#1a2018,#2a3826,#4a6b48,#c8a96e
            dist/snake-dark.svg?palette=github-dark&color_snake=#c8a96e

      - uses: crazy-max/gh-action-github-pages@v3.1.0
        with:
          target_branch: output
          build_dir: dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
'''

with open(os.path.join(workflows_dir, 'github-snake.yml'), 'w', encoding='utf-8') as f:
    f.write(snake_yml)
print("✓ github-snake.yml")

metrics_yml = '''name: Metrics
on:
  schedule: [{cron: "0 0 * * *"}]
  workflow_dispatch:
  push: {branches: ["main"]}
jobs:
  github-metrics:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: lowlighter/metrics@latest
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          user: sarathbabu123
          template: classic
          base: header, activity, community, repositories, metadata
          config_timezone: Asia/Kolkata
          plugin_languages: yes
          plugin_languages_colors: github
          plugin_languages_limit: 8
          plugin_isocalendar: yes
          plugin_isocalendar_duration: half-year
          plugin_habits: yes
          plugin_habits_charts: yes
          plugin_habits_charts_type: classic
'''
with open(os.path.join(workflows_dir, 'metrics.yml'), 'w', encoding='utf-8') as f:
    f.write(metrics_yml)
print("✓ metrics.yml")


# ─────────────────────────────────────────────────────────────────────────────
# 6. README.md — completely original copy, no projects, no plagiarism
#    Structure: banner → lanyard → bio → what I work on → stack → stats (live
#    API) → snake → connect. Clean. Timeless.
# ─────────────────────────────────────────────────────────────────────────────
readme = '''<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)"  srcset="./banner.svg?v=7">
  <source media="(prefers-color-scheme: light)" srcset="./banner-light.svg?v=7">
  <img alt="Sarath Babu P — Data Scientist, Bengaluru" src="./banner.svg?v=7" width="100%">
</picture>

<br>

<img src="./lanyard.svg?v=7" alt="Data Scientist ID Badge — Sarath Babu P" width="360">

<br><br>

<p>
  <a href="https://www.linkedin.com/in/sarath-babu-p/">
    <img src="https://img.shields.io/badge/LinkedIn-Sarath_Babu_P-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
  </a>&nbsp;
  <a href="mailto:sarathbabuparakkadavu@gmail.com">
    <img src="https://img.shields.io/badge/Email-sarathbabuparakkadavu-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email">
  </a>&nbsp;
  <a href="https://github.com/sarathbabu123">
    <img src="https://img.shields.io/badge/GitHub-sarathbabu123-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
  </a>&nbsp;
  <a href="https://github.com/sarathbabu123/sarathbabu123">
    <img src="https://api.visitorbadge.io/api/visitors?path=sarathbabu123.sarathbabu123&label=PROFILE%20VIEWS&countColor=%23d4c49a&style=for-the-badge" alt="Profile Views">
  </a>
</p>

</div>

---

### 👋 Who I am

Data Scientist. The kind who works with real hardware data — incomplete fields, mismatched timestamps, and 300 million rows of IoT logs from devices deployed across six cities.

I specialize in machine learning systems that live in production: routing pipelines, telemetry analytics, and computer vision tools built to be trusted by people who don't care how the model works, only whether it's right.

I got into this field by building things before understanding them. That habit never left.

---

### ⚡ What I work on

| Domain | What I build |
|:---|:---|
| 🔁 **ML Pipelines** | DBSCAN-based fleet routing & route optimization, anomaly detection at scale |
| 👁️ **Computer Vision** | Inference APIs and on-device TFLite models for real-world use cases |
| 📡 **Telemetry Analytics** | Firmware degradation, hardware-recovery audits, IoT signal processing |

---

### 🛠️ Stack

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch">
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="scikit-learn">
  <img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="pandas">
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV">
  <img src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly">
  <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</p>

---

### 📊 GitHub Stats

<p align="center">
  <img src="https://github-profile-summary-cards.vercel.app/api/cards/stats?username=sarathbabu123&theme=github_dark" width="31%" alt="Stats">
  <img src="https://github-profile-summary-cards.vercel.app/api/cards/most-commit-language?username=sarathbabu123&theme=github_dark" width="31%" alt="Most Commit Language">
  <img src="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=sarathbabu123&theme=github_dark" width="31%" alt="Repos per Language">
</p>

<p align="center">
  <img src="https://github-profile-summary-cards.vercel.app/api/cards/productive-time?username=sarathbabu123&theme=github_dark&utcOffset=5.5" width="47%" alt="Productive Time">
  <img src="https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=sarathbabu123&theme=github_dark" width="47%" alt="Profile Details">
</p>

---

### 📈 Activity Graph

<p align="center">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=sarathbabu123&bg_color=0b1009&color=d4c49a&line=c8a96e&point=eee9da&area=true&hide_border=true" alt="GitHub Activity Graph" width="100%">
</p>

---

### 🐍 Contribution Snake

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)"
      srcset="https://raw.githubusercontent.com/sarathbabu123/sarathbabu123/output/snake-dark.svg">
    <source media="(prefers-color-scheme: light)"
      srcset="https://raw.githubusercontent.com/sarathbabu123/sarathbabu123/output/snake.svg">
    <img alt="GitHub contribution snake" src="https://raw.githubusercontent.com/sarathbabu123/sarathbabu123/output/snake.svg" width="100%">
  </picture>
</p>

---

<div align="center">

*small lights, patiently kept.*

</div>
'''

with open(os.path.join(repo_dir, 'README.md'), 'w', encoding='utf-8') as f:
    f.write(readme)
print("✓ README.md")
print("\nAll files generated successfully.")
