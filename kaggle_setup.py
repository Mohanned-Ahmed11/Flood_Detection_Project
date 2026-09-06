import os
import sys

def setup_kaggle():
    print("========================================================")
    print("Kaggle API Token Setup Helper")
    print("========================================================\n")
    
    print("How to get your Kaggle API credentials (1 minute):")
    print(" 1. Go to: https://www.kaggle.com/settings")
    print(" 2. Scroll down to the 'API' section.")
    print(" 3. Click 'Create New Token'.")
    print(" 4. A file named 'kaggle.json' will be downloaded to your Downloads folder.\n")

    downloads_path = os.path.expanduser("~/Downloads/kaggle.json")
    target_dir = os.path.expanduser("~/.kaggle")
    target_path = os.path.join(target_dir, "kaggle.json")

    if os.path.exists(downloads_path):
        os.makedirs(target_dir, exist_ok=True)
        import shutil
        shutil.copy(downloads_path, target_path)
        print(f"✅ Found kaggle.json in Downloads! Automatically copied to: {target_path}")
        print("You can now download Kaggle datasets freely!")
        return

    print(f"Checking for kaggle.json at: {target_path}")
    if os.path.exists(target_path):
        print("✅ kaggle.json is already configured!")
        return

    print("\nAlternatively, enter your Kaggle credentials below:")
    username = input("Enter Kaggle Username: ").strip()
    key = input("Enter Kaggle API Key: ").strip()

    if username and key:
        os.makedirs(target_dir, exist_ok=True)
        with open(target_path, "w") as f:
            f.write(f'{{"username":"{username}","key":"{key}"}}')
        print(f"✅ Saved kaggle.json to: {target_path}")

if __name__ == "__main__":
    setup_kaggle()
