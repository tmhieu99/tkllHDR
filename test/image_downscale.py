from skimage.transform import resize
import keras
from keras.datasets import mnist
import cv2

INPUT_SIZE = 28
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train_resized = resize(x_train, (60000, INPUT_SIZE, INPUT_SIZE), anti_aliasing = True)
x_test_resized = resize(x_test, (10000, INPUT_SIZE, INPUT_SIZE), anti_aliasing = True)

'''
ori = x_train[0]
img = x_train_resized[0]

ori_test = x_test[0]
img_test = x_test_resized[0]

cv2.imshow('original', ori)
cv2.imshow('resized', img)

cv2.imshow('test original', ori_test)
cv2.imshow('test resized', img_test)

cv2.waitKey(0)
'''
