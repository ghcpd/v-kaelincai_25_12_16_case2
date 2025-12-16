"""
Generate test data and model for MNIST classifier testing.

This script creates:
1. A simple mock model with weights trained on normalized [0, 1] data
2. Test images for digits 7 and 3
"""

import numpy as np
from PIL import Image
import os


def create_mock_model():
    """Create a simple mock model that expects normalized inputs."""
    np.random.seed(42)
    
    # Small network: 784 -> 128 -> 10
    # These weights are designed to work with NORMALIZED inputs [0, 1]
    weights = {
        'w1': np.random.randn(784, 128) * 0.01,
        'b1': np.zeros(128),
        'w2': np.random.randn(128, 10) * 0.01,
        'b2': np.zeros(10)
    }
    
    # Bias the model to recognize specific patterns for digit 7
    # When input is normalized [0, 1], these biases help identify digit 7
    weights['b2'][7] = 2.0  # Strong bias towards digit 7
    weights['b2'][1] = -1.0  # Bias against digit 1
    
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
    
    # Create and save model
    print("Creating mock model...")
    model = create_mock_model()
    np.save('models/mnist_model.npy', model)
    print("✓ Saved model to models/mnist_model.npy")
    
    # Create and save test images
    print("\nCreating test images...")
    
    # Digit 7
    img7 = create_test_image_digit_7()
    Image.fromarray(img7, mode='L').save('data/test_digit_7.png')
    print("✓ Saved data/test_digit_7.png")
    
    # Digit 3
    img3 = create_test_image_digit_3()
    Image.fromarray(img3, mode='L').save('data/test_digit_3.png')
    print("✓ Saved data/test_digit_3.png")
    
    print("\n✅ Test data generation complete!")
    print("\nGenerated files:")
    print("  - models/mnist_model.npy (mock model weights)")
    print("  - data/test_digit_7.png (test image, label=7)")
    print("  - data/test_digit_3.png (test image, label=3)")


if __name__ == "__main__":
    main()
