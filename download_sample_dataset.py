import os
import math
from PIL import Image, ImageDraw

def create_sample_dataset():
    dataset_dir = "dataset"
    os.makedirs(dataset_dir, exist_ok=True)
    
    pre_path = os.path.join(dataset_dir, "pre_flood_sample.png")
    post_path = os.path.join(dataset_dir, "post_flood_sample.png")

    w, h = 1000, 1000

    # 1. Create Pre-Flood Satellite Image (Green landscape + Winding River)
    img_pre = Image.new("RGB", (w, h), color=(60, 140, 50))
    draw_pre = ImageDraw.Draw(img_pre)

    points_pre = []
    for x in range(0, w, 10):
        y = int(h / 2 + 60 * math.sin(x * 0.01))
        points_pre.append((x, y))

    draw_pre.line(points_pre, fill=(30, 90, 220), width=45)
    img_pre.save(pre_path)

    # 2. Create Post-Flood Satellite Image (Same landscape + Large Inundated Flood Basin)
    img_post = Image.new("RGB", (w, h), color=(60, 140, 50))
    draw_post = ImageDraw.Draw(img_post)

    draw_post.ellipse([200, 300, 800, 700], fill=(20, 110, 230))
    draw_post.line(points_pre, fill=(30, 90, 220), width=45)
    img_post.save(post_path)

    print("Sample dataset created in:", os.path.abspath(dataset_dir))
    print(" - Pre-Flood:", pre_path)
    print(" - Post-Flood:", post_path)

if __name__ == "__main__":
    create_sample_dataset()
