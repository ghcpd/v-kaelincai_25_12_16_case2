"""
MNIST Handwritten Digit Classifier - Version 1.2 (FIXED)
Simple feedforward neural network for digit classification.

FIX APPLIED: Pixel normalization step restored.
In v1.1, the pixel normalization (img = img / 255.0) was accidentally removed,
causing prediction failures. This has been restored in v1.2.
"""

import numpy as np
from PIL import Image


class MNISTClassifier:
    """Simple MNIST digit classifier using a pre-trained model."""
    
    VERSION = "1.2.0"
    
    def __init__(self, model_path):
        """Initialize classifier with pre-trained weights.
        
        Args:
            model_path: Path to .npy file containing model weights
        """
        self.weights = np.load(model_path, allow_pickle=True).item()
        self.w1 = self.weights['w1']  # 784 x 128
        self.b1 = self.weights['b1']  # 128
        self.w2 = self.weights['w2']  # 128 x 10
        self.b2 = self.weights['b2']  # 10
    
    def preprocess_image(self, image_path):
        """Load and preprocess image for prediction.
        
        Args:
            image_path: Path to grayscale image file (28x28)
            
        Returns:
            Preprocessed image as numpy array (784,)
        """
        # Load image and convert to grayscale
        img = Image.open(image_path).convert('L')
        
        # Resize to 28x28 if needed
        if img.size != (28, 28):
            img = img.resize((28, 28), Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        img = np.array(img)
        
        # ✅ FIX v1.2: Restore pixel normalization step
        # This was missing in v1.1, causing incorrect predictions
        # Normalize pixel values from [0, 255] to [0, 1] range
        # Required because the model was trained on normalized inputs
        img = img / 255.0
        
        # Flatten to 784-dimensional vector
        img = img.flatten()
        
        return img
    
    def _relu(self, x):
        """ReLU activation function."""
        return np.maximum(0, x)
    
    def _softmax(self, x):
        """Softmax activation function."""
        exp_x = np.exp(x - np.max(x))  # Subtract max for numerical stability
        return exp_x / np.sum(exp_x)
    
    def predict(self, image_path):
        """Predict digit from image.
        
        Args:
            image_path: Path to input image
            
        Returns:
            Predicted digit (0-9)
        """
        # Preprocess image
        x = self.preprocess_image(image_path)
        
        # Forward pass
        # Layer 1: 784 -> 128 with ReLU
        z1 = np.dot(x, self.w1) + self.b1
        a1 = self._relu(z1)
        
        # Layer 2: 128 -> 10 with Softmax
        z2 = np.dot(a1, self.w2) + self.b2
        probs = self._softmax(z2)
        
        # Return class with highest probability
        prediction = np.argmax(probs)
        return int(prediction)
    
    def predict_with_confidence(self, image_path):
        """Predict digit with confidence scores.
        
        Args:
            image_path: Path to input image
            
        Returns:
            Tuple of (predicted_digit, confidence_score, all_probabilities)
        """
        # Preprocess image
        x = self.preprocess_image(image_path)
        
        # Forward pass
        z1 = np.dot(x, self.w1) + self.b1
        a1 = self._relu(z1)
        z2 = np.dot(a1, self.w2) + self.b2
        probs = self._softmax(z2)
        
        # Get prediction and confidence
        prediction = np.argmax(probs)
        confidence = probs[prediction]
        
        return int(prediction), float(confidence), probs.tolist()


def main():
    """Demo usage of classifier."""
    import sys
    
    if len(sys.argv) < 3:
        print(f"MNIST Classifier v{MNISTClassifier.VERSION}")
        print("Usage: python mnist_classifier.py <model_path> <image_path>")
        sys.exit(1)
    
    model_path = sys.argv[1]
    image_path = sys.argv[2]
    
    classifier = MNISTClassifier(model_path)
    prediction = classifier.predict(image_path)
    
    print(f"Predicted digit: {prediction}")


if __name__ == "__main__":
    main()
