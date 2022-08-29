import cv2
import numpy as np

# https://docs.opencv.org/4.x/d1/d8f/tf_cls_tutorial_dnn_conversion.html

# # read frozen graph with OpenCV API
# opencv_net = cv2.dnn.readNetFromTensorflow("../model/inceptionv3_test/saved_model.pb",)
# print("OpenCV model was successfully read. Model layers: \n", opencv_net.getLayerNames())


# img = cv2.imread('img.jpg')
# rows, cols, channels = img.shape
# opencv_net.setInput(cv2.dnn.blobFromImage(img, size=(256,256), swapRB=True, crop=False))

# # Runs a forward pass to compute the net output
# networkOutput = opencv_net.forward()


IMAGE_SIZE = (256,256)

full_model_path = 'inceptionv3_test.onnx'

# https://docs.opencv.org/3.4/d6/d0f/group__dnn.html
opencv_net = cv2.dnn.readNetFromONNX("model.onnx")
# opencv_net = cv2.dnn.readNetFromONNX('squeezenet1.0-3.onnx')

# img = cv2.imread(image_path)

# img =cv2.resize(cv2.imread(image_path) , IMAGE_SIZE)
# img =cv2.cvtColor(img,cv2.COLOR_BGR2RGB)/255
# print(np.expand_dims(img, axis=0).shape)
# # print(img)
# opencv_net.setInput(np.expand_dims(img, axis=0))
# out = opencv_net.forward()
# print(out)