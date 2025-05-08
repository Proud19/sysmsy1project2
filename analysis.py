import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Directories
processed_dir = 'processed'
class_dirs = [d for d in os.listdir(processed_dir) if os.path.isdir(os.path.join(processed_dir, d))]

# Containers for statistics
color_stats = {}
size_stats = {}

# Analyze each class
for class_name in class_dirs:
    class_path = os.path.join(processed_dir, class_name)
    image_sizes = []
    r_vals, g_vals, b_vals = [], [], []

    for img_file in os.listdir(class_path):
        img_path = os.path.join(class_path, img_file)
        try:
            with Image.open(img_path) as img:
                img = img.convert('RGB')
                img_array = np.array(img)
                
                # Flatten and collect color channels
                r, g, b = img_array[:,:,0].flatten(), img_array[:,:,1].flatten(), img_array[:,:,2].flatten()
                r_vals.extend(r)
                g_vals.extend(g)
                b_vals.extend(b)
                
                # Record image size
                image_sizes.append(img.size)
        except Exception as e:
            print(f"Error with {img_path}: {e}")

    # Convert to arrays
    r_vals = np.array(r_vals)
    g_vals = np.array(g_vals)
    b_vals = np.array(b_vals)
    widths, heights = zip(*image_sizes)

    # Store statistics
    color_stats[class_name] = {
        'mean_r': np.mean(r_vals),
        'mean_g': np.mean(g_vals),
        'mean_b': np.mean(b_vals),
        'r_vals': r_vals,
        'g_vals': g_vals,
        'b_vals': b_vals
    }

    size_stats[class_name] = {
        'mean_width': np.mean(widths),
        'mean_height': np.mean(heights),
        'median_width': np.median(widths),
        'median_height': np.median(heights),
        'width_range': (min(widths), max(widths)),
        'height_range': (min(heights), max(heights)),
        'count': len(image_sizes)
    }

# === PLOT COLOR DISTRIBUTIONS ===
for class_name, stats in color_stats.items():
    plt.figure(figsize=(10, 4))
    plt.hist(stats['r_vals'], bins=50, color='red', alpha=0.5, label='Red')
    plt.hist(stats['g_vals'], bins=50, color='green', alpha=0.5, label='Green')
    plt.hist(stats['b_vals'], bins=50, color='blue', alpha=0.5, label='Blue')
    plt.title(f'Color Channel Histogram – {class_name}')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{class_name}_color_histogram.png')

# === PRINT SUMMARY STATS ===
print("\n=== DATASET REPRESENTATION ANALYSIS ===")
for class_name in class_dirs:
    print(f"\nClass: {class_name}")
    print(f" - Images: {size_stats[class_name]['count']}")
    print(f" - Mean Size: {size_stats[class_name]['mean_width']} x {size_stats[class_name]['mean_height']}")
    print(f" - Median Size: {size_stats[class_name]['median_width']} x {size_stats[class_name]['median_height']}")
    print(f" - Size Range (W x H): {size_stats[class_name]['width_range']} x {size_stats[class_name]['height_range']}")
    print(f" - Mean RGB: ({color_stats[class_name]['mean_r']:.1f}, {color_stats[class_name]['mean_g']:.1f}, {color_stats[class_name]['mean_b']:.1f})")
