import subprocess as sp
import colorsys
import cv2 as cv
import numpy as np
from cam_mask import show_cam
from win32api import GetSystemMetrics
from PIL import Image

path = "C:/Program Files/AutoHotKey/AutoHotKey.exe"
res = GetSystemMetrics(0), GetSystemMetrics(1)

colour = ""
img = show_cam()


def add_coord(x, y):
    command = "Click, Left, " + str(x+14) + ", " + str(y+185) + "\n"
    return command

def change_colour(c):
    # v = rgb_to_hsv(c)
    command = "Click, Left, 1180, 100 \nsleep 100 \n"
    command += "Click, Left, 470, 350 \n Click, Left, 470, 350\n"
    command += "send, {backspace}\n"
    command += "send, " + str(c) + "\n sleep 100\n"
    command += "send, {Enter}\n"
    return command

def rgb_to_hsv(c):
    c = [j / 255 for j in (c[0], c[1], c[2])]
    h, s, v = colorsys.rgb_to_hsv(c[0], c[1], c[2])
    return v

if img is not None:
    script = open("paint.ahk", "w")
    script.write("SetMouseDelay, -1 \nSend, {Lwin} \nsleep 100\n Send, paint \n sleep 100\n Send, {Enter}\n sleep 1000 \n")
    h, w = img.shape
    img = Image.fromarray(img)
    img = img.load()
    for x in range(w):
        for y in range(h):
            c = img[x, y]
            if c != colour:
                 script.write(change_colour(c))
                 colour = c
            if c != 255:
                script.write(add_coord(x, y))
    script.write("Esc:: ExitApp \n")
    script.close()
    print("uh oh")

    sp.call([path, "paint.ahk"])
