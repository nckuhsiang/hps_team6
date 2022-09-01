import cv2
import numpy as np
import tflite_runtime.interpreter as tflite
# from PIL import Image
# from keras import models
# import os


dir = "model"
model_name = "mobilenetv2"
tf_lite_path = "{}.tflite".format(model_name)

# Load the TFLite model and allocate tensors.
interpreter = tflite.Interpreter(tf_lite_path)
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
classes = ['Apple', 'Banana', 'Grape', 'Guava', 'Tomato', \
           'dumplings', 'french_fries', 'fried_rice', 'pizza', 'steak']


# model = models.load_model()
video = cv2.VideoCapture(0)

while True:
        _, frame = video.read()
        image = cv2.resize(frame,(256,256))        
        cv2.imshow("Prediction", image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        

        #Expand dimensions to match the 4D Tensor shape.
        test_image = np.expand_dims(image/255, axis=0).astype(np.float32)

        # Calling the predict function using tf-lite
        # interpreter.set_tensor(input_details[0]['index'], test_image)
        interpreter.invoke()
        prediction_scores = interpreter.get_tensor(output_details[0]['index'])
        predicted_index = np.argmax(prediction_scores)        
        print(classes[predicted_index])       

        # cv2.imshow("Prediction", frame)
        key=cv2.waitKey(1)
        if key == ord('q'):
                break
video.release()
cv2.destroyAllWindows()