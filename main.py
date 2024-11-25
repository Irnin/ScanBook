import cv2
import tkinter as tk
from tkinter import simpledialog

cam = cv2.VideoCapture(0)

cv2.namedWindow("ScanBook")
img_counter = 0

name ="dupa"

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break

    # Dodawanie danych do obrazku
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (50, 50)
    fontScale = 1
    color = (255, 0, 0)
    thickness = 2

    image = cv2.putText(frame, name, org, font, fontScale, color, thickness, cv2.LINE_AA)

    cv2.imshow("ScanBook", frame)

    # Czytanie klawiatury
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

    elif k%256 == 13:
        # TO DO
        # Zmiana nazwy na wcisniecie enter
        print("enter pressed")


cam.release()
cv2.destroyAllWindows()