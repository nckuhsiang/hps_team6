import cv2
import numpy as np
import glob
import tensorflow as tf
# from PIL import Image
# from keras import models
# import os


dir = "model"
model_name = "inceptionv3_0825"
saved_model_dir = "{}/{}/".format(dir,model_name)

model = tf.keras.models.load_model(saved_model_dir)

classes = ['Apple', 'Banana', 'Grape', 'Guava', 'Tomato', \
           'dumplings', 'french_fries', 'fried_rice', 'pizza', 'steak']



# model = models.load_model()
cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


while True:
        _, frame = cap.read()
        image = cv2.resize(frame,(256,256))        
        cv2.imshow("Prediction", image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        

        #Expand dimensions to match the 4D Tensor shape.
        test_image = np.expand_dims(image/255, axis=0).astype(np.float32)

        #Calling the predict function using keras
        prediction_scores = model.predict(test_image)
        predicted_index = np.argmax(prediction_scores)
        
        print(classes[predicted_index])       

        # cv2.imshow("Prediction", frame)
        key=cv2.waitKey(1)
        if key == ord('q'):
                break
cap.release()
cv2.destroyAllWindows()