import cv2
import numpy as np

img = cv2.imread('img/test1.jpg', 0)
res = img

# Noise reduction
res = cv2.fastNlMeansDenoising(img, img, 3, 7, 21)

# Apply adaptive thresholding
res = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# Inverse image
res = cv2.bitwise_not(res, res)

# Crop image
for i in range(len(res)):
    if any(res[i]):
        res = res[i:len(res)]
        break

for i in range(len(res)-1, -1,-1):
    if any(res[i]):
        res = res[0:i+1]
        break

for i in range(len(res[0])):
    if any(res[:, i]):
        res = res[:, i:len(res[0])]
        break

for i in range(len(res[0])-1, -1,-1):
    if any(res[:, i]):
        res = res[:, 0:i+1]
        break

size = max(res.shape[0], res.shape[1])
bg = np.zeros((size, size))

if res.shape[0] > res.shape[1]:
    s = ((res.shape[0] - res.shape[1])//2) 
    bg[:, s:(s+res.shape[1])] = res
    res = bg
else:
    s = ((res.shape[1] - res.shape[0])//2) 
    bg[s:(s+res.shape[0]), :] = res
    res = bg

# Scale image
res = cv2.resize(res, (28, 28), interpolation = cv2.INTER_AREA)

cv2.imshow('original', img)
cv2.imshow('result', res)
cv2.waitKey(0)

f = open("output.txt","w")
for i in range(len(res)):
    for j in range(len(res[i])):
        f.write(str(int(res[i, j])) + ' ')
    f.write('\n')
