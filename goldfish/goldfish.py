from PIL import Image, ImageDraw, ImageOps
import random
import math

# === Configuration ===
# Dimensions and Resolution
DPI = 600
WIDTH_IN = 8
HEIGHT_IN = 10
WIDTH_PX = WIDTH_IN * DPI
HEIGHT_PX = HEIGHT_IN * DPI

# Colors
BG_COLOR = (0, 0, 0, 255) # Solid Black
# McLaren Orange approx (Papaya Orange)
FISH_COLOR = (255, 133, 0, 255) 

# Distribution Settings
# Total attempts to try placing fish. Higher = denser overall.
TOTAL_ATTEMPTS = 15000 
# Controls how quickly the gradient fades. 
# 1.0 = linear fade. 2.0 = quadratic (fades faster towards right).
FADE_POWER = 1.75
# Base size of the goldfish in pixels (at 600dpi, 150px is about 1/4 inch)
BASE_FISH_SIZE = 150 

# === Helper Function: Create a single goldfish sprite ===
def create_fish_sprite(size, color):
    # Create a small transparent canvas for one fish
    # Aspect ratio of a goldfish cracker is roughly 5:3
    w = size
    h = int(size * 0.6)
    # Create transparent image
    fish_img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(fish_img)

    # Draw the body (an ellipse)
    body_bounds = [int(w*0.15), 0, w, h]
    draw.ellipse(body_bounds, fill=color)

    # Draw the tail (a triangle/wedge shape on the left)
    # Using a polygon to approximate the tail shape
    tail_points = [
        (int(w*0.3), int(h/2)), # Center attachment point
        (0, 0),                 # Top tail tip
        (int(w*0.075), int(h/2)), # Mild inward curve
        (0, h)                  # Bottom tail tip
    ]
    draw.polygon(tail_points, fill=color)
    
    # Add the classic "eye" dot (optional, but makes it look more like the cracker)
    eye_color = (color[0], color[1], color[2], 0) # Slightly transparent eye
    eye_x = int(w * 0.75)
    eye_y = int(h * 0.35)
    eye_rad = int(w * 0.04)
    draw.ellipse([eye_x - eye_rad, eye_y - eye_rad, eye_x + eye_rad, eye_y + eye_rad], fill=eye_color)

    return fish_img

# === Main Image Generation ===
print(f"Generating canvas: {WIDTH_PX}x{HEIGHT_PX} pixels at {DPI} DPI.")
main_canvas = Image.new('RGB', (WIDTH_PX, HEIGHT_PX), BG_COLOR)

print("Scattering goldfish evenly distributed by gradient... please wait.")

for i in range(TOTAL_ATTEMPTS):
    # 1. Choose a random X location across the whole canvas
    pos_x = random.randint(-BASE_FISH_SIZE, WIDTH_PX)
    
    # 2. Calculate Acceptance Probability based on X location.
    # Normalized X (0.0 at left, 1.0 at right)
    norm_x = max(0, min(1, pos_x / WIDTH_PX))
    
    # Probability is high at left (norm_x=0) and zero at right (norm_x=1).
    # Using power function to make the fade smoother than linear.
    probability = (1.0 - norm_x) ** FADE_POWER
    
    # 3. Rejection Sampling: Roll the dice.
    # Only place the fish if a random number is less than the calculated probability.
    if random.random() < probability:
        
        # Add slight random variation to size (80% to 120% base size)
        # scale_variance = random.uniform(0.8, 1.2)
        scale_variance = 1.0
        this_fish_size = int(BASE_FISH_SIZE * scale_variance)
        
        # Create the fish sprite
        fish = create_fish_sprite(this_fish_size, FISH_COLOR)
        
        # Add random rotation (0 to 360 degrees)
        rotation = random.randint(0, 360)
        fish_rotated = fish.rotate(rotation, expand=True, resample=Image.BICUBIC)
        
        # Pick random Y coordinate
        # Allow placing slightly off-canvas so edge fish aren't cut off flat
        pos_y = random.randint(-this_fish_size, HEIGHT_PX)
        
        # Center the coordinates for pasting
        paste_x = pos_x - fish_rotated.width // 2
        paste_y = pos_y - fish_rotated.height // 2
        
        # Paste the fish using its own alpha channel as a mask
        main_canvas.paste(fish_rotated, (paste_x, paste_y), fish_rotated)

# === Saving ===
output_filename = "mclaren_goldfish_livery_600dpi.png"
# Save including DPI metadata for printing software
main_canvas.save(output_filename, dpi=(DPI, DPI))
print(f"Done! Image saved as {output_filename}")