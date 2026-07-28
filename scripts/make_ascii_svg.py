#!/usr/bin/env python3
"""
make_ascii_svg.py - Convert image to animated ASCII art SVG
Reads source-prepped.png and outputs avi-ascii.svg
"""

import base64
import io
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


def build_image_data_uri(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((420, 520), Image.Resampling.LANCZOS)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def create_animated_svg(ascii_grid, output_file, static=False, input_image=INPUT_IMAGE):
    width = 760
    height = 760
    photo_uri = build_image_data_uri(input_image)

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
        '  <rect x="42" y="60" width="676" height="648" rx="12" fill="#0c1118" stroke="#1f2937" stroke-width="1.2"/>',
        '  <rect x="56" y="74" width="648" height="620" rx="10" fill="#090d12" stroke="#2b313d" stroke-width="1"/>',
        f'  <image href="{photo_uri}" x="80" y="100" width="360" height="450" preserveAspectRatio="xMidYMid meet"/>',
        '  <rect x="80" y="100" width="360" height="450" rx="10" fill="none" stroke="#2f3b4a" stroke-width="1"/>',
        '  <text x="80" y="590" fill="#d9d1d9" font-size="15" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">Aditya Mishra</text>',
        '  <text x="80" y="615" fill="#7d8590" font-size="12" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">Data Science • AI • Web Development</text>',
        '  <line x1="480" y1="110" x2="660" y2="110" stroke="#1f6feb" stroke-opacity="0.45"/>',
        '  <text x="480" y="150" fill="#7d8590" font-size="12" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">Focus</text>',
        '  <text x="480" y="176" fill="#d9d1d9" font-size="14" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">Building useful AI tools</text>',
        '  <text x="480" y="235" fill="#7d8590" font-size="12" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">Current stack</text>',
        '  <text x="480" y="260" fill="#d9d1d9" font-size="14" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">Python • React • MongoDB</text>',
        '  <rect x="480" y="290" width="150" height="10" rx="5" fill="#16212e"/>',
        '  <rect x="480" y="290" width="110" height="10" rx="5" fill="#3fb950"/>',
        '  <text x="480" y="335" fill="#7d8590" font-size="12" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">Availability</text>',
        '  <text x="480" y="360" fill="#d9d1d9" font-size="14" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">Open to interesting work</text>',
    ]

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
