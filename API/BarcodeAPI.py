import FoodAPI
from dbconnect import conncet

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