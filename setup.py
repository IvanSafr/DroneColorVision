from djitellopy import Tello
import cv2
import time
import numpy as np
me = Tello()

me.connect()
me.forward_back_velocity = 0
me.left_right_velocity = 0
me.up_down_velocity = 0
me.yaw_velocity = 0
me.speed = 0

print(f"Заряд батареи: {me.get_battery()}")

me.streamon()
time.sleep(5)

#######################################################
# Настройки
#######################################################
width = 1024
height = 720
########################################################
#
# # Установить настройки цветового поиска тут:
# hsv_min = (0, 71, 175)
# hsv_max = (14, 255, 255)
#######################################################

def nothing(x):
    pass
time.sleep(5)
cv2.namedWindow("settings")  # создаем окно настроек
cv2.namedWindow("res")  # создаем окно настроек

cv2.createTrackbar('h1', 'settings', 0, 255, nothing)
cv2.createTrackbar('s1', 'settings', 0, 255, nothing)
cv2.createTrackbar('v1', 'settings', 0, 255, nothing)
cv2.createTrackbar('h2', 'settings', 255, 255, nothing)
cv2.createTrackbar('s2', 'settings', 255, 255, nothing)
cv2.createTrackbar('v2', 'settings', 255, 255, nothing)
DroneImg = me.get_frame_read()
time.sleep(3)
print("start")
while True:
    frame = DroneImg.frame
    img = cv2.resize(frame, (width, height))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # считываем значения бегунков
    h1 = cv2.getTrackbarPos('h1', 'settings')
    s1 = cv2.getTrackbarPos('s1', 'settings')
    v1 = cv2.getTrackbarPos('v1', 'settings')
    h2 = cv2.getTrackbarPos('h2', 'settings')
    s2 = cv2.getTrackbarPos('s2', 'settings')
    v2 = cv2.getTrackbarPos('v2', 'settings')

        # формируем начальный и конечный цвет фильтра
    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8)

    # h_min = (17, 212, 76)
    # h_max = (255, 255, 255)
    kernel = np.zeros(img.shape[:2], np.uint8)

    img = cv2.bilateralFilter(img, 9, 75, 75)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # накладываем фильтр на кадр в модели HSV
    thresh = cv2.inRange(hsv, h_min, h_max)

    res = cv2.bitwise_and(img, img, mask=thresh)

    cl_s = cv2.dilate(img, kernel, iterations=7)
    edge = cv2.Canny(cl_s, 120, 180)

    contours, h = cv2.findContours(edge, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    k = cv2.waitKey(1) & 0xFF
    if k == ord("q"):
        print(h_min, h_max)
        break

    cv2.imshow('res', res)

cv2.destroyAllWindows()
