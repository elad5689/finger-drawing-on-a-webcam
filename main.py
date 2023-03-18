import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
xStart = 0
yStart = 0
xEnd = 0
yEnd = 0
imgCanvas = np.zeros((480, 640, 3), np.uint8)
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8 , maxHands=1)

while True:
    #reading img from webcame, and detector check hand
    _, frame = cap.read()
    frame = cv2.flip(frame,1)
    frame_copy = frame.copy()
    hand, img = detector.findHands(frame, flipType=False)
    if hand:
        hand = hand[0]
        finger = detector.fingersUp(hand)
        lmlist = hand["lmList"]
        #get location finger
        x, y = lmlist[8][0], lmlist[8][1]
        #drawing mode
        if finger != [0, 0, 0, 0, 0] and finger != [0, 1, 1, 1, 1]:
            if xStart == 0 and yStart == 0:
                xStart = x
                yStart = y
                xEnd = x
                yEnd = y
                cv2.line(imgCanvas, (xStart, yStart), (xEnd, yEnd), [255, 20, 20], 5)
            else:
                xStart = xEnd
                yStart = yEnd
                xEnd = x
                yEnd = y
                cv2.line(imgCanvas, (xStart, yStart), (xEnd, yEnd), [255, 20, 20], 5)

        # stop mode
        if finger == [0, 1, 1, 1, 1]:
            xStart=0
            yStart=0

        # delete draw
        if finger == [1, 0, 0, 0, 0]:
            xStart == 0
            yStart == 0
            imgCanvas = np.zeros((480, 640, 3), np.uint8)

    # merge webcame and canvas and display
    img = cv2.bitwise_or(frame_copy, imgCanvas)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
