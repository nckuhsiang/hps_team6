import cv2
import numpy as np

# img_path = "/content/drive/MyDrive/hps/barcode_img"

cap = cv2.VideoCapture(0)
# cap.setCaptureProperty(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.setCaptureProperty(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#  Initialize OpnenCV built-in barcode and QR code detector(only run once in the program)
## https://opencv.org/recognizing-one-dimensional-barcode-using-opencv/
bardet = cv2.barcode_BarcodeDetector()

while True:
  
    ret, img = cap.read()
    # img = cv2.resize(frame,(256,256))        
    # cv2.imshow("Prediction", image)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    #  Detect and decode the barcode
    ok, decoded_info, decoded_type, corners = bardet.detectAndDecode(img)
    print(ok, decoded_info, decoded_type, corners)
    if not type(corners) == type(None):
        cv2.polylines(img,np.int32(corners),1,(0,255,255))
    cv2.imshow("out",img)
    
    key=cv2.waitKey(1)
    if key == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()