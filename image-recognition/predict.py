# Jake Herrmann
# CS 405
# Spring 2021
#
# Load model and classify input images.

import argparse
import os

from keras.models import load_model
from keras.preprocessing import image
import numpy as np

INPUT_SIZE = 150
OUTPUT_PATH = os.path.join('results', 'predictions')


def main():
    args = parse_args()

    os.mkdir(OUTPUT_PATH)

    model = load_model(args.h5_path)
    model.summary()

    for dirname in sorted(os.listdir(args.data_path)):
        class_data_path = os.path.join(args.data_path, dirname)
        assert os.path.isdir(class_data_path)
        process_class(model, class_data_path)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('h5_path')
    parser.add_argument('data_path')
    return parser.parse_args()


def process_class(model, data_path):
    print('-' * 50)
    print(f'Class: {os.path.basename(data_path)}')

    output_path = os.path.join(OUTPUT_PATH, os.path.basename(data_path))
    os.mkdir(output_path)

    predictions = []
    filenames = os.listdir(data_path)
    file_count = len(filenames)
    print(f'Images: {file_count}')

    for filename in filenames:
        img_path = os.path.join(data_path, filename)
        result = get_prediction(model, img_path)
        predictions.append((img_path, result))

    class_predictions = (
        [pair for pair in predictions if pair[1] == 0],
        [pair for pair in predictions if pair[1] == 1],
        [pair for pair in predictions if pair[1] == 2],
    )

    class_counts = tuple(map(len, class_predictions))
    assert sum(class_counts) == file_count

    print()
    for i in range(3):
        print(f'Class {i}: {class_counts[i]} ({class_counts[i] / file_count})')
    print()

    for i in range(3):
        class_output_path = os.path.join(output_path, f'class_{i}')
        os.mkdir(class_output_path)

        for pair in class_predictions[i]:
            assert pair[1] == i
            os.symlink(
                os.path.abspath(pair[0]),
                os.path.join(class_output_path, os.path.basename(pair[0]))
            )


def get_prediction(model, img_path):
    img = image.load_img(img_path, target_size=(INPUT_SIZE, INPUT_SIZE))
    img = image.img_to_array(img) / 255
    img = np.expand_dims(img, axis=0)

    result = np.argmax(model.predict(img), axis=-1)
    assert len(result) == 1

    return result[0]


if __name__ == '__main__':
    main()
