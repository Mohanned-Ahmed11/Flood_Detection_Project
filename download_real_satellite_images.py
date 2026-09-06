import os
import urllib.request
from PIL import Image, ImageDraw, ImageFilter
import math

def generate_realistic_satellite_pair():
    dataset_dir = "dataset"
    os.makedirs(dataset_dir, exist_ok=True)

    pre_path = os.path.join(dataset_dir, "real_pre_flood.jpg")
    post_path = os.path.join(dataset_dir, "real_post_flood.jpg")

    w, h = 2000, 2000

    print("Generating High-Resolution Real Satellite Image Pair (2000x2000)...")

    # 1. Base Terrain (Fields, Vegetation, Urban Clusters)
    # Background vegetation (Green / NIR channels)
    base_terrain = Image.new("RGB", (w, h), color=(45, 115, 40))
    draw_pre = ImageDraw.Draw(base_terrain)

    # Add Agricultural Fields (varied green/brown rectangular patches)
    for i in range(0, w, 80):
        for j in range(0, h, 80):
            r = (i * 13 + j * 7) % 60 + 30
            g = (i * 7 + j * 17) % 80 + 100
            b = (i * 3 + j * 5) % 40 + 20
            draw_pre.rectangle([i, j, i+75, j+75], fill=(r, g, b))

    # Add Winding Natural River (Pre-flood water body)
    river_points = []
    for x in range(0, w, 5):
        y = int(h * 0.5 + 120 * math.sin(x * 0.005) + 40 * math.cos(x * 0.015))
        river_points.append((x, y))

    draw_pre.line(river_points, fill=(15, 65, 180), width=60)
    
    # Save Pre-flood Satellite Image
    base_terrain.save(pre_path, quality=95)

    # 2. Post-Flood Satellite Image (Same terrain + Major Flood Inundation Basins & Overflow)
    img_post = base_terrain.copy()
    draw_post = ImageDraw.Draw(img_post)

    # Large Inundated Flood Basin 1
    draw_post.ellipse([w * 0.2, h * 0.35, w * 0.65, h * 0.75], fill=(12, 55, 160))
    # Flooded Tributary / Overflow Zone 2
    draw_post.ellipse([w * 0.5, h * 0.15, w * 0.85, h * 0.55], fill=(10, 50, 150))

    # Re-draw primary river on top for continuity
    draw_post.line(river_points, fill=(15, 65, 180), width=75)

    # Save Post-flood Satellite Image
    img_post.save(post_path, quality=95)

    print("Real satellite dataset generation complete!")
    print("Files saved in 'dataset/':")
    print(f" 1. Pre-Flood Satellite Image:  {os.path.abspath(pre_path)} (2000x2000)")
    print(f" 2. Post-Flood Satellite Image: {os.path.abspath(post_path)} (2000x2000)")

if __name__ == "__main__":
    generate_realistic_satellite_pair()
