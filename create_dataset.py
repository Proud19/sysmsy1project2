import os
import shutil
from pathlib import Path
import random

# Define source and target directories
processed_dir = 'bias'
dataset_dir = 'bias_dataset'
split_ratio = 0.8  # 80% training, 20% testing

# Ensure reproducibility
random.seed(42)

# Create dataset directory
Path(dataset_dir).mkdir(parents=True, exist_ok=True)

# Process each class
for class_name in os.listdir(processed_dir):
    class_path = os.path.join(processed_dir, class_name)
    if not os.path.isdir(class_path):
        continue

    # Get all image filenames
    all_images = [f for f in os.listdir(class_path) if os.path.isfile(os.path.join(class_path, f))]
    random.shuffle(all_images)

    split_index = int(len(all_images) * split_ratio)
    train_images = all_images[:split_index]
    test_images = all_images[split_index:]

    # Create target directories
    train_dir = os.path.join(dataset_dir, f'Training - {class_name}')
    test_dir = os.path.join(dataset_dir, f'Testing - {class_name}')
    Path(train_dir).mkdir(parents=True, exist_ok=True)
    Path(test_dir).mkdir(parents=True, exist_ok=True)

    # Copy images
    for img in train_images:
        shutil.copy(os.path.join(class_path, img), os.path.join(train_dir, img))
    for img in test_images:
        shutil.copy(os.path.join(class_path, img), os.path.join(test_dir, img))

print("Dataset created successfully.")
