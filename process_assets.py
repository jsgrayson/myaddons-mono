from PIL import Image, ImageChops
import os

def slice_assets():
    source_path = 'static/img/composite_assets.png'
    output_dir = 'static/img'
    
    if not os.path.exists(source_path):
        print("Source image not found.")
        return

    img = Image.open(source_path).convert("RGBA")
    width, height = img.size
    
    # Define approximate quadrants based on the visual layout
    # Top Left: Pet Card Frame
    # Top Right: Weave Button (Gear)
    # Bottom Left: Header/Scroll
    # Bottom Right: Background Scene
    
    mid_x = width // 2
    mid_y = height // 2
    
    # 1. Pet Card (Top Left)
    pet_card = img.crop((0, 0, mid_x, mid_y))
    pet_card = trim(pet_card)
    pet_card.save(os.path.join(output_dir, 'pet_card_bg.png'))
    print("Saved pet_card_bg.png")
    
    # 2. Weave Button (Top Right)
    weave_btn = img.crop((mid_x, 0, width, mid_y))
    weave_btn = trim(weave_btn)
    weave_btn.save(os.path.join(output_dir, 'weave_btn.png'))
    print("Saved weave_btn.png")
    
    # 3. Main Frame / Scroll (Bottom Left)
    loom_frame = img.crop((0, mid_y, mid_x, height))
    loom_frame = trim(loom_frame)
    loom_frame.save(os.path.join(output_dir, 'loom_frame.png'))
    print("Saved loom_frame.png")
    
    # 4. Background Tile (Bottom Right)
    # For the background, we might want the whole quadrant or a tile
    bg_tile = img.crop((mid_x, mid_y, width, height))
    bg_tile = bg_tile.convert("RGB") # Remove Alpha for JPEG
    bg_tile.save(os.path.join(output_dir, 'bg_tile.jpg'), 'JPEG')
    print("Saved bg_tile.jpg")

def trim(im):
    """Trims black/transparent borders"""
    bg = Image.new(im.mode, im.size, (0,0,0,0))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, 0)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im

if __name__ == "__main__":
    slice_assets()
