import serial
import struct
import time
import cv2
import math
from handDetector import HandDetector

handDetector = HandDetector(min_detection_confidence=0.7)
webcamFeed = cv2.VideoCapture(0)

arduino = serial.Serial('COM14', 115200)
time.sleep(1.5)

while True:
    status, image = webcamFeed.read()
    handLandmarks = handDetector.findHandLandMarks(image=image, draw=True)
    if(len(handLandmarks) != 0):
        x1, y1 = handLandmarks[4][1], handLandmarks[4][2]
        x2, y2 = handLandmarks[8][1], handLandmarks[8][2]
        x3, y3 = handLandmarks[12][1], handLandmarks[12][2]
        x4, y4 = handLandmarks[0][1], handLandmarks[0][2]
        length = int((math.hypot(x2-x1, y2-y1))-10)
        length2 = int((math.hypot(x3-x4, y3-y4)/3))
        
        calX = int((handLandmarks[0][1]-300) / 1.55) 
        if(calX >= (-180) and calX < 0):
            valueX= 90 - (calX / (-2))
        elif(calX == 0):
            valueX = 90
        elif(calX > 0 and calX <= 180):
            valueX = (calX / 2) + 90
        calY = (((handLandmarks[0][2]/2) - 40) / 2) - 5
        if(calY < 0):
            calY = 0
        elif(calY > 180):
            calY = 180
        print(f"lenght : {length}")
        print(f"lenght2 : {length2}")
        print(f"hand point X : {int(valueX)}")
        print(f"hand point Y : {int(calY)}")
        
        if(length < 255 and length >= 0 and length2 < 255 and valueX < 255 and calY < 255):
            #pass
            arduino.write(struct.pack('>BBBB', int(valueX), int(length2), int(calY), int(length)))
        
        cv2.circle(image, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(image, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 3)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    
    cv2.imshow("Control robot", image)
    cv2.waitKey(1)
cv2.destroyAllWindows()