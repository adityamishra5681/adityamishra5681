#!/usr/bin/env python3
"""
make_ascii_svg.py - Convert image to animated ASCII-art SVG in the frex style.
"""

import numpy as np
from PIL import Image, ImageEnhance

# ===== CONFIG SECTION - TUNE THIS =====
INPUT_IMAGE = "source-prepped.png"
OUTPUT_SVG = "avi-ascii.svg"
WIDTH = 72
CONTRAST = 1.7
GAMMA = 1.14
WHITE_FLOOR = 24
STATIC = 0
BACKGROUND = "#111722"
TEXT_COLOR = "#d9d1d9"
ACCENT_COLOR = "#3fb950"
# ======================================

ASCII_CHARS = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"


def brightness_to_ascii(brightness):
    index = int(brightness / 255 * (len(ASCII_CHARS) - 1))
    return ASCII_CHARS[index]


def image_to_ascii(image_path, width=72):
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


def build_reveal_text(text, x, y, fill, size, begin):
    parts = [f'<text x="{x}" y="{y:.1f}" font-size="{size}" fill="{fill}" style="letter-spacing:-0.3px;">']
    for idx, ch in enumerate(text):
        ch_text = escape_xml(ch)
        if ch == " ":
            ch_text = "&#160;"
        start = begin + idx * 0.05
        parts.append(f'<tspan opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{start:.2f}s" dur="0.01s" fill="freeze"/>{ch_text}</tspan>')
    parts.append('</text>')
    return parts


def create_animated_svg(ascii_grid, output_file, static=False):
    width = 480
    height = 390
    font_size = 11
    line_height = 11.3
    rows = ascii_grid[:24]

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#111722"/><stop offset="1" stop-color="#0d1117"/></linearGradient></defs>',
        f'<rect width="{width}" height="{height}" rx="12" fill="url(#bg)"/>',
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="12" fill="none" stroke="#30363d"/>',
        f'<line x1="0" y1="30" x2="{width}" y2="30" stroke="#30363d"/>',
        '<circle cx="20" cy="15.0" r="5" fill="#ff5f56"/>',
        '<circle cx="36" cy="15.0" r="5" fill="#ffbd2e"/>',
        '<circle cx="52" cy="15.0" r="5" fill="#27c93f"/>',
        f'<text x="{width / 2:.1f}" y="19.0" fill="#7d8590" font-size="12" text-anchor="middle">aditya@github: ~$ ./portrait.sh</text>',
        '<g transform="translate(0,5)">',
    ]

    svg_lines.extend(build_reveal_text("Aditya Mishra", 20, 60.0, ACCENT_COLOR, 22, 0.05))
    svg_lines.extend(build_reveal_text("Data Science & AI • Web Development", 20, 84.0, TEXT_COLOR, 11.8, 0.45))

    for idx, row in enumerate(rows):
        y = 106 + idx * line_height
        prefix = "> "
        line_text = prefix + row
        svg_lines.append(f'<text x="20" y="{y:.1f}" font-size="{font_size}" fill="{TEXT_COLOR}" style="letter-spacing:-0.3px;">')
        for char_idx, ch in enumerate(line_text):
            ch_text = escape_xml(ch)
            if ch == " ":
                ch_text = "&#160;"
            start = 0.7 + idx * 0.03 + char_idx * 0.008
            svg_lines.append(f'<tspan opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{start:.2f}s" dur="0.01s" fill="freeze"/>{ch_text}</tspan>')
        svg_lines.append('</text>')

    svg_lines.append('</g></svg>')
    svg_content = "\n".join(svg_lines)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"✓ Created: {output_file}")
    print(f"  Size: {width}x{height}px")
    print(f"  Rows: {len(rows)}")


if __name__ == "__main__":
    print(f"Converting {INPUT_IMAGE} to ASCII art...")
    ascii_grid = image_to_ascii(INPUT_IMAGE, WIDTH)
    print("\nCreating SVG...")
    create_animated_svg(ascii_grid, OUTPUT_SVG, static=STATIC)
    print("\n✓ Done! Preview with:")
    print(f"  Open {OUTPUT_SVG} in a browser")
