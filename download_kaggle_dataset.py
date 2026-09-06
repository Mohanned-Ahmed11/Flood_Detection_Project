import os
import glob
import shutil
import kagglehub

def download_dataset():
    print("Downloading Kaggle Satellite Flood Dataset...")
    dataset_dir = "dataset"
    os.makedirs(dataset_dir, exist_ok=True)

    try:
        # Download Flood Area Segmentation Dataset from Kaggle
        path = kagglehub.dataset_download("faizalkhan/flood-area-segmentation")
        print(f"✅ Downloaded to: {path}")

        # Find images in downloaded dataset
        image_files = glob.glob(os.path.join(path, "**", "*.png"), recursive=True) + \
                      glob.glob(os.path.join(path, "**", "*.jpg"), recursive=True)

        print(f"Found {len(image_files)} dataset images!")

        if image_files:
            copied_count = 0
            for idx, img_path in enumerate(image_files[:6]):
                ext = os.path.splitext(img_path)[1]
                dest_path = os.path.join(dataset_dir, f"kaggle_flood_{idx+1}{ext}")
                shutil.copy(img_path, dest_path)
                copied_count += 1
                print(f" -> Saved to: {os.path.abspath(dest_path)}")
            print(f"\nSuccessfully copied {copied_count} dataset image files into '{os.path.abspath(dataset_dir)}'.")

    except Exception as e:
        print(f"Error downloading via kagglehub: {e}")

if __name__ == "__main__":
    download_dataset()
