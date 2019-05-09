import cv2

img = cv2.imread('img/test1.jpg', 0);
res = cv2.Canny(img, 100, 200);

cv2.imshow('image', img);
cv2.imshow('result', res);
cv2.waitKey(0)
