import csv
import cv2
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import imagehash
import os

def hamming_distance_int(a, b):
    return bin(a ^ b).count("1")

def group_duplicates(verified_pairs):
    """Group duplicate images together using Union-Find algorithm"""
    from collections import defaultdict
    
    # Create a graph of connections
    graph = defaultdict(set)
    all_images = set()
    
    for img1, img2 in verified_pairs:
        graph[img1].add(img2)
        graph[img2].add(img1)
        all_images.add(img1)
        all_images.add(img2)
    
    # Find connected components (groups of duplicates)
    visited = set()
    duplicate_groups = []
    
    def dfs(image, current_group):
        if image in visited:
            return
        visited.add(image)
        current_group.append(image)
        for neighbor in graph[image]:
            dfs(neighbor, current_group)
    
    for image in all_images:
        if image not in visited:
            group = []
            dfs(image, group)
            if len(group) > 1:  # Only groups with duplicates
                duplicate_groups.append(sorted(group))
    
    return duplicate_groups

def verify_candidates(images_folder="Project_1/images", candidates_csv="Project_1/results/candidates.csv", 
                     output_csv="Project_1/results/verified_duplicates.csv", 
                     grouped_csv="Project_1/results/duplicate_groups.csv", hamming_threshold=6):
    verified = []
    verified_data = []  # Store detailed information for CSV output
    
    with open(candidates_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            img1, img2 = row["image1"], row["image2"]
            path1 = os.path.join(images_folder, img1)
            path2 = os.path.join(images_folder, img2)

            # Compute hashes again (or read from CSV if you prefer)
            h1 = imagehash.phash(Image.open(path1).convert("L"))
            h2 = imagehash.phash(Image.open(path2).convert("L"))

            ham = h1 - h2  # ImageHash objects support direct Hamming distance calculation
            if ham <= hamming_threshold:
                verified.append((img1, img2))
                verified_data.append({
                    'image1': img1,
                    'image2': img2, 
                    'hamming_distance': ham,
                    'verified': True
                })
                print(f"Match {img1} ↔ {img2} (Hamming={ham})")
            else:
                print(f"No Match {img1} ↔ {img2} (Hamming={ham})")

    # Group duplicates together
    duplicate_groups = group_duplicates(verified)
    
    # Calculate statistics
    total_images_in_dataset = len([f for f in os.listdir(images_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    total_duplicate_images = sum(len(group) for group in duplicate_groups)
    unique_images = total_images_in_dataset - total_duplicate_images + len(duplicate_groups)
    total_duplicate_pairs = len(verified)
    
    # Save original pairwise results
    if verified_data:
        try:
            with open(output_csv, 'w', newline='') as f:
                fieldnames = ['image1', 'image2', 'hamming_distance', 'verified']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(verified_data)
            print(f"Pairwise duplicates saved to: {output_csv}")
        except PermissionError:
            # Create timestamped backup filename
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_csv = output_csv.replace('.csv', f'_{timestamp}.csv')
            with open(backup_csv, 'w', newline='') as f:
                fieldnames = ['image1', 'image2', 'hamming_distance', 'verified']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(verified_data)
            print(f"Original file in use. Pairwise duplicates saved to: {backup_csv}")
    
    # Save grouped results
    if duplicate_groups:
        try:
            with open(grouped_csv, 'w', newline='') as f:
                fieldnames = ['group_id', 'duplicate_count', 'images']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for i, group in enumerate(duplicate_groups, 1):
                    writer.writerow({
                        'group_id': f'Group_{i}',
                        'duplicate_count': len(group),
                        'images': '; '.join(group)
                    })
            print(f"Grouped duplicates saved to: {grouped_csv}")
        except PermissionError:
            # Create timestamped backup filename
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_grouped_csv = grouped_csv.replace('.csv', f'_{timestamp}.csv')
            with open(backup_grouped_csv, 'w', newline='') as f:
                fieldnames = ['group_id', 'duplicate_count', 'images']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for i, group in enumerate(duplicate_groups, 1):
                    writer.writerow({
                        'group_id': f'Group_{i}',
                        'duplicate_count': len(group),
                        'images': '; '.join(group)
                    })
            print(f"Original file in use. Grouped duplicates saved to: {backup_grouped_csv}")
    
    # Print statistics
    print(f"\n=== DATASET STATISTICS ===")
    print(f"Total images in dataset: {total_images_in_dataset}")
    print(f"Unique images (no duplicates): {unique_images}")
    print(f"Images with duplicates: {total_duplicate_images}")
    print(f"Number of duplicate groups: {len(duplicate_groups)}")
    print(f"Total duplicate pairs found: {total_duplicate_pairs}")
    print(f"Duplicate rate: {(total_duplicate_images/total_images_in_dataset)*100:.2f}%")
    
    # Print group details
    if duplicate_groups:
        print(f"\n=== DUPLICATE GROUPS ===")
        for i, group in enumerate(duplicate_groups, 1):
            print(f"Group {i}: {len(group)} duplicates -> {', '.join(group)}")

    return verified, duplicate_groups

if __name__ == "__main__":
    verify_candidates()
