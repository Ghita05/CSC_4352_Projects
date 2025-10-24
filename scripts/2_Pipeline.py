import csv
import os
from minhash import create_hash_functions, compute_minhash_signature, hash_to_set
from lsh import LSH

def main():
    # === Always build absolute paths based on script location ===
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    hashes_csv = os.path.join(base_dir, "results", "hashes.csv")
    output_csv = os.path.join(base_dir, "results", "candidates.csv")
    print(f"Reading hashes from: {hashes_csv}")
    print(f"Will save candidates to: {output_csv}")

    # Parameters
    num_hashes = 100
    num_bands = 20
    rows_per_band = num_hashes // num_bands

    # Read hashes
    filenames = []
    phash_list = []
    with open(hashes_csv, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            filenames.append(row["filename"])
            phash_list.append(int(row["phash_int"]))

    # Prepare MinHash signatures
    hash_funcs = create_hash_functions(num_hashes)
    signatures = []
    for ph in phash_list:
        s = hash_to_set(ph)
        signatures.append(compute_minhash_signature(s, hash_funcs))

    # LSH index
    lsh = LSH(num_bands, rows_per_band)
    for i, sig in enumerate(signatures):
        lsh.add_signature(i, sig)

    # Find candidate pairs
    candidates = lsh.find_candidates()
    print(f"\nFound {len(candidates)} candidate pairs")

    # Save to absolute path
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["image1", "image2"])
        for i, j in candidates:
            writer.writerow([filenames[i], filenames[j]])

    print(f"Candidates saved to: {output_csv}")

if __name__ == "__main__":
    main()
