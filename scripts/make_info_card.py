#!/usr/bin/env python3
"""
make_info_card.py - Generate info card SVG with experience, stack, and highlights
"""

# ===== CONFIG SECTION - EDIT YOUR INFO HERE =====
ROWS = [
    ("Education", "BCA (Hons.) in Data Science & AI"),
    ("University", "Techno India University, Kolkata"),
    ("Focus", "AI/ML · Web Development · Data Science"),
    ("", ""),  # Empty row for spacing
    ("Languages", "Python · JavaScript · SQL · Java"),
    ("Web Stack", "HTML · CSS · JavaScript · React"),
    ("Data Stack", "pandas · NumPy · scikit-learn · OpenCV"),
    ("Tools", "VS Code · Jupyter · Git · Power BI"),
    ("Databases", "PostgreSQL · MySQL · SQLite"),
    ("", ""),  # Empty row for spacing
    ("Current Work", "Portfolio site · ML experiments · profile automation"),
    ("Learning", "MLOps · Computer Vision · NLP · Cloud"),
    ("Highlights", "GitHub profile automation · clean UI builds · data storytelling"),
]

HOST = "github.com/adityamishra5681"
OUTPUT_FILE = "info-card.svg"

# Layout settings
W = 490
H = 404  # Match rendered portrait height - adjust if content overflows
PADDING = 20
FONT_SIZE = 13
LINE_HEIGHT = 22
# =========================================

def create_info_card():
    """Generate the info card SVG with a dark terminal-inspired reveal."""
    
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '  <defs>',
        '    <linearGradient id="panel" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#030712"/>',
        '      <stop offset="100%" stop-color="#111827"/>',
        '    </linearGradient>',
        '  </defs>',
        '  <style>',
        '    @import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;600&amp;display=swap");',
        '    .label { font-family: "Inter", sans-serif; font-size: ' + str(FONT_SIZE) + 'px; font-weight: 600; fill: #f3f4f6; }',
        '    .value { font-family: "Inter", sans-serif; font-size: ' + str(FONT_SIZE) + 'px; font-weight: 400; fill: #e5e7eb; }',
        '    .host { font-family: "Inter", monospace; font-size: 11px; fill: #9ca3af; }',
        '    .line { stroke: #374151; stroke-width: 0.8; opacity: 0.75; }',
        '  </style>',
        f'  <rect width="{W}" height="{H}" rx="18" fill="url(#panel)" stroke="#1f2937" stroke-width="1.2"/>',
        f'  <rect x="12" y="12" width="{W - 24}" height="{H - 24}" rx="14" fill="none" stroke="#374151" stroke-width="0.8" opacity="0.75"/>',
        f'  <line x1="24" y1="28" x2="{W - 24}" y2="28" class="line"/>',
        f'  <line x1="24" y1="{H - 28}" x2="{W - 24}" y2="{H - 28}" class="line"/>',
        f'  <text x="{PADDING}" y="{PADDING + 10}" class="host">SYSTEM PROFILE</text>',
    ]
    
    y = PADDING + 15
    
    for idx, (label, value) in enumerate(ROWS):
        if label == "" and value == "":
            # Empty row - just add spacing
            y += LINE_HEIGHT * 0.5
            continue
        
        row_group = [
            f'  <g opacity="0">',
            f'    <animate attributeName="opacity" from="0" to="1" begin="{0.08 + idx * 0.06:.2f}s" dur="0.18s" fill="freeze"/>',
            f'    <line x1="{PADDING}" y1="{y + 4}" x2="{PADDING + 8}" y2="{y + 4}" stroke="#9ca3af" stroke-width="0.8" opacity="0.6"/>',
        ]
        if label:
            # Label: value format
            row_group.append(f'    <text x="{PADDING + 16}" y="{y}" class="label">{escape_xml(label)}:</text>')
            row_group.append(f'    <text x="{PADDING + 130}" y="{y}" class="value">{escape_xml(value)}</text>')
        else:
            # Just value (for longer text)
            row_group.append(f'    <text x="{PADDING + 16}" y="{y}" class="value">{escape_xml(value)}</text>')
        row_group.append('  </g>')
        svg_lines.extend(row_group)
        
        y += LINE_HEIGHT
    
    # Add host at bottom
    svg_lines.append(f'  <text x="{W - PADDING}" y="{H - PADDING}" text-anchor="end" class="host">{escape_xml(HOST)}</text>')
    
    svg_lines.append('</svg>')
    
    svg_content = '\n'.join(svg_lines)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print(f"✓ Created: {OUTPUT_FILE}")
    print(f"  Size: {W}x{H}px")
    print(f"  Rows: {len([r for r in ROWS if r[0] or r[1]])}")

def escape_xml(text):
    """Escape special XML characters"""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&apos;'))

if __name__ == "__main__":
    create_info_card()
