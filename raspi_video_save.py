import numpy as np
import cv2
from datetime import datetime


cap = cv2.VideoCapture(1)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
# get data and time 
now = datetime.now().time() # time object
now = now.strftime("%H_%M_%S") # time string
out = cv2.VideoWriter('output_{}.avi'.format(now), fourcc, 20.0, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.flip(frame,0)
        out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()

out.release()

cv2.destroyAllWindows()
