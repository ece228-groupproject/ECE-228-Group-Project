from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Load image
img = Image.open('./tiles/full_size_64.png')
img_width, img_height = img.size
center_x = img_width // 2
center_y = img_height // 2

fig, ax = plt.subplots()
ax.imshow(img)
plt.title("Click 2N points (relative to center origin)")
coords = plt.ginput(n=2, timeout=0)
plt.close()

# Draw and label each box using center-origin
fig, ax = plt.subplots()
ax.imshow(img)

print("Detected boxes (with origin at image center):\n")

for i in range(0, len(coords), 2):
    (x1, y1), (x2, y2) = coords[i], coords[i+1]

    # Convert from top-left origin to center-origin
    x1_c, y1_c = x1 - center_x, center_y - y1
    x2_c, y2_c = x2 - center_x, center_y - y2

    # Reconvert for drawing (still uses top-left coordinates for display)
    x_min = min(x1, x2)
    y_min = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    rect = patches.Rectangle((x_min, y_min), width, height,
                             linewidth=2, edgecolor='r', facecolor='none')
    ax.add_patch(rect)

    print(f"Box {i//2 + 1}: Center-Origin Coords:"
          f"\n  - Top-Left = ({int(min(x1_c, x2_c))}, {int(max(y1_c, y2_c))})"
          f"\n  - Width = {int(width)}, Height = {int(height)}\n")

plt.title("Boxes drawn (display still top-left based)")
plt.show()
