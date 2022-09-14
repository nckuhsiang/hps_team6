import cv2
import numpy as np
from dbconnect import conncet
# new library for http request
import requests
import base64
import json

'''
加入了 `RecognitionAPI_GCP.py`，主要變動如下
- create_request(image):只需要image就可以 要記得把另一邊呼叫也改一下
- 需要新增這幾樣 Library
  ```
  import requests
  import base64
  import json
  ```
- 開機不需要再先載入模型，需要辨識時只需呼叫`get_food_by_recognition`

btw:`HPS-ai-model/GCP_https_IO.py` 是可以在自己電腦的執行的，有問題可先試試看這個
'''
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
    
def get_food_by_recognition(image):
      
    classes_name = http_response_detect_labels(image)
    
    db = conncet()
    cursor = db.cursor()
    sql = "SELECT per,calories,fat,carbs,protein FROM Recognition WHERE food_name=%s;"
    cursor.execute(sql,(classes_name))
    row = cursor.fetchone()
    food = dict()
    if row:
        food["food_name"] = classes_name
        food["per"] = row[0]
        food["calories"] = row[1]
        food["fat"] = row[2]
        food["carbs"] = row[3]
        food["protein"] = row[4]
        return food
    else:
        print("food doesn't exist")
        return None

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
                


# if __name__ == "__main__":
#     img = cv2.imread("pizza.jpeg")
#     model =load_model()
#     print(get_food_by_recognition(img,model))
