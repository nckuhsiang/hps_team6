import cv2
import numpy as np
import tensorflow as tf
import json


model_name = "inceptionv3_0825"
# tf_lite_path = "{}/{}.tflite".format(dir,model_name)
tf_lite_path = "{}.tflite".format(model_name)

# Load the TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(tf_lite_path)
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# load the classes in json file
classes = json.load(open("{}.json".format(model_name)))
print(classes)


# model = models.load_model()
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


while True:
        _, frame = cap.read()
        image = cv2.resize(frame,(256,256))        
        cv2.imshow("Prediction", image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        

        #Expand dimensions to match the 4D Tensor shape.
        test_image = np.expand_dims(image/255, axis=0).astype(np.float32)

        # Calling the predict function using tf-lite
        interpreter.set_tensor(input_details[0]['index'], test_image)
        # start_time = time.time()
        interpreter.invoke()
        # start_time = time.time()
        prediction_scores = interpreter.get_tensor(output_details[0]['index'])
        predicted_index = np.argmax(prediction_scores)        
        # show classes name 
        print(classes[predicted_index])       

        # cv2.imshow("Prediction", frame)
        key=cv2.waitKey(1)
        if key == ord('q'):
                break
cap.release()
cv2.destroyAllWindows()