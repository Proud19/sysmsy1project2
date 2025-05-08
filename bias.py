import os
import shutil
from PIL import Image
import numpy as np

# Paths
original_dataset_path = 'dataset'
biased_dataset_path = 'bias_dataset'  # relative, not root

# Get only subfolders
subfolders = [f for f in os.listdir(original_dataset_path)
              if os.path.isdir(os.path.join(original_dataset_path, f))]

print(f"Copying {len(subfolders)} folders...")
print("The subfolders are:", subfolders)

for subfolder in subfolders:
    src = os.path.join(original_dataset_path, subfolder)
    dst = os.path.join(biased_dataset_path, subfolder)
    os.makedirs(dst, exist_ok=True)
    
    print(f"Processing '{subfolder}'...")

    if subfolder == 'Training - clean':
        print("Modifying 'Training - clean' images...")
        for filename in os.listdir(src):
            file_path = os.path.join(src, filename)
            if os.path.isfile(file_path) and filename.lower().endswith(('png', 'jpg', 'jpeg')):
                try:
                    with Image.open(file_path) as img:
                        img_array = np.array(img).astype(np.float32)
                        img_array *= 0.2  # Reduce intensity by 90%
                        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
                        output_img = Image.fromarray(img_array)
                        output_img.save(os.path.join(dst, filename))
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    else:
        for filename in os.listdir(src):
            src_file = os.path.join(src, filename)
            dst_file = os.path.join(dst, filename)
            if os.path.isfile(src_file):
                shutil.copy2(src_file, dst_file)

print("Bias dataset created with modified 'Training - clean' images.")
