#!/usr/bin/env python3
"""
make_info_card.py - Generate a terminal-style info card inspired by frex/info-card.svg
"""

# ===== CONFIG SECTION - EDIT YOUR INFO HERE =====
ROWS = [
    ("Education", "BCA (Hons.) in Data Science & AI"),
    ("University", "Techno India University, Kolkata"),
    ("Focus", "AI/ML • Web Development • Data Science"),
    ("Languages", "Python • JavaScript • SQL • Java"),
    ("Stack", "HTML • CSS • React • pandas"),
    ("Current", "Portfolio • ML experiments • automation"),
]

PROGRESS = [
    ("Python", 95),
    ("JavaScript", 80),
    ("ML/AI", 88),
    ("Cloud", 62),
]

HOST = "github.com/adityamishra5681"
OUTPUT_FILE = "info-card.svg"

W = 480
H = 390
PADDING = 20
# =========================================


def create_info_card():
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        '<defs>',
        '<linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">',
        '<stop offset="0" stop-color="#111722"/>',
        '<stop offset="1" stop-color="#0d1117"/>',
        '</linearGradient>',
        '</defs>',
        f'<rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>',
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="#30363d"/>',
        f'<line x1="0" y1="30" x2="{W}" y2="30" stroke="#30363d"/>',
        '<circle cx="20" cy="15.0" r="5" fill="#ff5f56"/>',
        '<circle cx="36" cy="15.0" r="5" fill="#ffbd2e"/>',
        '<circle cx="52" cy="15.0" r="5" fill="#27c93f"/>',
        f'<text x="{W / 2:.1f}" y="19.0" fill="#7d8590" font-size="12" text-anchor="middle">aditya@github: ~$ neofetch</text>',
    ]

    svg_lines.append('<g transform="translate(0,5)">')
    svg_lines.extend(build_reveal_text("Aditya Mishra", 20, 60.0, "#3fb950", 22, 800, 0.05))
    svg_lines.extend(build_reveal_text("Data Science & AI • Web Development", 20, 82.0, "#d9d1d9", 12, 400, 0.45))

    y = 108
    for idx, (label, value) in enumerate(ROWS):
        begin = 0.7 + idx * 0.07
        svg_lines.append(f'<text x="{PADDING}" y="{y:.1f}" font-size="12" font-weight="600" fill="#c9d1d9">')
        svg_lines.append(f'<tspan fill="#3fb950">{escape_xml(label.lower())}: </tspan>')
        svg_lines.append(f'<tspan fill="#f0f6fc">{escape_xml(value)}</tspan>')
        svg_lines.append('</text>')
        y += 20

    progress_y = y + 10
    svg_lines.append(f'<text x="{PADDING}" y="{progress_y:.1f}" font-size="12" font-weight="600" fill="#c9d1d9">skills</text>')
    for i, (name, pct) in enumerate(PROGRESS):
        bar_y = progress_y + 18 + i * 18
        svg_lines.extend([
            f'<text x="{PADDING}" y="{bar_y:.1f}" font-size="11" fill="#7d8590">{escape_xml(name)}</text>',
            f'<rect x="{PADDING + 72}" y="{bar_y - 8:.1f}" width="140" height="7" rx="3.5" fill="#0f172a" stroke="#1f2937" stroke-width="1"/>',
            f'<rect x="{PADDING + 72}" y="{bar_y - 8:.1f}" width="{int(140 * pct / 100)}" height="7" rx="3.5" fill="#3fb950"/>',
            f'<text x="{PADDING + 224}" y="{bar_y:.1f}" font-size="11" fill="#7d8590">{pct}%</text>',
        ])

    svg_lines.append(f'<text x="{PADDING}" y="{H - 18:.1f}" fill="#7d8590" font-size="11">{escape_xml(HOST)}</text>')
    svg_lines.append('</g>')
    svg_lines.append('</svg>')

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))

    print(f"✓ Created: {OUTPUT_FILE}")
    print(f"  Size: {W}x{H}px")


def build_reveal_text(text, x, y, fill, size, weight, begin):
    parts = [f'<text x="{x}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" fill="{fill}">']
    for idx, ch in enumerate(text):
        ch_text = escape_xml(ch)
        if ch == " ":
            ch_text = "&#160;"
        start = begin + idx * 0.05
        parts.append(f'<tspan opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{start:.2f}s" dur="0.01s" fill="freeze"/>{ch_text}</tspan>')
    parts.append('</text>')
    return parts


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
