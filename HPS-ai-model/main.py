import cv2
import numpy as np
import tensorflow as tf
# import tflite_runtime.interpreter as tflite


def image_process_to_tensor(img):
    '''
    This function is used to process image to tensor(a.k.a. image preprocessing)
    @img: image
    @return: tensor(processed image)
    '''
    image = cv2.resize(img,(224,224))        
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #Expand dimensions to match the 4D Tensor shape.
    tensor = (np.expand_dims(image, axis=0).astype(np.float32))/255.0
    return tensor

def predict(input_tensor,interpreter,classes_name,threshold=0.55):
    '''
    @input_tensor: input tensor(processed image)
    @interpreter: tf-lite interpreter
    @classes_name: classes name
    @threshold: threshold for prediction if lower than threshold, then predict other
    '''
    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    interpreter.set_tensor(input_details[0]['index'], tensor)
    interpreter.invoke()
    
    # Show predict results
    prediction_scores = interpreter.get_tensor(output_details[0]['index'])
    predicted_index = np.argmax(prediction_scores)
    max_prediction = prediction_scores[0][predicted_index]
    
    if max_prediction > threshold and predicted_index != 8 and predicted_index != 11:
        return max_prediction,classes[predicted_index],np.max(prediction_scores)
    else :
        return -1,classes_name[predicted_index],np.max(prediction_scores)



# setting the camera
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


model_name = "HPS-ai-model/mobilenetv2_0901.tflite"
tf_lite_path = model_name
# Load the TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(tf_lite_path)
# interpreter = tflite.Interpreter(tf_lite_path)
interpreter.allocate_tensors()
# load the classes name
classes = ['Apple', 'Banana', 'Grape', 'Guava', 'Tomato', 'dumplings', \
    'french_fries', 'ice_cream', 'other', 'pizza', 'steak', 'sushi']



while True:
    _, frame = cap.read()
    
    # Show the frame      
    cv2.imshow("Prediction", frame)
    
    # Preporcess the image to tensor
    tensor = image_process_to_tensor(frame)
    index , name , accuracy= predict(tensor,interpreter,classes,threshold=0.6)
    if index != -1:
        print(index , name , accuracy)
    
    key=cv2.waitKey(1)
    if key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()



