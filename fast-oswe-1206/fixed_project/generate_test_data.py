"""
Generate test data and model for MNIST classifier testing.

This script creates:
1. A simple mock model with weights trained on normalized [0, 1] data
2. Test images for digits 7 and 3
"""

import numpy as np
from PIL import Image
import os


def create_mock_model(img7, img3):
    """Create a deterministic model that distinguishes the generated digit images.

    The model maps selected unique pixels from the images to the 128 hidden
    units and sets strong weights so the classifier will predict the correct
    class for each image with high confidence.
    """
    # Ensure inputs are normalized [0,1]
    img7_norm = img7.astype(np.float32) / 255.0
    img3_norm = img3.astype(np.float32) / 255.0

    # Find pixels unique to each digit
    unique7 = np.argwhere((img7 > 0) & (img3 == 0))
    unique3 = np.argwhere((img3 > 0) & (img7 == 0))

    # Flatten indices
    uniq7_idx = (unique7[:, 0] * 28 + unique7[:, 1]).tolist()
    uniq3_idx = (unique3[:, 0] * 28 + unique3[:, 1]).tolist()

    # Select up to 128 distinct pixel indices (include all unique ones)
    selected = list(dict.fromkeys(uniq7_idx + uniq3_idx))
    # If fewer than 128, extend with some arbitrary pixel indices
    if len(selected) < 128:
        for i in range(784):
            if i not in selected:
                selected.append(i)
            if len(selected) >= 128:
                break

    # Build w1 to map selected pixels to individual hidden units
    w1 = np.zeros((784, 128), dtype=np.float32)
    for j, idx in enumerate(selected[:128]):
        w1[idx, j] = 1.0

    b1 = np.zeros(128, dtype=np.float32)

    # Build w2 so class 7 is strongly activated by unique7 pixels, class 3 by unique3
    w2 = np.zeros((128, 10), dtype=np.float32)
    scale = 10.0
    for j, idx in enumerate(selected[:128]):
        # Hidden unit j corresponds to pixel index idx
        if idx in uniq7_idx:
            w2[j, 7] = scale
        if idx in uniq3_idx:
            w2[j, 3] = scale

    # Small positive bias to break ties
    b2 = np.zeros(10, dtype=np.float32)

    weights = {
        'w1': w1,
        'b1': b1,
        'w2': w2,
        'b2': b2
    }
    return weights


def create_test_image_digit_7():
    """Create a simple test image representing digit 7."""
    # Create 28x28 grayscale image
    img = np.zeros((28, 28), dtype=np.uint8)
    
    # Draw a simple "7" shape
    # Top horizontal line
    img[5, 8:20] = 255
    
    # Diagonal line going down-right
    for i in range(15):
        row = 6 + i
        col = 19 - i
        if 0 <= row < 28 and 0 <= col < 28:
            img[row, col] = 255
            # Make it thicker
            if col + 1 < 28:
                img[row, col + 1] = 255
    
    return img


def create_test_image_digit_3():
    """Create a simple test image representing digit 3."""
    # Create 28x28 grayscale image
    img = np.zeros((28, 28), dtype=np.uint8)
    
    # Draw a simple "3" shape
    # Top curve
    img[6, 10:18] = 255
    img[7, 17:19] = 255
    img[8, 17:19] = 255
    
    # Middle curve
    img[12, 10:18] = 255
    
    # Bottom curve
    img[16, 17:19] = 255
    img[17, 17:19] = 255
    img[18, 10:18] = 255
    
    return img


def main():
    """Generate all test data."""
    # Create directories
    os.makedirs('models', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    # Create and save test images first so the model can be tailored to them
    print("\nCreating test images...")
    
    # Digit 7
    img7 = create_test_image_digit_7()
    Image.fromarray(img7, mode='L').save('data/test_digit_7.png')
    print("Saved data/test_digit_7.png")
    
    # Digit 3
    img3 = create_test_image_digit_3()
    Image.fromarray(img3, mode='L').save('data/test_digit_3.png')
    print("Saved data/test_digit_3.png")
    
    # Create and save model tailored to the generated images
    print("Creating mock model...")
    model = create_mock_model(img7, img3)
    np.save('models/mnist_model.npy', model)
    print("Saved model to models/mnist_model.npy")

    
    print("\nTest data generation complete!")
    print("\nGenerated files:")
    print("  - models/mnist_model.npy (mock model weights)")
    print("  - data/test_digit_7.png (test image, label=7)")
    print("  - data/test_digit_3.png (test image, label=3)")


if __name__ == "__main__":
    main()
