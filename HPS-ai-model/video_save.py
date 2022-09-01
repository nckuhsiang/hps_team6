import numpy as np
import cv2
from datetime import datetime
import os

'''
Run 'python video_save.py' to save video
The video will be saved in the same directory as this file

Caution : 
1. If you useing raspberry pi, you need change `cv2.VideoCapture(1)` to `cv2.VideoCapture(0)`
2. If the video size is too small, the video will not be saved

You can ues `rm *.avi` to delete all video files in directory
'''

# If you want show the video real-time, change the value of "show_video" to True
show_image = False

# get data and time
now = datetime.now().time() # time object
now = now.strftime("%H_%M_%S") # time string

cap = cv2.VideoCapture(1)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_{}.avi'.format(now), fourcc, 20.0, (640,480))

# fourcc = cv2.VideoWriter_fourcc(*'MP4V')
# out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640,480))


while(cap.isOpened()):
    try :
        ret, frame = cap.read()
        if show_image:
            cv2.imshow("out",frame)
            key=cv2.waitKey(1)
            if key == ord('q'):
                    break
        if ret==True:
            frame = cv2.flip(frame,0)
            out.write(frame)
    except KeyboardInterrupt:
        print ("KeyboardInterrupt saving...")
        break
    except:
        break


cap.release()
out.release()
cv2.destroyAllWindows()


file_stats = os.stat('output_{}.avi'.format(now))
# if file size smaller than 1MB, delete it
if file_stats.st_size < 1000000:
    os.remove('output_{}.avi'.format(now))
    print("File size smaller than 1MB, delete it")
