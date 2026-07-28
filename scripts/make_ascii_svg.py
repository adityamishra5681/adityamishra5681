#!/usr/bin/env python3
"""
make_ascii_svg.py - Convert image to animated ASCII art SVG
Reads source-prepped.png and outputs avi-ascii.svg
"""

import numpy as np
from PIL import Image, ImageEnhance
import sys

# ===== CONFIG SECTION - TUNE THIS =====
INPUT_IMAGE = "source-prepped.png"
OUTPUT_SVG = "avi-ascii.svg"
WIDTH = 80                    # ASCII art width in characters
CONTRAST = 1.6                # Image contrast boost (1.0 = no change)
GAMMA = 1.15                  # Gamma correction (1.0 = no change, >1 = brighter)
WHITE_FLOOR = 26              # Minimum brightness (0-255, raise to avoid pure black)
STATIC = 0                    # Set to 1 to render final frame without animation
BACKGROUND = "#030712"
TEXT_COLOR = "#F9FAFB"
ACCENT_COLOR = "#6B7280"
# ======================================

# ASCII characters from darkest to brightest
ASCII_CHARS = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

def brightness_to_ascii(brightness):
    """Map brightness (0-255) to ASCII character"""
    index = int(brightness / 255 * (len(ASCII_CHARS) - 1))
    return ASCII_CHARS[index]

def image_to_ascii(image_path, width=80):
    """Convert image to ASCII art grid"""
    
    print(f"Loading image: {image_path}")
    img = Image.open(image_path)
    
    # Convert to grayscale
    img = img.convert('L')
    
    # Apply contrast enhancement
    if CONTRAST != 1.0:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(CONTRAST)
    
    # Apply gamma correction
    if GAMMA != 1.0:
        img_array = np.array(img).astype(float)
        img_array = 255 * np.power(img_array / 255, 1/GAMMA)
        img = Image.fromarray(img_array.astype(np.uint8))
    
    # Apply white floor
    if WHITE_FLOOR > 0:
        img_array = np.array(img)
        img_array = np.maximum(img_array, WHITE_FLOOR)
        img = Image.fromarray(img_array)
    
    # Calculate height to maintain aspect ratio
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.55)  # 0.55 to adjust for char aspect ratio
    
    print(f"Resizing to {width}x{height} characters")
    img = img.resize((width, height))
    
    # Convert to ASCII
    pixels = np.array(img)
    ascii_grid = []
    
    for row in pixels:
        ascii_row = ''.join([brightness_to_ascii(pixel) for pixel in row])
        ascii_grid.append(ascii_row)
    
    return ascii_grid

def create_animated_svg(ascii_grid, output_file, static=False):
    """Create SVG with a dark terminal-style line-by-line reveal."""
    
    font_size = 12
    char_width = font_size * 0.6
    line_height = font_size * 1.2
    
    width = len(ascii_grid[0]) * char_width + 60
    height = len(ascii_grid) * line_height + 80
    
    # Calculate total characters for animation
    total_chars = sum(len(row) for row in ascii_grid)
    
    # Animation duration in seconds (typing effect)
    duration = 3.2  # 3.2 seconds to type everything
    
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{int(width)}" height="{int(height)}" viewBox="0 0 {int(width)} {int(height)}">',
        '  <defs>',
        '    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">',
        f'      <stop offset="0%" stop-color="{BACKGROUND}"/>',
        '      <stop offset="100%" stop-color="#111827"/>',
        '    </linearGradient>',
        '  </defs>',
        '  <style>',
        '    @import url("https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400&amp;display=swap");',
        '    text { font-family: "Courier Prime", monospace; font-size: ' + str(font_size) + 'px; fill: ' + TEXT_COLOR + '; }',
        '    .scan { stroke: #4b5563; stroke-width: 1; stroke-dasharray: 6 6; opacity: 0.35; }',
        '    .prompt { fill: ' + ACCENT_COLOR + '; }',
        '  </style>',
        f'  <rect width="{int(width)}" height="{int(height)}" fill="url(#bg)"/>',
        f'  <rect x="10" y="10" width="{int(width) - 20}" height="{int(height) - 20}" rx="18" fill="none" stroke="#1f2937" stroke-width="1.2"/>',
        f'  <line x1="22" y1="22" x2="{int(width) - 22}" y2="22" class="scan"/>',
        f'  <line x1="22" y1="{int(height) - 22}" x2="{int(width) - 22}" y2="{int(height) - 22}" class="scan"/>',
        f'  <text x="22" y="20" class="prompt">&gt;</text>',
    ]
    
    char_index = 0
    
    for row_idx, row in enumerate(ascii_grid):
        y = 30 + row_idx * line_height
        
        row_group = [
            f'  <g opacity="0">',
            f'    <animate attributeName="opacity" from="0" to="1" begin="{row_idx * 0.12:.3f}s" dur="0.2s" fill="freeze"/>',
            f'    <line x1="20" y1="{y + 3:.1f}" x2="34" y2="{y + 3:.1f}" stroke="{ACCENT_COLOR}" stroke-width="0.8" opacity="0.45"/>',
        ]
        
        for col_idx, char in enumerate(row):
            if char == ' ':
                char_index += 1
                continue
            
            x = 40 + col_idx * char_width
            
            # Escape special XML characters
            display_char = char
            if char == '<':
                display_char = '&lt;'
            elif char == '>':
                display_char = '&gt;'
            elif char == '&':
                display_char = '&amp;'
            
            if static or STATIC:
                row_group.append(f'    <text x="{x:.1f}" y="{y:.1f}">{display_char}</text>')
            else:
                delay = (row_idx * 0.12) + ((char_index / total_chars) * 0.08)
                row_group.append(
                    f'    <text x="{x:.1f}" y="{y:.1f}" opacity="0">'
                    f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.3f}s" dur="0.04s" fill="freeze"/>'
                    f'{display_char}'
                    f'</text>'
                )
            
            char_index += 1
        
        row_group.append('  </g>')
        svg_lines.extend(row_group)
    
    svg_lines.append('</svg>')
    
    svg_content = '\n'.join(svg_lines)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print(f"✓ Created: {output_file}")
    print(f"  Size: {int(width)}x{int(height)}px")
    print(f"  Characters: {total_chars}")
    if not static and not STATIC:
        print(f"  Animation: {duration}s typing effect")

if __name__ == "__main__":
    print(f"Converting {INPUT_IMAGE} to ASCII art...")
    ascii_grid = image_to_ascii(INPUT_IMAGE, WIDTH)
    
    print(f"\nCreating SVG...")
    create_animated_svg(ascii_grid, OUTPUT_SVG, static=STATIC)
    
    print(f"\n✓ Done! Preview with:")
    print(f"  Open {OUTPUT_SVG} in a browser")
