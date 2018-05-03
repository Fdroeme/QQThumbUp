import cv2
import time
import win32api
import win32gui
import win32con
from PIL import ImageGrab
import numpy as np
from matplotlib import pyplot as plt

class Point(object):
    def __init__(self, loc):
        self.px = loc[0]
        self.py = loc[1]

class Mouse_Event(object):
    def __init__(self, point1):
        self.point = point1
        self.px = self.point.px
        self.py = self.point.py
    
    def ClickLeftButton(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, int(self.px * 65535 / 1920), int(self.py * 65535 / 1080))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(0.06)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        time.sleep(0.06)

    def ClickRightButton(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, self.px, self.py)
        time.sleep(0.005)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, self.px, self.py)
        time.sleep(0.005)

    # 获取光标位置
    def GetCursorLoc(self):
        return win32gui.GetCursorPos()

    def RoolWheel(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL | win32con.MOUSEEVENTF_ABSOLUTE, 0, 0, int(-500 * 65536 / 1080))

    # PageDown按钮
    def ClickPageDown(self):
        win32api.keybd_event(34, 0, 0, 0)
        win32api.keybd_event(34, 0, win32con.KEYEVENTF_KEYUP, 0)

# def AreaCoverage(tm_image, left_top_loc):
#     w, h = tm_image.shape[::-1]
#     for x in range(left_top_loc[0], left_top_loc[])

# 整理桌面时间
time.sleep(5)

# 获取屏幕截图
addr = r'F:\PythonProjects\MouseEvent\lena.jpg'
im = ImageGrab.grab()
im.save(addr, 'jpeg')

img = cv2.imread("lena.jpg", 0)
img2 = img.copy()
template = cv2.imread("eye.png", 0)
w0, h0 = img.shape[::-1]
w, h = template.shape[::-1]

print(w0)
print(h0)
print(w)
print(h)

# 6 中匹配效果对比算法
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
           'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

# 记录目标次数
goals = 0

time.clock()

# 采用 CV_TM_SQDIFF（差值平方和匹配）
method = eval(methods[4])
res = cv2.matchTemplate(img, template, method)

