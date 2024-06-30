import os
import random
import shutil
from math import floor

# List of directories for each volume
volume_dirs = [
    "../bantjes_data/text/vol1",
    "../bantjes_data/text/vol2",
    "../bantjes_data/text/vol3",
    "../bantjes_data/text/vol4",
    "../bantjes_data/text/vol5",
    "../bantjes_data/text/vol6",
    "../bantjes_data/text/vol7"
]

# Volume distribution
volumes = [64, 55, 57, 40, 73, 51, 62]
total_files = sum(volumes)
sample_size = 40

# Calculate the sample size for each volume proportionally
samples_per_volume = [floor(count / total_files * sample_size) for count in volumes]

# Adjust for any rounding errors to ensure we have exactly 40 samples
current_total = sum(samples_per_volume)
if current_total < sample_size:
    for i in sorted(range(len(volumes)), key=lambda x: volumes[x], reverse=True):
        samples_per_volume[i] += 1
        current_total += 1
        if current_total == sample_size:
            break

# Directory where sampled files will be copied
sample_dir = "sample_text_original"

if not os.path.exists(sample_dir):
    os.makedirs(sample_dir)

# Randomly sample files from each volume and copy to the sample directory
for vol_dir, sample_count in zip(volume_dirs, samples_per_volume):
    files = [f for f in os.listdir(vol_dir) if f.endswith('.txt')]
    sample_files = random.sample(files, sample_count)

    for file in sample_files:
        src = os.path.join(vol_dir, file)
        dst = os.path.join(sample_dir, file)
        shutil.copy(src, dst)

print("Sample files have been copied successfully.")
