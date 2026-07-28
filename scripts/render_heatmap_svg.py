#!/usr/bin/env python3
"""
render_heatmap_svg.py - Render GitHub-style contribution heatmap
Reads contributions.json and outputs contrib-heatmap.svg
"""

import json
from datetime import datetime, timedelta

# ===== CONFIG SECTION =====
INPUT_FILE = "contributions.json"
OUTPUT_FILE = "contrib-heatmap.svg"

# Visual settings
CELL_SIZE = 12
CELL_GAP = 3
WEEKS_TO_SHOW = 53  # One year
# ==========================

def load_contributions(input_file):
    """Load contribution data from JSON"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {input_file} not found. Run fetch_contributions.py first.")
        exit(1)

def get_level_color(count):
    """Get color based on contribution count (GitHub-style)"""
    if count == 0:
        return '#ebedf0'
    elif count < 3:
        return '#9be9a8'
    elif count < 6:
        return '#40c463'
    elif count < 9:
        return '#30a14e'
    else:
        return '#216e39'

def create_heatmap_svg(data):
    """Create animated contribution heatmap SVG"""
    
    contributions = {c['date']: c['count'] for c in data['contributions']}
    
    # Calculate dimensions
    width = (WEEKS_TO_SHOW + 2) * (CELL_SIZE + CELL_GAP) + 100
    height = 7 * (CELL_SIZE + CELL_GAP) + 80
    
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '  <style>',
        '    @import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;600&amp;display=swap");',
        '    text { font-family: "Inter", sans-serif; font-size: 12px; fill: #1f2937; }',
        '    .stat-label { font-weight: 600; }',
        '    .stat-value { font-weight: 400; }',
        '    .legend-text { font-size: 10px; fill: #6b7280; }',
        '  </style>',
        f'  <rect width="{width}" height="{height}" fill="#ffffff"/>',
    ]
    
    # Title and stats
    svg_lines.append('  <text x="20" y="25" class="stat-label">GitHub Contributions</text>')
    
    total = data.get('total_contributions', 0)
    current_streak = data.get('current_streak', 0)
    longest_streak = data.get('longest_streak', 0)
    
    svg_lines.append(f'  <text x="200" y="25" class="stat-value">Total: {total} | Current: {current_streak} days | Longest: {longest_streak} days</text>')
    
    # Day labels
    days = ['Mon', 'Wed', 'Fri']
    for i, day in enumerate(days):
        y = 50 + [1, 3, 5][i] * (CELL_SIZE + CELL_GAP)
        svg_lines.append(f'  <text x="10" y="{y + CELL_SIZE - 2}" class="legend-text">{day}</text>')
    
    # Get date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=WEEKS_TO_SHOW * 7)
    
    # Draw cells
    cell_index = 0
    total_cells = WEEKS_TO_SHOW * 7
    
    for week in range(WEEKS_TO_SHOW):
        for day in range(7):
            current_date = start_date + timedelta(days=week * 7 + day)
            date_str = current_date.strftime('%Y-%m-%d')
            
            x = 50 + week * (CELL_SIZE + CELL_GAP)
            y = 45 + day * (CELL_SIZE + CELL_GAP)
            
            count = contributions.get(date_str, 0)
            color = get_level_color(count)
            
            # Animation delay
            delay = (cell_index / total_cells) * 2.0  # 2 second animation
            
            svg_lines.append(
                f'  <rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" '
                f'fill="{color}" rx="2">'
                f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.3f}s" dur="0.05s" fill="freeze"/>'
                f'<title>{date_str}: {count} contributions</title>'
                f'</rect>'
            )
            
            cell_index += 1
    
    # Legend
    legend_x = 50
    legend_y = height - 20
    
    svg_lines.append(f'  <text x="{legend_x}" y="{legend_y}" class="legend-text">Less</text>')
    
    colors = ['#ebedf0', '#9be9a8', '#40c463', '#30a14e', '#216e39']
    for i, color in enumerate(colors):
        x = legend_x + 35 + i * (CELL_SIZE + 3)
        svg_lines.append(f'  <rect x="{x}" y="{legend_y - 10}" width="{CELL_SIZE}" height="{CELL_SIZE}" fill="{color}" rx="2"/>')
    
    svg_lines.append(f'  <text x="{legend_x + 35 + len(colors) * (CELL_SIZE + 3) + 5}" y="{legend_y}" class="legend-text">More</text>')
    
    svg_lines.append('</svg>')
    
    svg_content = '\n'.join(svg_lines)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print(f"✓ Created: {OUTPUT_FILE}")
    print(f"  Size: {width}x{height}px")
    print(f"  Days: {total_cells}")

if __name__ == "__main__":
    print(f"Loading {INPUT_FILE}...")
    data = load_contributions(INPUT_FILE)
    
    print("Rendering heatmap...")
    create_heatmap_svg(data)
    
    print(f"\n✓ Done! Preview {OUTPUT_FILE} in a browser")
