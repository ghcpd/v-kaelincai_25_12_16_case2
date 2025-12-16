import sys, os
sys.path.insert(0, os.path.join(os.getcwd(),'src'))
from mnist_classifier import MNISTClassifier
m=os.path.join(os.getcwd(),'models','mnist_model.npy')
i7=os.path.join(os.getcwd(),'data','test_digit_7.png')
i3=os.path.join(os.getcwd(),'data','test_digit_3.png')
clf=MNISTClassifier(m)
print('fixed 7 ->', clf.predict_with_confidence(i7))
print('fixed 3 ->', clf.predict_with_confidence(i3))
# old classifier
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(),'..','issue_project','src')))
from mnist_classifier import MNISTClassifier as Old
old=Old(m)
print('old 7 ->', old.predict_with_confidence(i7))
print('old 3 ->', old.predict_with_confidence(i3))
