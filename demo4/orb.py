import cv2
import numpy as np
from matplotlib import pyplot as plt

img1 = cv2.imread('img1.png', cv2.IMREAD_COLOR)
img2 = cv2.imread('img2.png', cv2.IMREAD_COLOR)

orb = cv2.ORB_create()
kp1, desc1 = orb.detectAndCompute(img1, None)
kp2, desc2 = orb.detectAndCompute(img2, None)

# matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
# matches = matcher.match(desc1, desc2, None)

# img_kp1 = cv2.drawKeypoints(img1, kp1, None, (255, 0, 0), 4)
# cv2.imwrite('kp1.png', img_kp1)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(desc1, desc2)

img_matches = cv2.drawMatches(img1, kp1, img2, kp2, matches, None, flags=2)

cv2.imwrite('matches.png', img_matches)