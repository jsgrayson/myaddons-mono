from PIL import Image, ImageDraw
import os
import math

MEDIA_DIR = "/Users/jgrayson/Documents/MyAddons-Mono/PetWeaver/Media"

def generate_xp_bar():
    dst = os.path.join(MEDIA_DIR, "XPBar.tga")
    print(f"Generating synthetic XPBar at {dst}...")
    width, height = 128, 16 
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Border
    draw.rectangle([0, 0, width-1, height-1], outline=(150, 150, 150, 255), width=1)
    
    # Gradient Fill (Blue to Purple)
    for x in range(1, width-1):
        ratio = x / width
        r = int(50 * ratio + 100 * (1-ratio)) # 50 to 100
        g = int(0 * ratio + 50 * (1-ratio))
        b = int(255 * ratio + 200 * (1-ratio))
        for y in range(1, height-1):
            img.putpixel((x, y), (r, g, b, 255))
            
    img.save(dst, format="TGA")
    print("XPBar generation complete.")

def generate_hunter_icon():
    dst = os.path.join(MEDIA_DIR, "HunterIcon.tga")
    print(f"Generating synthetic HunterIcon at {dst}...")
    size = 64
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Crosshairs (Red/Gold)
    # Outer Circle
    draw.ellipse([8, 8, 56, 56], outline=(255, 50, 50, 255), width=3)
    
    # Inner Cross
    cx, cy = 32, 32
    draw.line([cx-10, cy, cx+10, cy], fill=(255, 215, 0, 255), width=2)
    draw.line([cx, cy-10, cx, cy+10], fill=(255, 215, 0, 255), width=2)
    
    # Center Dot
    draw.ellipse([cx-2, cy-2, cx+2, cy+2], fill=(255, 0, 0, 255))
    
    img.save(dst, format="TGA")
    print("HunterIcon generation complete.")

if __name__ == "__main__":
    if not os.path.exists(MEDIA_DIR):
        os.makedirs(MEDIA_DIR)
    generate_xp_bar()
    generate_hunter_icon()