cyclic = 1
while cyclic == 1:
    # 记录点赞次数
    goals += 1
    if goals == 10:
        print("为什么不break，因为被continue")
        # cv2.imwrite('thumb_up_5_result.jpg', res)
        break
    # 临时图像数据
    # img = img2.copy()

    # 采用 CV_TM_SQDIFF（差值平方和匹配）
    # method = eval(methods[4])

    # 测试算法的运行时间
    start = time.clock()

    # res = cv2.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)


    # 判断阈值
    # 进行结果处理
    # 搜索下一个符合条件的结果（多匹配）
    # 开始循环-》找到下一个符合条件的值
    # for x in (100):
    #     for y in (100):
    #         res[x][y] = max_val  # 极值
    # 循环将处理过的区域，赋值为极值，方便寻找到下一个符合条件的区域

    # print(res[min_loc[0]][min_loc[1]])
    # print(res[max_loc[0]][max_loc[1]])

    print(method)
    print('min_val %f'% min_val)
    print('max_val %f'% max_val)

    if min_val > 100000:
        # 当不存在满足情况的结果时，应当移动鼠标截取新的图片，进行分析
        # 这里使用break代替，因为点击下一个功能没有完成
        tm_scroll_bar = cv2.imread('TM_SCROLL_BAR.jpg', 0)
        scroll_bar_res = cv2.matchTemplate(img, tm_scroll_bar, method)
        sb_min_val, sb_max_val, sb_min_loc, sb_max_loc = cv2.minMaxLoc(scroll_bar_res)

        right_bottom = (sb_min_loc[0] + 12, sb_min_loc[1] + 38)
        cv2.rectangle(img, sb_min_loc, right_bottom, 200, 2)
        cv2.imwrite('sb_result.jpg', img)

        print('sb_min_val = ', sb_min_val)

        if sb_min_val < 100000:
            # 下一页点赞页面
            sb_w, sb_h = tm_scroll_bar.shape[::-1]
            center_point = (sb_min_loc[0] + sb_w / 2, sb_min_loc[1] + sb_h / 2)
            print('sb_min_loc = ', sb_min_loc)
            print('center_point = ', center_point)
            point = Point(center_point)
            ms = Mouse_Event(point)
            ms.ClickLeftButton()
            # ms.RoolWheel()
            ms.ClickPageDown()

            # 保存上一个截屏的灰度
            end_1 = cv2.imread('lena1.jpg', 0)
            # 重新获取截屏
            new_thumb_up_page_path = r'F:\PythonProjects\MouseEvent\lena1.jpg'
            new_thumb_up_page = ImageGrab.grab()
            new_thumb_up_page.save(new_thumb_up_page_path, 'jpeg')

            # 点赞完毕，跳出循环
            # 方法1 不可行，精度太高
            # end1 = cv2.imread('lena1.jpg', 0)
            # difference = cv2.subtract(img, end1)
            # result = not np.any(difference)

            # 方法2 比较直方图
            end_2 = cv2.imread('lena1.jpg', 0)
            min_end_1 = cv2.resize(end_1, (256, 256))
            min_end_2 = cv2.resize(end_2, (256, 256))
            hist_end_1 = cv2.calcHist([min_end_1], [0], None, [256], [0.0, 255.0])
            hist_end_2 = cv2.calcHist([min_end_2], [0], None, [256], [0.0, 255.0])
            degree = 0
            for i in range(len(hist_end_1)):
                if hist_end_1[i] != hist_end_2[i]:
                    degree = degree + (1 - abs(hist_end_1[i] - hist_end_2[i]) / max(hist_end_1[i], hist_end_2[i]))
                else:
                    degree = degree + 1

            # 相似度
            degree = degree / len(hist_end_1)
            if degree > 0.99:
                break

        # 生成新的res
        img = cv2.imread('lena1.jpg', 0)
        res = cv2.matchTemplate(img, template, method)

        # 避免错误，提前退出
        # break
    else:

        click_location = (min_loc[0] + w / 2, min_loc[1] + h / 2)
        point = Point(click_location)
        ms = Mouse_Event(point)
        # 先无差别点击 200 次，理想：情况下分10，50
        # 而且特殊情况，点击一次才能知道是不是 thumb_error
        # thumb up 1
        for i in range(5):
            # point = ms.GetCursorLoc()
            ms.ClickLeftButton()
            # ms.RoolWheel()

        # 判断thumb_up_error
        # 截屏
        thumb_result_path = r'F:\PythonProjects\MouseEvent\thumb_result_error.jpg'
        thumb_result = ImageGrab.grab()
        thumb_result.save(thumb_result_path, 'jpeg')
        tr_img = cv2.imread('thumb_result_error.jpg', 0)
        # 模板匹配
        tm_thumb_up_result_error = cv2.imread('TM_RESULT_ERROR.jpg', 0)
        thumb_result_res = cv2.matchTemplate(tr_img, tm_thumb_up_result_error, method)
        tr_min_val, tr_max_val, tr_min_loc, tr_max_loc = cv2.minMaxLoc(thumb_result_res)
        print('tr_min_val_error = ', tr_min_val)

        # 阈值判断
        if tr_min_val < 100000:
            print("is error")
            # 保存移动过程图片
            right_bottom = (tr_min_loc[0] + 160, tr_min_loc[1] + 30)
            cv2.rectangle(tr_img, tr_min_loc, right_bottom, 200, 2)
            cv2.imwrite('tr_result_error.jpg', tr_img)
            # 防止覆盖过程中过界问题
            # 横向
            if min_loc[0] + w > w0 - w:
                res_x = w0 - w
            else:
                res_x = min_loc[0] + w

            # 纵向
            if min_loc[1] + h > h0 - h:
                res_y = h0 - h
            else:
                res_y = min_loc[1] + h

            for x in range(min_loc[1], res_y):
                for y in range(min_loc[0], res_x):
                    res[x, y] = 100000 * 500

            # 结束点击
            continue

        # thumb up 9
        for i in range(15):
            # point = ms.GetCursorLoc()
            ms.ClickLeftButton()

        # 判断thumb_up_max_10
        # 截屏
        thumb_result_path = r'F:\PythonProjects\MouseEvent\thumb_result_10.jpg'
        thumb_result = ImageGrab.grab()
        thumb_result.save(thumb_result_path, 'jpeg')
        tr_img = cv2.imread('thumb_result_10.jpg', 0)
        # 模板匹配
        tm_thumb_up_result_max_10 = cv2.imread('TM_RESULT_MAX_10.jpg', 0)
        thumb_result_res = cv2.matchTemplate(tr_img, tm_thumb_up_result_max_10, method)
        tr_min_val, tr_max_val, tr_min_loc, tr_max_loc = cv2.minMaxLoc(thumb_result_res)
        print('tr_min_val_10 = ', tr_min_val)
        if tr_min_val < 300000:
            print("is max 10")
            # 保存移动过程图片
            right_bottom = (tr_min_loc[0] + 160, tr_min_loc[1] + 30)
            cv2.rectangle(tr_img, tr_min_loc, right_bottom, 200, 2)
            cv2.imwrite('tr_result_10.jpg', tr_img)
            # 防止覆盖过程中过界问题
            # 横向
            if min_loc[0] + w > w0 - w:
                res_x = w0 - w
            else:
                res_x = min_loc[0] + w

            # 纵向
            if min_loc[1] + h > h0 - h:
                res_y = h0 - h
            else:
                res_y = min_loc[1] + h

            for x in range(min_loc[1], res_y):
                for y in range(min_loc[0], res_x):
                    res[x, y] = 100000 * 500

            # 结束点击
            continue

        # 判断thumb_up_max_50
        # thumb up 40
        for i in range(55):
            # point = ms.GetCursorLoc()
            ms.ClickLeftButton()

        # 截屏
        thumb_result_path = r'F:\PythonProjects\MouseEvent\thumb_result_50.jpg'
        thumb_result = ImageGrab.grab()
        thumb_result.save(thumb_result_path, 'jpeg')
        tr_img = cv2.imread('thumb_result_50.jpg', 0)
        # 模板匹配
        tm_thumb_up_result_max_50 = cv2.imread('TM_RESULT_MAX_50.jpg', 0)
        thumb_result_res = cv2.matchTemplate(tr_img, tm_thumb_up_result_max_50, method)
        tr_min_val, tr_max_val, tr_min_loc, tr_max_loc = cv2.minMaxLoc(thumb_result_res)
        print('tr_min_val_50 = ', tr_min_val)
        if tr_min_val < 2000000:

            # 保存移动过程图片
            right_bottom = (tr_min_loc[0] + 160, tr_min_loc[1] + 30)
            cv2.rectangle(tr_img, tr_min_loc, right_bottom, 200, 2)
            cv2.imwrite('tr_result_50.jpg', tr_img)
            # 防止覆盖过程中过界问题
            # 横向
            if min_loc[0] + w > w0 - w:
                res_x = w0 - w
            else:
                res_x = min_loc[0] + w

            # 纵向
            if min_loc[1] + h > h0 - h:
                res_y = h0 - h
            else:
                res_y = min_loc[1] + h

            for x in range(min_loc[1], res_y):
                for y in range(min_loc[0], res_x):
                    res[x, y] = 100000 * 500

            # 结束点击
            continue
        # break
        # print(top_left)

        # 生成匹配后的文件
        # cv2.rectangle(img, top_left, bottom_right, 0, 2)
        # cv2.imwrite(methods[4] + ".jpg", img)

        # print
        # meth
        # plt.subplot(221), plt.imshow(img2, cmap="jet")
        # plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        # plt.subplot(222), plt.imshow(template, cmap="gray")
        # plt.title('template Image'), plt.xticks([]), plt.yticks([])
        # plt.subplot(223), plt.imshow(res, cmap="gray")
        # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        # plt.subplot(224), plt.imshow(img, cmap="gray")
        # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        # plt.show()

end = time.clock()
t = int(1000 * (end - start))
print('run time %dms' % t)
