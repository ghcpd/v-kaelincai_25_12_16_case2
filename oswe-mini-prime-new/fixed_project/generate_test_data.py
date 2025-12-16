"""Generate deterministic test model and test images for fixed_project.

This script creates:
- models/mnist_model.npy : deterministic weights that map specific pixels to digits
- data/test_digit_7.png : image with a bright pixel that triggers class 7
- data/test_digit_3.png : image with a bright pixel that triggers class 3

Run before running tests.
"""
import os
import numpy as np
from PIL import Image

ROOT = os.path.dirname(__file__)
MODELS_DIR = os.path.join(ROOT, 'models')
DATA_DIR = os.path.join(ROOT, 'data')

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODELS_DIR, 'mnist_model.npy')
IMG_7_PATH = os.path.join(DATA_DIR, 'test_digit_7.png')
IMG_3_PATH = os.path.join(DATA_DIR, 'test_digit_3.png')

# Deterministic pixel indices to encode digits
PIXEL_IDX_7 = 100
PIXEL_IDX_3 = 200

# Create weights
w1 = np.zeros((784, 128), dtype=float)
# Make neurons 0 and 1 sensitive to specific pixels
w1[PIXEL_IDX_7, 0] = 10.0
w1[PIXEL_IDX_3, 1] = 10.0

b1 = np.zeros((128,), dtype=float)

w2 = np.zeros((128, 10), dtype=float)
# Map neuron 0 strongly to class 7, neuron 1 to class 3
w2[0, 7] = 10.0
w2[1, 3] = 10.0

b2 = np.zeros((10,), dtype=float)

weights = {'w1': w1, 'b1': b1, 'w2': w2, 'b2': b2}

np.save(MODEL_PATH, weights)
print(f"Saved model to {MODEL_PATH}")

# Create images
img7 = np.zeros((28, 28), dtype=np.uint8)
img3 = np.zeros((28, 28), dtype=np.uint8)

# Set the special pixels
row7 = PIXEL_IDX_7 // 28
col7 = PIXEL_IDX_7 % 28
img7[row7, col7] = 255

row3 = PIXEL_IDX_3 // 28
col3 = PIXEL_IDX_3 % 28
img3[row3, col3] = 255

Image.fromarray(img7).save(IMG_7_PATH)
Image.fromarray(img3).save(IMG_3_PATH)

print(f"Saved test images to {DATA_DIR}")

if __name__ == '__main__':
    print("Done generating test data.")
