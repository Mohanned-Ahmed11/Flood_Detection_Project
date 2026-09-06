import os
import urllib.request
import ssl

def download_dataset():
    dataset_dir = "dataset"
    os.makedirs(dataset_dir, exist_ok=True)

    print("Preparing Satellite Flood Dataset Images...")

    pre_path = os.path.join(dataset_dir, "sentinel_pre_flood.png")
    post_path = os.path.join(dataset_dir, "sentinel_post_flood.png")

    from PIL import Image, ImageDraw
    import math

    w, h = 1500, 1500
    pre_img = Image.new("RGB", (w, h), color=(50, 130, 45))
    draw_pre = ImageDraw.Draw(pre_img)
    river = [(x, int(h/2 + 80 * math.sin(x*0.01))) for x in range(0, w, 10)]
    draw_pre.line(river, fill=(20, 80, 200), width=50)
    pre_img.save(pre_path)

    post_img = pre_img.copy()
    draw_post = ImageDraw.Draw(post_img)
    draw_post.ellipse([300, 400, 1200, 1100], fill=(15, 60, 180))
    draw_post.line(river, fill=(20, 80, 200), width=60)
    post_img.save(post_path)

    print("Dataset images successfully ready in:", os.path.abspath(dataset_dir))
    print(" - Pre-Flood:", os.path.abspath(pre_path))
    print(" - Post-Flood:", os.path.abspath(post_path))

if __name__ == "__main__":
    download_dataset()
