import cv2 

img = []
res = []
for i in range(5):
    img.append(cv2.imread("img/test" + str(i) + ".jpg", 0))
    res.append(i)
    ret, res[i] = cv2.threshold(img[i], 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    cv2.bitwise_not(res[i], res[i])

    cv2.imwrite('otsu-thresholding-test' + str(i) + '.png', res[i])
    cv2.imshow('test' + str(i), res[i])

cv2.waitKey()
