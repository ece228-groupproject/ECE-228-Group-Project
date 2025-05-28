import time
import os
import requests
from PIL import Image
from io import BytesIO

tile_dict = {(1, 1): 'https://mt2.google.com/vt/lyrs=m&x=1&y=1&z=2&hl=en&scale=2', (2, 1): 'https://mt3.google.com/vt/lyrs=m&x=2&y=1&z=2&hl=en&scale=2', (1, 2): 'https://mt3.google.com/vt/lyrs=m&x=1&y=2&z=2&hl=en&scale=2', (2, 2): 'https://mt0.google.com/vt/lyrs=m&x=2&y=2&z=2&hl=en&scale=2', (0, 1): 'https://mt1.google.com/vt/lyrs=m&x=0&y=1&z=2&hl=en&scale=2', (3, 1): 'https://mt0.google.com/vt/lyrs=m&x=3&y=1&z=2&hl=en&scale=2', (0, 2): 'https://mt2.google.com/vt/lyrs=m&x=0&y=2&z=2&hl=en&scale=2', (3, 2): 'https://mt1.google.com/vt/lyrs=m&x=3&y=2&z=2&hl=en&scale=2', (1, 0): 'https://mt1.google.com/vt/lyrs=m&x=1&y=0&z=2&hl=en&scale=2', (2, 0): 'https://mt2.google.com/vt/lyrs=m&x=2&y=0&z=2&hl=en&scale=2', (0, 0): 'https://mt0.google.com/vt/lyrs=m&x=0&y=0&z=2&hl=en&scale=2', (3, 0): 'https://mt3.google.com/vt/lyrs=m&x=3&y=0&z=2&hl=en&scale=2'} 

TILE_SIZE = 256

canvas_width =  TILE_SIZE *3
canvas_height = TILE_SIZE *4
canvas = Image.new("RGB", (canvas_width, canvas_height))

for coord,url in tile_dict.items():
    print(f"Key: {coord}, Value: {url}")

    paste_x = coord[0] + TILE_SIZE
    paste_y = coord[1] + TILE_SIZE
    response = requests.get(url)

    img = Image.open(BytesIO(response.content)).convert("RGB")
    canvas.paste(img, (paste_x, paste_y))


canvas.save("stitched_map.png")
print("Saved to stitched_map.png")