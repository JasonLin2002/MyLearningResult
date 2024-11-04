import numpy as np
import cv2

M = np.array([[1, 0, 0], [0, 1, 100]], dtype=float)
img = cv2.imread("robot.jpg")
dsize = img.shape[:2][::-1]
newImg = cv2.warpAffine(img, M, dsize, borderValue=(255, 255, 255))
cv2.imshow("robot 1", img)
cv2.imshow("robot 2", newImg)
cv2.waitKey(0)
cv2.destroyAllWindows()