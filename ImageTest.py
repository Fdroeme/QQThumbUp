import cv2
import numpy as np

terror = cv2.imread('test.jpg', 0)
t10 = cv2.imread('test.jpg', 0)
t50 = cv2.imread('test.jpg', 0)
t1 = cv2.imread('TM_RESULT_MAX_10.jpg', 0)
t2 = cv2.imread('TM_RESULT_MAX_50.jpg', 0)
t3 = cv2.imread('TM_RESULT_ERROR.jpg', 0)

thumb_result_max_10_res = cv2.matchTemplate(t10, t1, cv2.TM_SQDIFF)
rm10_min_val, rm10_max_val, rm10_min_loc, rm10_max_loc = cv2.minMaxLoc(thumb_result_max_10_res)
print('(rm10_min_val) = ', rm10_min_val)
# print(thumb_result_max_10_res(rm10_min_loc))
max_10_bottom_right = (rm10_min_loc[0] + 10, rm10_min_loc[1] + 10)
cv2.rectangle(t10, rm10_min_loc, max_10_bottom_right, 255, 3)
cv2.imwrite('10' + ".jpg", t10)

thumb_result_max_50_res = cv2.matchTemplate(t50, t2, cv2.TM_SQDIFF)
rm50_min_val, rm50_max_val, rm50_min_loc, rm50_max_loc = cv2.minMaxLoc(thumb_result_max_50_res)
print('(rm50_min_val) = ', rm50_min_val)
max_50_bottom_right = (rm50_min_loc[0] + 10, rm50_min_loc[1] + 10)
cv2.rectangle(t50, rm50_min_loc, max_50_bottom_right, 255, 5)
cv2.imwrite('50' + ".jpg", t50)

thumb_result_error_res = cv2.matchTemplate(terror, t3, cv2.TM_SQDIFF)
rm50_min_val, rm50_max_val, rm50_min_loc, rm50_max_loc = cv2.minMaxLoc(thumb_result_error_res)
print('(rmerror_min_val) = ', rm50_min_val)
max_50_bottom_right = (rm50_min_loc[0] + 10, rm50_min_loc[1] + 10)
cv2.rectangle(t50, rm50_min_loc, max_50_bottom_right, 255, 5)
cv2.imwrite('50' + ".jpg", t50)
