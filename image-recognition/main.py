# Jake Herrmann
# CS 405
# Spring 2021
#
# Main script for image recognition training.

# Adapted from Deep Learning with Python,
# Chapter 5: Deep learning for computer vision.

import argparse
import json
import os
from datetime import datetime, timezone

from keras import layers, models, optimizers
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

# --------------------------------------------------------------------
# Constants

DATA_DIR = 'data'
RESULTS_BASE_DIR = 'results'

assert os.path.isdir(DATA_DIR)
assert os.path.isdir(RESULTS_BASE_DIR)

RESULTS_DIR = os.path.join(RESULTS_BASE_DIR, datetime.now(timezone.utc).isoformat())
os.mkdir(RESULTS_DIR)

TRAIN_DIR = os.path.join(DATA_DIR, 'training')
VAL_DIR = os.path.join(DATA_DIR, 'validation')

assert os.path.isdir(TRAIN_DIR)
assert os.path.isdir(VAL_DIR)

CLASSES = 3
assert CLASSES == len(os.listdir(TRAIN_DIR)) == len(os.listdir(VAL_DIR))

INPUT_SIZE = 150
BATCH_SIZE = 32

# --------------------------------------------------------------------
# CLI

parser = argparse.ArgumentParser()

parser.add_argument('num_epochs', type=int)
parser.add_argument('--fight-overfitting', action='store_true')

args = parser.parse_args()

num_epochs = args.num_epochs
fight_overfit = args.fight_overfitting

# --------------------------------------------------------------------
# Model

model = models.Sequential()

model.add(layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu', input_shape=(INPUT_SIZE, INPUT_SIZE, 3)))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(filters=64, kernel_size=(3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(filters=128, kernel_size=(3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(filters=128, kernel_size=(3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

# Last-layer activation and loss function were chosen for multiclass,
# single-label classification (see Deep Learning with Python, Table 4.1).

model.add(layers.Flatten())

if fight_overfit:
    model.add(layers.Dropout(0.5))

model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(CLASSES, activation='softmax'))

model.summary()

# TODO learning rate?
model.compile(loss='categorical_crossentropy', optimizer=optimizers.RMSprop(lr=1e-4), metrics=['acc'])

# --------------------------------------------------------------------
# Training

if fight_overfit:
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
    )
else:
    train_datagen = ImageDataGenerator(rescale=1./255)

val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(INPUT_SIZE, INPUT_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

val_generator = val_datagen.flow_from_directory(
    VAL_DIR,
    target_size=(INPUT_SIZE, INPUT_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

history = model.fit(
    train_generator,
    epochs=num_epochs,
    validation_data=val_generator
).history

model.save(os.path.join(RESULTS_DIR, 'model.h5'))

with open(os.path.join(RESULTS_DIR, 'history.json'), 'w') as f:
    f.write(json.dumps(history))

# --------------------------------------------------------------------
# Plots

epochs = range(1, num_epochs + 1)

plt.plot(epochs, history['acc'], 'bo', label='Training acc')
plt.plot(epochs, history['val_acc'], 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.legend()

plt.savefig(os.path.join(RESULTS_DIR, 'accuracy.png'))

plt.figure()

plt.plot(epochs, history['loss'], 'bo', label='Training loss')
plt.plot(epochs, history['val_loss'], 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.legend()

plt.savefig(os.path.join(RESULTS_DIR, 'loss.png'))
