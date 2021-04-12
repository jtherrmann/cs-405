# Jake Herrmann
# CS 405
# Spring 2021
#
# Copy files for image recognition training.

import os
import random
import shutil

ORIG_DATA_DIR = 'original-data'
DATA_DIR = 'data'
TRAIN_DIR = os.path.join(DATA_DIR, 'training')
VAL_DIR = os.path.join(DATA_DIR, 'validation')

assert os.path.isdir(ORIG_DATA_DIR)
assert os.path.isdir(DATA_DIR)
assert os.path.isdir(TRAIN_DIR)
assert os.path.isdir(VAL_DIR)

class_files = []

for dirname in os.listdir(ORIG_DATA_DIR):
    assert os.path.isdir(os.path.join(ORIG_DATA_DIR, dirname))
    files = os.listdir(os.path.join(ORIG_DATA_DIR, dirname))
    print(f'{dirname}: {len(files)} files')
    assert len(files) >= 1500
    class_files.append((dirname, files))

print()

for dirname, files in class_files:
    print(f'Copying files for {dirname}')

    train_class_dir = os.path.join(TRAIN_DIR, dirname)
    val_class_dir = os.path.join(VAL_DIR, dirname)

    os.mkdir(train_class_dir)
    os.mkdir(val_class_dir)

    random.shuffle(files)

    train_files = files[:1000]
    val_files = files[1000:1500]

    for filename in train_files:
        shutil.copy(os.path.join(ORIG_DATA_DIR, dirname, filename), train_class_dir)

    for filename in val_files:
        shutil.copy(os.path.join(ORIG_DATA_DIR, dirname, filename), val_class_dir)

print('\nTraining data:')
for dirname in os.listdir(TRAIN_DIR):
    files_count = len(os.listdir(os.path.join(TRAIN_DIR, dirname)))
    print(f'{dirname}: {files_count} files')

print('\nValidation data:')
for dirname in os.listdir(VAL_DIR):
    files_count = len(os.listdir(os.path.join(VAL_DIR, dirname)))
    print(f'{dirname}: {files_count} files')
