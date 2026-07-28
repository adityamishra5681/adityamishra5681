#!/usr/bin/env python3
"""
make_ascii_svg.py - Convert image to animated ASCII art SVG
Reads source-prepped.png and outputs avi-ascii.svg
"""

import numpy as np
from PIL import Image, ImageEnhance

# ===== CONFIG SECTION - TUNE THIS =====
INPUT_IMAGE = "source-prepped.png"
OUTPUT_SVG = "avi-ascii.svg"
WIDTH = 80
CONTRAST = 1.6
GAMMA = 1.15
WHITE_FLOOR = 26
STATIC = 0
BACKGROUND = "#111722"
TEXT_COLOR = "#d9d1d9"
ACCENT_COLOR = "#3fb950"
# ======================================

ASCII_CHARS = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"


def brightness_to_ascii(brightness):
    index = int(brightness / 255 * (len(ASCII_CHARS) - 1))
    return ASCII_CHARS[index]


def image_to_ascii(image_path, width=80):
    print(f"Loading image: {image_path}")
    img = Image.open(image_path).convert("L")

    if CONTRAST != 1.0:
        img = ImageEnhance.Contrast(img).enhance(CONTRAST)

    if GAMMA != 1.0:
        img_array = np.array(img).astype(float)
        img_array = 255 * np.power(img_array / 255, 1 / GAMMA)
        img = Image.fromarray(img_array.astype(np.uint8))

    if WHITE_FLOOR > 0:
        img_array = np.array(img)
        img_array = np.maximum(img_array, WHITE_FLOOR)
        img = Image.fromarray(img_array)

    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.55)
    img = img.resize((width, height))

    pixels = np.array(img)
    return ["".join(brightness_to_ascii(pixel) for pixel in row) for row in pixels]


def escape_xml(text):
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def create_animated_svg(ascii_grid, output_file, static=False):
    font_size = 12
    line_height = 13
    char_width = 7
    width = max(320, len(ascii_grid[0]) * char_width + 90)
    height = 72 + len(ascii_grid) * line_height + 24

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{int(width)}" height="{int(height)}" viewBox="0 0 {int(width)} {int(height)}">',
        '  <defs>',
        '    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">',
        f'      <stop offset="0" stop-color="{BACKGROUND}"/>',
        '      <stop offset="1" stop-color="#0d1117"/>',
        '    </linearGradient>',
        '  </defs>',
        f'  <rect width="{int(width)}" height="{int(height)}" rx="14" fill="url(#bg)"/>',
        f'  <rect x="0.8" y="0.8" width="{int(width) - 1.6}" height="{int(height) - 1.6}" rx="14" fill="none" stroke="#30363d" stroke-width="1"/>',
        f'  <line x1="0" y1="38" x2="{int(width)}" y2="38" stroke="#30363d"/>',
        '  <circle cx="20" cy="15" r="5" fill="#ff5f56"/>',
        '  <circle cx="36" cy="15" r="5" fill="#ffbd2e"/>',
        '  <circle cx="52" cy="15" r="5" fill="#27c93f"/>',
        f'  <text x="{int(width) / 2:.1f}" y="19" fill="#7d8590" font-size="12" text-anchor="middle" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">aditya@github: ~$ ./portrait.sh</text>',
    ]

    for idx, row in enumerate(ascii_grid):
        y = 48 + idx * line_height
        line_text = f"> {row}"
        svg_lines.extend([
            f'  <g opacity="0">',
            f'    <animate attributeName="opacity" from="0" to="1" begin="{0.08 + idx * 0.06:.2f}s" dur="0.16s" fill="freeze"/>',
            f'    <text x="18" y="{y}" fill="{TEXT_COLOR}" font-size="{font_size}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">{escape_xml(line_text)}</text>',
            '  </g>',
        ])

    svg_lines.append('</svg>')
    svg_content = "\n".join(svg_lines)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"✓ Created: {output_file}")
    print(f"  Size: {int(width)}x{int(height)}px")
    print(f"  Rows: {len(ascii_grid)}")


if __name__ == "__main__":
    print(f"Converting {INPUT_IMAGE} to ASCII art...")
    ascii_grid = image_to_ascii(INPUT_IMAGE, WIDTH)
    print("\nCreating SVG...")
    create_animated_svg(ascii_grid, OUTPUT_SVG, static=STATIC)
    print("\n✓ Done! Preview with:")
    print(f"  Open {OUTPUT_SVG} in a browser")
