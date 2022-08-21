from dbconnect import conncet
import json
import requests

class Food:
    def __init__(self,name,per,calories,fat,carbs,protein,url):
        self.name = name
        self.per = per #unit:g
        self.calories = calories #unit:kcal
        self.fat = fat #unit:g
        self.carbs = carbs #unit:g
        self.protein = protein #unit:g
        self.url = url

def get_foods(name,num):
    url = "https://asia-east1-goolge-hps-team6.cloudfunctions.net/hps-team6-server"
    data = {
        "name":name,
        "num":num
    }
    tmp = requests.post(url,json=data)
    response = json.loads(tmp.text)
    if response["message"] == "fail":
        return None
    if response["message"] == "success":
        foods = []
        for food in response["foods"]:
            foods.append(Food(food["name"],food["per"],food["calories"],food["fat"],food["carbs"],food["protein"],food["url"]))
    else:
        print(name + "is not exist")
        return []
    return foods

def get_daily_diet(account):
    db = conncet()
    cursor = db.cursor()
    sql = "SELECT account,calories,fat,carbs,protein FROM Daily WHERE account=%s"
    cursor.execute(sql,(account))
    row = cursor.fetchone()
    if row:
        return row
    sql = "SELECT account,calories,fat,carbs,protein FROM User WHERE account=%s"
    cursor.execute(sql,(account))
    row = cursor.fetchone()
    if not row:
        print("account doesn't exist")
        return None
    sql = "INSERT INTO Daily VALUES (%s,%s,%s,%s,%s);"
    try:
        cursor.execute(sql,row)
        db.commit()
    except:
        print('Insert fail')
        db.rollback()
        return None
    db.close()
    return (row[1],row[2],row[3],row[4])

def save_diet(food,account):
    db = conncet()
    cursor = db.cursor()
    sql = "SELECT * FROM Daily WHERE account=%s;"
    cursor.execute(sql,(account))
    row = cursor.fetchone() #(account,calories,fat,carbs,protein)
    if row: #if data is already in daily
        sql = "UPDATE Daily SET calories=%s,fat=%s,carbs=%s,protein=%s WHERE account=%s;"
        try:
            cursor.execute(sql,(row[1]-food[1],row[2]-food[2],row[3]-food[3],row[4]-food[4],row[0]))
            db.commit()
        except:
            print('Update fail')
            db.rollback()
            return False
    else: #data is not in daily
        sql = "SELECT account,calories,fat,carbs,protein FROM User WHERE account=%s;"
        cursor.execute(sql,(account))
        row = cursor.fetchone()
        if row:
            sql = "INSERT INTO Daily VALUES (%s,%s,%s,%s,%s);"
            try:
                cursor.execute(sql,(row[0],row[1]-food[1],row[2]-food[2],row[3]-food[3],row[4]-food[4]))
                db.commit()
            except:
                print('Insert fail')
                db.rollback()
                return False
        else:
            print("account doesn't exist")
            return False
    db.close()
    return True
    

if __name__ == "__main__":
    foods = get_foods("cola",50)
    if foods:
        for food in foods:
            print(food.name,food.per,food.calories,food.fat,food.carbs,food.protein,food.url)
    else:
        print("no data")