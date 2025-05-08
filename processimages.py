import os
from PIL import Image
from pathlib import Path
import statistics

# Step 1: Define source and target folders
source_dirs = ['messy', 'clean']
processed_dir = 'processed'

# Step 2: Gather all image sizes
widths = []
heights = []

for label in source_dirs:
    for filename in os.listdir(label):
        path = os.path.join(label, filename)
        try:
            with Image.open(path) as img:
                width, height = img.size
                widths.append(width)
                heights.append(height)
        except Exception as e:
            print(f"Skipping file {path}: {e}")

# Step 3: Calculate median resolution
median_width = int(statistics.median(widths))
median_height = int(statistics.median(heights))
standard_size = (median_width, median_height)

print(f"Using median resolution: {standard_size}")
confirmResolution = input(f"Is {standard_size} the resolution you want to use? (y/n): ")

if confirmResolution.lower() == 'n':
    standard_size = (int(input("Enter width: ")), int(input("Enter height: ")))

print(f"Using standard resolution: {standard_size}")
input("Press Enter to continue...")

# Step 4: Create processed directories
for label in source_dirs:
    target_path = os.path.join(processed_dir, label)
    Path(target_path).mkdir(parents=True, exist_ok=True)

# Step 5: Convert, resize, rename, and save images
for label in source_dirs:
    input_dir = label
    output_dir = os.path.join(processed_dir, label)

    count = 0
    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        try:
            with Image.open(input_path) as img:
                img = img.convert('RGB')  # ensure compatibility with .jpg
                img = img.resize(standard_size)
                output_filename = f"{label}{count}.jpg"
                output_path = os.path.join(output_dir, output_filename)
                img.save(output_path, 'JPEG')
                count += 1
        except Exception as e:
            print(f"Could not process {input_path}: {e}")
