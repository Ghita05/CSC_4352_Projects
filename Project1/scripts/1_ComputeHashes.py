import os
import csv
from PIL import Image
import imagehash

def compute_phash(image_path, hash_size=8):
    img = Image.open(image_path).convert("L")
    ph = imagehash.phash(img, hash_size=hash_size)
    return int(str(ph), 16)

def main():
    images_folder = "Project_1\images"     
    output_csv = "Project_1/results/hashes.csv"

    os.makedirs("../results", exist_ok=True)
    images = sorted(os.listdir(images_folder))

    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "phash_int"])
        for img_name in images:
            path = os.path.join(images_folder, img_name)
            if not os.path.isfile(path): 
                continue
            try:
                ph = compute_phash(path)
                writer.writerow([img_name, ph])
                print(f"{img_name} -> {ph}")
            except Exception as e:
                print(f"Error on {img_name}: {e}")

    print(f"\n✅ All perceptual hashes saved to {output_csv}")

if __name__ == "__main__":
    main()
