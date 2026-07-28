#!/usr/bin/env python3
"""
make_ascii_svg.py - Convert image to animated ASCII art SVG
Reads source-prepped.png and outputs avi-ascii.svg
"""

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

# ===== CONFIG SECTION - TUNE THIS =====
INPUT_IMAGE = "source-prepped.png"
OUTPUT_SVG = "avi-ascii.svg"
WIDTH = 84
CONTRAST = 2.1
GAMMA = 1.18
WHITE_FLOOR = 20
STATIC = 0
BACKGROUND = "#111722"
TEXT_COLOR = "#d9d1d9"
ACCENT_COLOR = "#3fb950"
# ======================================

ASCII_CHARS = "@%#*+=-:. "


def brightness_to_ascii(brightness):
    index = int(brightness / 255 * (len(ASCII_CHARS) - 1))
    return ASCII_CHARS[index]


def image_to_ascii(image_path, width=84):
    print(f"Loading image: {image_path}")
    img = Image.open(image_path).convert("L")
    img = ImageOps.autocontrast(img, cutoff=1)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.0, percent=140, threshold=2))

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
    height = int(width * aspect_ratio * 0.58)
    img = img.resize((width, height), Image.Resampling.LANCZOS)

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


def create_animated_svg(ascii_grid, output_file, static=False, input_image=INPUT_IMAGE):
    width = 840
    height = 905

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{int(width)}" height="{int(height)}" viewBox="0 0 {int(width)} {int(height)}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#111722"/><stop offset="1" stop-color="#0d1117"/></linearGradient></defs>',
        f'<rect width="{int(width)}" height="{int(height)}" rx="12" fill="url(#bg)"/>',
        f'<rect x=".5" y=".5" width="{int(width) - 1}" height="{int(height) - 1}" rx="12" fill="none" stroke="#30363d"/>',
        f'<line x1="0" y1="30" x2="{int(width)}" y2="30" stroke="#30363d"/>',
        '<circle cx="20" cy="15" r="5" fill="#ff5f56"/>',
        '<circle cx="36" cy="15" r="5" fill="#ffbd2e"/>',
        '<circle cx="52" cy="15" r="5" fill="#27c93f"/>',
        f'<text x="{int(width) / 2:.1f}" y="19" fill="#7d8590" font-size="12" text-anchor="middle">aditya@github: ~$ ./portrait.sh</text>',
    ]

    for row_idx, row in enumerate(ascii_grid):
        y = 37 + row_idx * 13
        if y > 840:
            break
        clip_id = f"r{row_idx}"
        svg_lines.extend([
            f'<clipPath id="{clip_id}"><rect x="20" y="{y - 11}" height="15" width="0"><animate attributeName="width" from="0" to="800" begin="{row_idx * 0.05:.2f}s" dur="0.11s" fill="freeze"/></rect></clipPath>',
            f'<g clip-path="url(#{clip_id})"><text xml:space="preserve" x="20" y="{y}" fill="#c9d1d9" font-size="12.9" textLength="800" lengthAdjust="spacing">{escape_xml(" " * 0 + row)}</text></g>',
            f'<rect y="{y - 11}" width="8" height="13" fill="#c9d1d9" opacity="0"><animate attributeName="x" from="20" to="820" begin="{row_idx * 0.05:.2f}s" dur="0.11s" fill="freeze"/><set attributeName="opacity" to=".85" begin="{row_idx * 0.05:.2f}s"/><set attributeName="opacity" to="0" begin="{row_idx * 0.05 + 0.11:.2f}s"/></rect>',
        ])

    svg_lines.extend([
        '<line x1="0" y1="862" x2="840" y2="862" stroke="#30363d"/>',
        '<text x="20" y="881" fill="#7d8590" font-size="13">aditya@github:~$ whoami <tspan fill="#c9d1d9">Aditya Mishra</tspan></text>',
        '</svg>',
    ])
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
