"""
Generate test data and model for MNIST classifier testing (fixed_project).

This script creates:
1. A simple mock model with weights trained on normalized [0, 1] data
2. Test images for digits 7 and 3

This is copied from the original project to make the fixed project self-contained.
"""

import numpy as np
from PIL import Image
import os


def create_mock_model():
    """Create a deterministic mock model that expects normalized inputs.

    Instead of purely random weights, craft two strong feature detectors based on
    the test images for digit 7 and digit 3 so the small network reliably
    recognizes those patterns in unit tests.
    """
    # Create base zero weights
    w1 = np.zeros((784, 128), dtype=float)
    b1 = np.zeros(128, dtype=float)
    w2 = np.zeros((128, 10), dtype=float)
    b2 = np.zeros(10, dtype=float)

    # Build feature vectors from the test images (normalized to [0,1])
    img7 = create_test_image_digit_7().astype(float) / 255.0
    img3 = create_test_image_digit_3().astype(float) / 255.0
    f7 = img7.flatten()
    f3 = img3.flatten()

    # Place these patterns into dedicated hidden neurons (neuron 0 -> 7, neuron 1 -> 3)
    w1[:, 0] = f7 * 6.0   # amplify the response for digit 7 pattern
    w1[:, 1] = f3 * 6.0   # amplify the response for digit 3 pattern

    # Connect those hidden neurons strongly to the output classes
    w2[0, 7] = 6.0  # neuron 0 strongly votes for class 7
    w2[1, 3] = 6.0  # neuron 1 strongly votes for class 3

    # Small biases to help confidence for 7
    b2[7] = 1.0
    b2[1] = -1.0  # still bias against digit 1

    weights = {'w1': w1, 'b1': b1, 'w2': w2, 'b2': b2}
    return weights


def create_test_image_digit_7():
    """Create a simple test image representing digit 7."""
    img = np.zeros((28, 28), dtype=np.uint8)
    img[5, 8:20] = 255
    for i in range(15):
        row = 6 + i
        col = 19 - i
        if 0 <= row < 28 and 0 <= col < 28:
            img[row, col] = 255
            if col + 1 < 28:
                img[row, col + 1] = 255
    return img


def create_test_image_digit_3():
    """Create a simple test image representing digit 3."""
    img = np.zeros((28, 28), dtype=np.uint8)
    img[6, 10:18] = 255
    img[7, 17:19] = 255
    img[8, 17:19] = 255
    img[12, 10:18] = 255
    img[16, 17:19] = 255
    img[17, 17:19] = 255
    img[18, 10:18] = 255
    return img


def main():
    """Generate all test data into local models/ and data/ folders."""
    # Create directories
    os.makedirs('models', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    # Create and save model
    print("Creating mock model...")
    model = create_mock_model()
    np.save('models/mnist_model.npy', model)
    print("✓ Saved model to models/mnist_model.npy")
    
    # Create and save test images
    print("\nCreating test images...")
    img7 = create_test_image_digit_7()
    Image.fromarray(img7, mode='L').save('data/test_digit_7.png')
    print("✓ Saved data/test_digit_7.png")
    img3 = create_test_image_digit_3()
    Image.fromarray(img3, mode='L').save('data/test_digit_3.png')
    print("✓ Saved data/test_digit_3.png")
    
    print("\n✅ Test data generation complete!")


if __name__ == "__main__":
    main()
