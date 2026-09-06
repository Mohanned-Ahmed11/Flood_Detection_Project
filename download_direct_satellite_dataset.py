import os
import urllib.request
import ssl

def download_dataset():
    dataset_dir = "dataset"
    os.makedirs(dataset_dir, exist_ok=True)

    print("Downloading Real Public Satellite Flood Dataset...")

    # Public NASA Earth Observatory & Sentinel satellite image datasets
    dataset_urls = {
        "satellite_pre_flood.jpg": "https://raw.githubusercontent.com/giswqs/data/main/raster/disaster_pre.jpg",
        "satellite_post_flood.jpg": "https://raw.githubusercontent.com/giswqs/data/main/raster/disaster_post.jpg"
    }

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    for filename, url in dataset_urls.items():
        dest_path = os.path.join(dataset_dir, filename)
        print(f"Downloading {filename}...")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ctx) as response, open(dest_path, 'wb') as out_file:
                out_file.write(response.read())
            print(f" -> Saved: {os.path.abspath(dest_path)}")
        except Exception as e:
            print(f"Failed to download {filename}: {e}")

    print("\nDataset download process complete!")

if __name__ == "__main__":
    download_dataset()
