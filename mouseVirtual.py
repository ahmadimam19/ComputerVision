import cv2
import numpy as np
import time
import HandTrackingModule as htm # type: ignore
import autopy
import pyautogui, sys
               

wScr , hScr = autopy.screen.size()

######################
wCam, hCam = 640,480
frameR = 100
smoothening = 8
####################

plocX,ploY = 0,0
cloX, cloY=0,0
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
detector =htm.handDetector(maxHands=1)
while True:

    success, img = cap.read()
    img = detector.findHands(img)
    lmList , bbox = detector.findPosition(img)

    if len(lmList)!=0:
        x1,y1 =lmList[8][1:]
        x2,y2 = lmList[12][1:]

        #print(x1,y1,x2,y2)

        fingers = detector.fingersUp()
        #print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                      (255, 0, 255), 2)


        #mouse move
        if fingers[1]==1 and fingers[2]==0:
            x3 =np.interp(x1,(frameR,wCam-frameR),(0,wScr))
            y3 =np.interp(y1,(frameR,hCam-frameR),(0,hScr))
            cloX = cloX + (x3-plocX)/smoothening
            cloY = cloY + (y3-ploY)/smoothening

            autopy.mouse.move(wScr-cloX, cloY)
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            plocX,ploY = cloX,cloY

        #mouse left click
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3]==0:
            length,img ,lineinfo = detector.findDistance(8,12,img)
            print(length)
            if length <45:
                cv2.circle(img, (lineinfo[4], lineinfo[5]),
                           15, (0, 255,0), cv2.FILLED)
                autopy.mouse.click()
                time.sleep(0.4)
                print(fingers)

        #mouse double click
        if fingers[0]==0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3]==1 and fingers[4]==0:
            length, img, lineinfo = detector.findDistance(8, 12, img)
            print(length)
            if length < 45:
                cv2.circle(img, (lineinfo[4], lineinfo[5]),
                           15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()
                autopy.mouse.click()
                time.sleep(0.4)

        #mouse right click
        if fingers[0] == 1 and fingers[1]==0 and fingers[2]==0 and fingers[3]==0 and fingers[4]==1:
            length, img, lineinfo = detector.findDistance(8, 12, img)
            print(length)
            if length < 45:
                cv2.circle(img, (lineinfo[4], lineinfo[5]),
                           15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click(autopy.mouse.Button.RIGHT)
                time.sleep(0.75)

        #scroll down
        if fingers[0] == 0 and fingers[1] == 0 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0:
            length, img, lineinfo = detector.findDistance(8, 12, img)
            print(fingers)
            print(length)
            pyautogui.scroll(-20)

        #scroll up
        if fingers[0] == 1 and fingers[1] == 0 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0:
            length, img, lineinfo = detector.findDistance(8, 12, img)
            print(fingers)
            print(length)
            pyautogui.scroll(20)

    cTime=time.time()
    fps = 1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,
                (255,0,0),3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)