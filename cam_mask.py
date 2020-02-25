import cv2 as cv
import numpy as np


def show_cam():
    vs = cv.VideoCapture(0)
    cv.namedWindow("Camera", cv.WINDOW_NORMAL)
    cv.resizeWindow("Camera", 640, 480)
    while True:
        ret, img = vs.read()
        bg = img
        img = cv.flip(img, 1)
        if img is not None:
            roi = detect_face(img)
            cv.imshow("Camera", img if roi is None else roi)
            if roi is not None:
                return roi
        key = cv.waitKey(100)
        if key == 48:  # Press 0 to take a picture
            return posterize(detect_face(img))
        if key == 27:  # Press esc to exit
            print("Program exited")
            break
    vs.release()


def detect_face(img):
    img_gray = cv.cvtColor(img,  cv.COLOR_BGR2GRAY)
    img_gray = cv.equalizeHist(img_gray)
    faces = face_cascade.detectMultiScale(img_gray, 1.1, 15)
    for (x, y, w, h) in faces:
        w_cor = (320 - w) // 2
        h_cor = (230 - h) // 2

        if x - w_cor > 0 and y - h_cor > 0:
            return img_gray[y - h_cor:y + h + h_cor, x - w_cor:x + w + w_cor]
    return None

def mask(img):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    #color threshold may be slightly discriminatory against certain races
    lower = np.array([0, 48, 80])
    upper = np.array([20, 255, 255])
    mask = cv.inRange(hsv, lower, upper)

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (10, 10))
    mask = cv.erode(mask, kernel) #for spooky images, set iterations to 2
    mask = cv.dilate(mask, kernel)
    mask = cv.GaussianBlur(mask, (3, 3), 0)

    img2 = cv.bitwise_and(img, img, mask=mask)
    return img2

def posterize(img):
    img[img >= 100] = 255
    img[img < 100] = 0
    return img

face_cascade = cv.CascadeClassifier("haarcascade_frontalface_alt.xml")