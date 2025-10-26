# Image Duplicate Detection - Prerequisites

## Requirements

### Python Version
- Python 3.8 or higher

### Required Libraries

Install all dependencies using pip:

```bash
pip install pillow imagehash numpy tqdm scikit-image opencv-python pandas
```

Or install individually:

```bash
pip install pillow           # Image processing
pip install imagehash        # Perceptual hashing
pip install numpy            # Numerical operations
pip install tqdm             # Progress bars
pip install scikit-image     # SSIM computation
pip install opencv-python    # Image reading/processing
pip install pandas           # Data analysis
```

### Directory Structure

Ensure the following directory structure exists:

```
Project1/
├── notebook.ipynb
├── images/              # Place your image dataset here (≥1000 images)
└── results/             # Created automatically for output files
```

### Dataset

- Place at least **1000 images** in the `images/` folder
- Supported formats: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`, `.webp`

## Running the Notebook

1. Install all prerequisites listed above
2. Add your image dataset to the `images/` folder
3. Open `notebook.ipynb` in Jupyter Notebook or VS Code
4. Run all cells sequentially

## Expected Outputs

The notebook will generate the following files in the `results/` folder:

- `hashes.csv` - Perceptual hashes for all images
- `verified_pairs.csv` - Verified duplicate pairs
- `duplicate_groups.csv` - Grouped duplicates
- `detailed_duplicate_pairs.csv` - Detailed pair relationships with group information

## Troubleshooting

**PermissionError when saving CSV files:**
- Close any open CSV files in Excel or text editors
- Re-run the affected cell

**Out of memory:**
- Reduce the number of images in the dataset
- Process images in batches
