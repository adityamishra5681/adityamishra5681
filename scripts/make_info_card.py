#!/usr/bin/env python3
"""
make_info_card.py - Generate info card SVG with experience, stack, and highlights
"""

# ===== CONFIG SECTION - EDIT YOUR INFO HERE =====
ROWS = [
    ("Education", "BCA (Hons.) in Data Science & AI"),
    ("University", "Techno India University, Kolkata"),
    ("Focus", "AI/ML · Web Development · Data Science"),
    ("", ""),
    ("Languages", "Python · JavaScript · SQL · Java"),
    ("Web Stack", "HTML · CSS · JavaScript · React"),
    ("Data Stack", "pandas · NumPy · scikit-learn · OpenCV"),
    ("Tools", "VS Code · Jupyter · Git · Power BI"),
    ("Databases", "PostgreSQL · MySQL · SQLite"),
    ("", ""),
    ("Current Work", "Portfolio site · ML experiments · profile automation"),
    ("Learning", "MLOps · Computer Vision · NLP · Cloud"),
    ("Highlights", "GitHub profile automation · clean UI builds · data storytelling"),
]

HOST = "github.com/adityamishra5681"
OUTPUT_FILE = "info-card.svg"

W = 490
H = 430
PADDING = 24
LABEL_COLUMN = 118
VALUE_COLUMN = 150
FONT_SIZE = 12
LINE_HEIGHT = 22
# =========================================


def create_info_card():
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '  <defs>',
        '    <linearGradient id="panel" x1="0" y1="0" x2="1" y2="1">',
        '      <stop offset="0" stop-color="#030712"/>',
        '      <stop offset="1" stop-color="#111827"/>',
        '    </linearGradient>',
        '  </defs>',
        '  <style>',
        '    @import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;600&amp;display=swap");',
        '    .label { font-family: "Inter", sans-serif; font-size: ' + str(FONT_SIZE) + 'px; font-weight: 600; fill: #f3f4f6; }',
        '    .value { font-family: "Inter", sans-serif; font-size: ' + str(FONT_SIZE) + 'px; font-weight: 400; fill: #e5e7eb; }',
        '    .host { font-family: "Inter", monospace; font-size: 11px; fill: #9ca3af; }',
        '  </style>',
        f'  <rect width="{W}" height="{H}" rx="16" fill="url(#panel)" stroke="#30363d" stroke-width="1"/>',
        f'  <rect x="0.8" y="0.8" width="{W - 1.6}" height="{H - 1.6}" rx="16" fill="none" stroke="#374151" stroke-width="0.8"/>',
        '  <line x1="0" y1="38" x2="490" y2="38" stroke="#30363d"/>',
        '  <circle cx="20" cy="15" r="5" fill="#ff5f56"/>',
        '  <circle cx="36" cy="15" r="5" fill="#ffbd2e"/>',
        '  <circle cx="52" cy="15" r="5" fill="#27c93f"/>',
        f'  <text x="{W / 2:.1f}" y="19" text-anchor="middle" class="host">aditya@github: ~$ ./info.sh</text>',
    ]

    y = 54
    for idx, (label, value) in enumerate(ROWS):
        if label == "" and value == "":
            y += LINE_HEIGHT * 0.5
            continue

        svg_lines.extend([
            f'  <g opacity="0">',
            f'    <animate attributeName="opacity" from="0" to="1" begin="{0.08 + idx * 0.045:.2f}s" dur="0.16s" fill="freeze"/>',
            f'    <text x="{PADDING}" y="{y}" class="label">{escape_xml(label)}:</text>',
            f'    <text x="{PADDING + VALUE_COLUMN}" y="{y}" class="value">{escape_xml(value)}</text>',
            '  </g>',
        ])
        y += LINE_HEIGHT

    svg_lines.append(f'  <text x="{W - PADDING}" y="{H - PADDING}" text-anchor="end" class="host">{escape_xml(HOST)}</text>')
    svg_lines.append('</svg>')

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))

    print(f"✓ Created: {OUTPUT_FILE}")
    print(f"  Size: {W}x{H}px")
    print(f"  Rows: {len([r for r in ROWS if r[0] or r[1]])}")


def escape_xml(text):
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


if __name__ == "__main__":
    create_info_card()
