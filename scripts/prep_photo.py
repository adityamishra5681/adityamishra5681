#!/usr/bin/env python3
"""
prep_photo.py - Remove background and enhance contrast for ASCII art conversion
Usage: python scripts/prep_photo.py <input_image> <output_image>
"""

import sys
import cv2
import numpy as np
from rembg import remove
from PIL import Image

# ===== CONFIG SECTION - TUNE THIS =====
CLIP_LIMIT = 3.0  # CLAHE contrast enhancement (higher = more contrast)
TILE_GRID_SIZE = (8, 8)  # CLAHE tile grid size
# ======================================

def prep_photo(input_path, output_path):
    """Remove background and enhance local contrast"""
    
    print(f"[1/3] Loading image: {input_path}")
    # Load image
    with open(input_path, 'rb') as f:
        input_data = f.read()
    
    print("[2/3] Removing background...")
    # Remove background using rembg
    output_data = remove(input_data)
    
    # Convert to PIL Image
    from io import BytesIO
    img = Image.open(BytesIO(output_data))
    
    # Convert to OpenCV format (BGR)
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2BGRA)
    
    # Split channels
    b, g, r, a = cv2.split(img_cv)
    
    print("[3/3] Enhancing contrast...")
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to each channel
    clahe = cv2.createCLAHE(clipLimit=CLIP_LIMIT, tileGridSize=TILE_GRID_SIZE)
    
    # Only apply to non-transparent areas
    b = clahe.apply(b)
    g = clahe.apply(g)
    r = clahe.apply(r)
    
    # Merge back
    enhanced = cv2.merge([b, g, r, a])
    
    # Convert back to PIL and save
    result = Image.fromarray(cv2.cvtColor(enhanced, cv2.COLOR_BGRA2RGBA))
    result.save(output_path)
    
    print(f"✓ Saved to: {output_path}")
    print(f"  Image size: {result.size}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scripts/prep_photo.py <input_image> <output_image>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    prep_photo(input_file, output_file)
