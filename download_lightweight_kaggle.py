import os
os.environ["KAGGLE_API_TOKEN"] = "KGAT_60f918924925a4ab328767447b9ba217"

import kagglehub
import glob
import shutil

def download_lightweight():
    print("Downloading Kaggle Flood dataset using API Token...")
    try:
        path = kagglehub.dataset_download("faizalkhan/flood-area-segmentation")
        print("Downloaded successfully to:", path)

        dataset_dir = "dataset"
        os.makedirs(dataset_dir, exist_ok=True)

        images = glob.glob(os.path.join(path, "**", "*.jpg"), recursive=True) + \
                 glob.glob(os.path.join(path, "**", "*.png"), recursive=True)

        print(f"Found {len(images)} images in dataset.")

        if images:
            for idx, img_path in enumerate(images[:5]):
                dest_path = os.path.join(dataset_dir, f"kaggle_flood_{idx+1}.jpg")
                shutil.copy(img_path, dest_path)
                print(f" -> Saved sample image to: {os.path.abspath(dest_path)}")
    except Exception as e:
        print("Error downloading dataset:", str(e))

if __name__ == "__main__":
    download_lightweight()
