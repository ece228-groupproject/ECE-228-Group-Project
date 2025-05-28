from PIL import Image, ImageDraw
import cv2
import numpy as np
import re

def remove_arrows(image_path, output_path, mask_coords):
    # Load image and convert to BGR
    image = cv2.imread(image_path)

    # Create mask (white = inpaint region)
    mask = np.zeros(image.shape[:2], dtype=np.uint8)

    # Fill the arrow region with white (255) in the mask
    for (x, y, w, h) in mask_coords:
        mask[y:y+h, x:x+w] = 255

    # Inpaint using Telea method (more natural edges)
    result = cv2.inpaint(image, mask, inpaintRadius=5, flags=cv2.INPAINT_NS)

    cv2.imwrite(output_path, result)
    print(f"Saved inpainted image to {output_path}")

def crop_and_pad_content(img_path, output_path, crop_top=90, crop_bottom=90, pad_to=(768, 768)):
    img = Image.open(img_path)
    arrow_box = [(), (), [], [] ]
    width, height = img.size
    img.show()
    # Image cropping 

    # 1) Top bar removal 
    img1 = img.crop((0, 59, width, height))
    width, height = img1.size
    img2 = img1.crop((0, 0, width, 580))
    # img1.show()
    
    img2.show()

def parse_transform(transform):
    translate = re.search(r'translate\(([\d.]+)[ ,]([\d.]+)', transform)
    scale = re.search(r'scale\(([\d.]+)[ ,]([\d.]+)', transform)
    rotate = re.search(r'rotate\(([\d.]+)', transform)

    tx, ty = float(translate.group(1)), float(translate.group(2))
    sx, sy = float(scale.group(1)), float(scale.group(2))
    angle = float(rotate.group(1)) if rotate else 0

    return {
        'x': tx,
        'y': ty,
        'scale_x': sx,
        'scale_y': sy,
        'angle': angle
    }


# remove_arrows(
#     "./screenshots/streetview_iframe.png",
#     "./screenshots/cleaned.png",
#    mask_coords=[(500, 565, 60, 600-565)]  # Example box for white arrows
# )


# crop_and_pad_content(
#     img_path="./screenshots/streetview_iframe.png",
#     output_path="./screenshots/bottomBar.png",
#     crop_top=90,      # remove top GUI
#     crop_bottom=80,   # remove bottom GUI
#     pad_to=(768, 768) # final desired CNN input size
# )

img = Image.open('./tiles/full_size_64.png')
# Get screen coords : -80
transform_str='translate(600 656.3324125212636) scale(1 0.31698729810778065) rotate(306.94284)'
coords = parse_transform(transform_str)
draw = ImageDraw.Draw(img)

# Draw a simple circle at the arrow position
r = 15  # radius of overlay
x, y = coords['x'], coords['y']
draw.ellipse((x-r, y-r, x+r, y+r), fill=(255, 0, 0, 128))  # red translucent

img.show()
