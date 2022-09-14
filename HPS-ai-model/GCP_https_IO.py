from google.cloud import vision
import requests
import cv2
import base64
import json

# https://cloud.google.com/vision/docs/request
API_KEY = "AIzaSyBkekhbHjgq44FdE4z8POD6wlIZa4QAmqY"


def create_request(image):
    BASE64_ENCODED_IMAGE = base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()
    return  {
    "requests": [
        {
        "image": {
            "content": "{}".format(BASE64_ENCODED_IMAGE)},
        "features": [
            {
                "type": "LABEL_DETECTION",
                "maxResults": 10
            }
        ]
        }
    ]
    }
def http_response_detect_labels(image):
    request_json = create_request(image)
    # https://cloud.google.com/vision/docs/request
    API_KEY = "AIzaSyBkekhbHjgq44FdE4z8POD6wlIZa4QAmqY"
    response = requests.post('https://vision.googleapis.com/v1/images:annotate?key=' + API_KEY, json=request_json)
    # convert response.text to json 
    labels = json.loads(response.text)
    
    # print(response)
    # print(type(labels))
    # print(labels['responses'][0]['labelAnnotations'])
        
    """ index of labelAnnotations
    0:Apple 0
    1:Grape 1
    2:Guava 2
    3:Tomato 3
    4:Fried rice 4 
    5:Pizza 5
    6:Dumpling 6,7
    7:French fries 8,9
    8:Banana 10,11,12
    9:Steak 13,14,15
    """        
    # classes = ['Apple', 'Banana','Saba banana','Banana family','Grape', 'Guava', 'Tomato', \
    #     'Dumpling','Nikuman','Fast food','French fries', 'Fried rice', 'Pizza', 'Steak','Meat','Red meat']
    classes = ['Apple','Grape', 'Guava', 'Tomato','Fried rice', 'Pizza', \
        'Dumpling','Nikuman', 'Fast food','French fries','Banana','Saba banana','Banana family', 'Steak','Meat','Red meat']
    real_classes = ['Apple', 'Graps', 'Guava', 'Tomato','Fried rice', 'Pizza', \
        'Dumpling','French fries','Banana','Steak']
    
    for label in labels['responses'][0]['labelAnnotations']:
        if label['description'] in classes:
            # print(label['description'])
            # print(classes.index(label['description']))
            index = classes.index(label['description'])
            if index < 6:
                return real_classes[index]
            elif index < 10:
                return real_classes[6+((index-6)%2)]
            else:
                return real_classes[8+ ((index-10)%3)]
                


# # image_path = "Grape.png"
# image_path = "FIDS30/grapes/7.jpg"

# image = cv2.imread(image_path)
# image = cv2.resize(image, (224,224))
# # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# print(http_response_detect_labels(image))



def detect_labels(image):
    """Detects labels in the file."""
    # encode np array to base64
    content = base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()
    client = vision.ImageAnnotatorClient()
    
    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')
    # classes = ['Apple', 'Banana', 'Grape', 'Guava', 'Tomato', \
    #        'Dumpling', 'French fries', 'Fried rice', 'Pizza', 'Steak']
    classes = ['Apple', 'Banana','Saba banana','Banana family','Grape', 'Guava', 'Tomato', \
           'Dumpling','Nikuman', 'Fast food','French fries', 'Fried rice', 'Pizza', 'Steak','Meat','Red meat']

    # print(type(labels))
    for label in labels:
        print(label.description)
        for classes_name in classes:
            if label.description == classes_name:
                print("Same:",label.description)
                
        # print(label.description)
        
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


# image_path = "/Users/msyang/shuan-code/HPS-ai-model/image/fried_rice/1108588.jpg"
# image_path = "Grape.png"
# image_path = "FIDS30/grapes/7.jpg"

# image = cv2.imread(image_path)
# image = cv2.resize(image, (224,224))
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# detect_labels(image)
# detect_labels(image_path)


video = cv2.VideoCapture(0)
while True:
        _, frame = video.read()
        # image = cv2.resize(frame,(224,224))
        image = frame 
        cv2.imshow("Prediction", image)
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # detect_labels(image)
        http_response_detect_labels(image)
        # cv2.imshow("Prediction", frame)
        key=cv2.waitKey(1)
        if key == ord('q'):
                break
video.release()
cv2.destroyAllWindows()


