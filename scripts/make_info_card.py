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

PROGRESS = [
    ("Python", 95),
    ("JavaScript", 80),
    ("ML / AI", 88),
    ("Cloud", 62),
]

HOST = "github.com/adityamishra5681"
OUTPUT_FILE = "info-card.svg"

W = 490
H = 430
PADDING = 24
LABEL_COLUMN = 118
VALUE_COLUMN = 158
FONT_SIZE = 12
LINE_HEIGHT = 22
TITLE_Y = 24
BODY_TOP = 56
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
        '    @import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;display=swap");',
        '    .label { font-family: "Inter", sans-serif; font-size: ' + str(FONT_SIZE) + 'px; font-weight: 600; fill: #f9fafb; }',
        '    .value { font-family: "Inter", sans-serif; font-size: ' + str(FONT_SIZE) + 'px; font-weight: 400; fill: #d1d5db; }',
        '    .muted { font-family: "Inter", monospace; font-size: 10.5px; fill: #9ca3af; }',
        '    .title { font-family: "Inter", sans-serif; font-size: 16px; font-weight: 600; fill: #f3f4f6; }',
        '    .bar-bg { fill: #0f172a; stroke: #1f2937; stroke-width: 1; }',
        '    .bar-fill { fill: #3fb950; }',
        '  </style>',
        f'  <rect width="{W}" height="{H}" rx="16" fill="url(#panel)" stroke="#30363d" stroke-width="1"/>',
        f'  <rect x="0.8" y="0.8" width="{W - 1.6}" height="{H - 1.6}" rx="16" fill="none" stroke="#374151" stroke-width="0.8"/>',
        '  <line x1="0" y1="38" x2="490" y2="38" stroke="#30363d"/>',
        '  <circle cx="20" cy="15" r="5" fill="#ff5f56"/>',
        '  <circle cx="36" cy="15" r="5" fill="#ffbd2e"/>',
        '  <circle cx="52" cy="15" r="5" fill="#27c93f"/>',
        f'  <text x="{W / 2:.1f}" y="19" text-anchor="middle" class="muted">aditya@github: ~$ ./info.sh</text>',
        f'  <text x="{PADDING}" y="{TITLE_Y}" class="title">Profile Snapshot</text>',
        f'  <line x1="{PADDING}" y1="{TITLE_Y + 6}" x2="{W - PADDING}" y2="{TITLE_Y + 6}" stroke="#1f2937" stroke-width="0.8"/>',
    ]

    y = BODY_TOP
    for idx, (label, value) in enumerate(ROWS):
        if label == "" and value == "":
            y += LINE_HEIGHT * 0.5
            continue

        svg_lines.extend([
            f'  <g opacity="0">',
            f'    <animate attributeName="opacity" from="0" to="1" begin="{0.06 + idx * 0.04:.2f}s" dur="0.16s" fill="freeze"/>',
            f'    <text x="{PADDING}" y="{y}" class="label">{escape_xml(label)}:</text>',
            f'    <text x="{PADDING + VALUE_COLUMN}" y="{y}" class="value">{escape_xml(value)}</text>',
            '  </g>',
        ])
        y += LINE_HEIGHT

    progress_y = y + 8
    svg_lines.append(f'  <text x="{PADDING}" y="{progress_y}" class="label">Skills</text>')
    for i, (name, pct) in enumerate(PROGRESS):
        bar_y = progress_y + 14 + i * 18
        svg_lines.extend([
            f'  <text x="{PADDING}" y="{bar_y}" class="muted">{escape_xml(name)}</text>',
            f'  <rect x="{PADDING + 76}" y="{bar_y - 8}" width="140" height="7" rx="3.5" class="bar-bg"/>',
            f'  <rect x="{PADDING + 76}" y="{bar_y - 8}" width="{int(140 * pct / 100)}" height="7" rx="3.5" class="bar-fill"/>',
            f'  <text x="{PADDING + 222}" y="{bar_y}" class="muted">{pct}%</text>',
        ])

    svg_lines.append(f'  <text x="{W - PADDING}" y="{H - PADDING}" text-anchor="end" class="muted">{escape_xml(HOST)}</text>')
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
