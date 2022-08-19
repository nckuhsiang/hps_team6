import cv2, os
import numpy as np
import FoodAPI
from dbconnect import conncet
from numpy import ndarray
from pyzbar.pyzbar import decode

color = (0, 0, 255)

def get_food_by_barcode(barcode):
    db = conncet()
    cursor = db.cursor()
    sql = "SELECT food_name FROM Barcode WHERE id=%s;"
    cursor.execute(sql,(barcode))
    row = cursor.fetchone()
    if row:
        foods = FoodAPI.get_foods(row[0],1)
        if foods:
            return foods[0]
        else:
            print("this food doesn't exist")
    else:
        print("barcode doesn't exist")
    return None   

def createBarcode(barcode,food_name):
    result = True
    db = conncet()
    cursor = db.cursor()
    sql = "INSERT INTO Barcode VALUES (%s,%s);"
    try:
        cursor.execute(sql,(barcode,food_name))
        db.commit()
    except:
        db.rollback()
        print('create fail,please check the data')
        result = False
    db.close()
    return result

def deleteBarcode(barcode):
    result = True
    db = conncet()
    cursor = db.cursor()
    sql = "DELETE FROM Barcode WHERE id=%s;"
    try:
        cursor.execute(sql,(barcode))
        db.commit()
    except:
        db.rollback()
        result = False
        print('delete fail, please check the data')
    db.close()
    return result

def updateBarcode(barcode,food_name):
    result = True
    db = conncet()
    cursor = db.cursor()
    sql = "UPDATE Barcode SET food_name=%s WHERE id=%s;"
    try:
        cursor.execute(sql,(food_name,barcode))
        db.commit()
    except:
        db.rollback()
        result = False
        print('update fail,please check the data')
    db.close()
    return result

def detectBarcode(frame: ndarray):
    # do some pre-processing to make the bar-code readable.
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dens = np.sum(frame_gray, axis=0)
    frame_gray = cv2.morphologyEx(frame_gray, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (1, 21)))
    for idx, val in enumerate(dens):
        if val < 10800:
            frame_gray[:,idx] = 0
    _, frame_gray = cv2.threshold(frame_gray, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    for barcode in decode(frame_gray):
        barcode_number = barcode.data.decode('utf-8')
        # get food name from mySQL
        food_name = getFoodName(barcode_number)[0]
        # add box and text around the barcode
        rect = barcode.rect
        top_left = (rect[0],rect[1])
        left_bottom = (rect[0]+rect[2],rect[1]+rect[3])
        frame = cv2.rectangle(frame, top_left, left_bottom, color, 5)
        frame = cv2.putText(frame, food_name, (rect[0],rect[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        return frame, food_name
    return frame, None

def getFoodName(barcode):
    db = conncet()
    cursor = db.cursor()
    sql = "SELECT food_name FROM Barcode WHERE barcode LIKE '" + barcode + "%';"
    cursor.execute(sql)
    row = cursor.fetchone()
    if not row:
        return ["Food not exist"]
    return row

if __name__ == '__main__':
    img_file = ((os.path.dirname(os.path.abspath(__file__)))+'/test_img.jpg')
    img = cv2.imread(img_file)
    detectBarcode(img)