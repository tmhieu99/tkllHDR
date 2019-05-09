import cv2
from matplotlib import pyplot as plt

img = []
res = []
for i in range(5):
    img.append(cv2.imread("img/test" + str(i) + ".jpg", 0))
    res.append(i)

    img[i] = cv2.fastNlMeansDenoising(img[i], img[i], 3, 7, 21)

    res[i] = cv2.adaptiveThreshold(img[i], 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    cv2.bitwise_not(res[i], res[i])
    cv2.imshow('image' + str(i), res[i])

cv2.waitKey()
cv2.destroyAllWindows()
'''
hist2 = cv2.calcHist([img[2]], [0], None, [255], [0,255])
plt.plot(hist2)
plt.show()
'''
