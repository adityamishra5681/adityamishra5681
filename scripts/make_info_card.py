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
    """Generate the info card SVG"""
    
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '  <style>',
        '    @import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;600&amp;display=swap");',
        '    .label { font-family: "Inter", sans-serif; font-size: ' + str(FONT_SIZE) + 'px; font-weight: 600; fill: #374151; }',
        '    .value { font-family: "Inter", sans-serif; font-size: ' + str(FONT_SIZE) + 'px; font-weight: 400; fill: #1f2937; }',
        '    .host { font-family: "Inter", monospace; font-size: 11px; fill: #6b7280; }',
        '  </style>',
        f'  <rect width="{W}" height="{H}" fill="#ffffff" stroke="#e5e7eb" stroke-width="1"/>',
    ]
    
    y = PADDING + 15
    
    for label, value in ROWS:
        if label == "" and value == "":
            # Empty row - just add spacing
            y += LINE_HEIGHT * 0.5
            continue
        
        if label:
            # Label: value format
            svg_lines.append(f'  <text x="{PADDING}" y="{y}" class="label">{escape_xml(label)}:</text>')
            svg_lines.append(f'  <text x="{PADDING + 110}" y="{y}" class="value">{escape_xml(value)}</text>')
        else:
            # Just value (for longer text)
            svg_lines.append(f'  <text x="{PADDING}" y="{y}" class="value">{escape_xml(value)}</text>')
        
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
