# HPS team6 AImodel in raspberry pi

## Introduction

This is a project for the HPS team6.
run the code in the raspberry pi and get the result.
type`pyhton3 src/main.py` in the terminal and get the result.
mind the model path is need to be the same as the json file.

---

# Install required libraries
1. OpenCV
2. tf-lite
## Install OPenCV

```bash
sudo apt-get install libhdf5-dev libhdf5-serial-dev libhdf5-100
sudo apt-get install libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
sudo apt-get install libjasper-dev
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
sudo pip install opencv-contrib-python
```


## Install tf-lite(Rspi)
https://www.tensorflow.org/lite/guide/python

``` bash
python3 -m pip install tflite-runtime
```

---

# How to use code

1. load the model(Run once when the program start)
``` python
# Load the TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(tf_lite_path)
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load the classes in json file
classes = json.load(open("{}.json".format(model_name)))

```
2. Preprocessing(Run everytime before predict)
``` python
image = cv2.resize(frame,(256,256))   
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
test_image = np.expand_dims(image/255, axis=0).astype(np.float32)
```
3. Predict(Run everytime when you want to predict)
``` python
interpreter.invoke()
prediction_scores = interpreter.get_tensor(output_details[0]['index'])
predicted_index = np.argmax(prediction_scores)
# show classes name 
print(classes[predicted_index])    
```
