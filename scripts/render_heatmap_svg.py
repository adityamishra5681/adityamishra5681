#!/usr/bin/env python3
"""
render_heatmap_svg.py - Render a frex-inspired contribution heatmap.
"""

import json
from datetime import datetime, timedelta

# ===== CONFIG SECTION =====
INPUT_FILE = "contributions.json"
OUTPUT_FILE = "contrib-heatmap.svg"

# Visual settings
CELL_SIZE = 12
CELL_GAP = 3
WEEKS_TO_SHOW = 53
# ==========================


def load_contributions(input_file):
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {input_file} not found. Run fetch_contributions.py first.")
        exit(1)


def get_level_color(count):
    if count == 0:
        return "#161b22"
    elif count < 3:
        return "#1f6feb"
    elif count < 6:
        return "#3fb950"
    elif count < 9:
        return "#2ea043"
    else:
        return "#26a641"


def create_heatmap_svg(data):
    contributions = {c["date"]: c["count"] for c in data["contributions"]}

    width = 869
    height = 265
    start_date = datetime.now() - timedelta(days=WEEKS_TO_SHOW * 7)
    day_labels = ["Mon", "Wed", "Fri"]

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        '<style>@keyframes cell { 0% { opacity: 0; transform: translateY(-6px); } 100% { opacity: 1; transform: translateY(0); } } .c { opacity: 0; animation: cell 0.42s cubic-bezier(.2,.8,.2,1) both; }</style>',
        '<defs><linearGradient id="hbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d1420"/><stop offset="1" stop-color="#0a0e14"/></linearGradient></defs>',
        f'<rect width="{width}" height="{height}" rx="12" fill="url(#hbg)"/>',
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="12" fill="none" stroke="#1f6feb" stroke-width="1" stroke-opacity="0.55"/>',
        f'<line x1="0" y1="30" x2="{width}" y2="30" stroke="#1f6feb" stroke-opacity="0.35"/>',
        '<circle cx="22" cy="15.0" r="5" fill="#ff5f56"/>',
        '<circle cx="38" cy="15.0" r="5" fill="#ffbd2e"/>',
        '<circle cx="54" cy="15.0" r="5" fill="#27c93f"/>',
        f'<text x="{width / 2:.1f}" y="19.0" fill="#7d8590" font-size="12" text-anchor="middle">aditya@github: ~/contributions --graph</text>',
    ]

    total = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)
    svg_lines.append(f'<text x="52" y="44" fill="#7d8590" font-size="10">{(start_date + timedelta(days=30)).strftime("%b")}</text>')
    for idx, month_name in enumerate(["Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun"]):
        x = 52 + idx * 60
        svg_lines.append(f'<text x="{x}" y="44" fill="#7d8590" font-size="10">{month_name}</text>')

    for i, day in enumerate(day_labels):
        y = 74.4 + i * 30
        svg_lines.append(f'<text x="22" y="{y}" fill="#7d8590" font-size="9">{day}</text>')

    cell_index = 0
    total_cells = WEEKS_TO_SHOW * 7
    for week in range(WEEKS_TO_SHOW):
        for day in range(7):
            current_date = start_date + timedelta(days=week * 7 + day)
            date_str = current_date.strftime("%Y-%m-%d")
            x = 52 + week * (CELL_SIZE + CELL_GAP)
            y = 60 + day * (CELL_SIZE + CELL_GAP)
            count = contributions.get(date_str, 0)
            color = get_level_color(count)
            delay = (cell_index / total_cells) * 0.9
            svg_lines.append(
                f'<rect class="c" x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2.5" fill="{color}" style="animation-delay:{delay:.3f}s"><title>{date_str}: {count} contributions</title></rect>'
            )
            cell_index += 1

    legend_x = 52
    legend_y = height - 28
    svg_lines.append(f'<text x="{legend_x}" y="{legend_y}" fill="#7d8590" font-size="10">Less</text>')
    colors = ["#161b22", "#1f6feb", "#3fb950", "#2ea043", "#26a641"]
    for i, color in enumerate(colors):
        x = legend_x + 32 + i * (CELL_SIZE + 3)
        svg_lines.append(f'<rect x="{x}" y="{legend_y - 10}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2.5" fill="{color}"/>')
    svg_lines.append(f'<text x="{legend_x + 32 + len(colors) * (CELL_SIZE + 3) + 5}" y="{legend_y}" fill="#7d8590" font-size="10">More</text>')
    svg_lines.append(f'<text x="{legend_x + 190}" y="{legend_y}" fill="#7d8590" font-size="10">Total: {total} · Streak: {current_streak}/{longest_streak}</text>')
    svg_lines.append('</svg>')

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))

    print(f"✓ Created: {OUTPUT_FILE}")
    print(f"  Size: {width}x{height}px")


if __name__ == "__main__":
    print(f"Loading {INPUT_FILE}...")
    data = load_contributions(INPUT_FILE)
    print("Rendering heatmap...")
    create_heatmap_svg(data)
    print(f"\n✓ Done! Preview {OUTPUT_FILE} in a browser")
