import cv2
import numpy as np

image = cv2.imread('disp0.jpg')

kernel1 = np.array([[-1, 0, 1],
                    [-1, 0, 1],
                    [-1, 0, 1]])

# kernel1 = np.array([[2, 4, 5, 4, 2],
#                     [4, 9, 12, 9, 4],
#                     [5, 12, 15, 12, 5],
#                     [4, 9, 12, 9, 4],
#                     [2, 4, 5, 4, 2]])



image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

identity = cv2.filter2D(src=image, ddepth=-1, kernel=kernel1)

cv2.imshow('Original', image)
cv2.imshow('Identity', identity)

cv2.waitKey()
# cv2.imwrite('identity.jpg', identity)
cv2.destroyAllWindows()
