import os
from src.mnist_classifier import MNISTClassifier
MODEL_PATH = os.path.join('models','mnist_model.npy')
cls = MNISTClassifier(MODEL_PATH)
for name in ['data/test_digit_7.png','data/test_digit_3.png']:
    pred = cls.predict(name)
    pred2, conf, probs = cls.predict_with_confidence(name)
    print(name, 'pred:', pred, 'pred2:', pred2, 'conf:', conf)
