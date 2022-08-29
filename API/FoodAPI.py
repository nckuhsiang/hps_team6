from turtle import update
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

def get_daily_diet(account, machine_id):
    db = conncet()
    cursor = db.cursor()
    sql = "SELECT calories,fat,carbs,protein FROM Daily WHERE account=%s and machine_id= %s;"
    cursor.execute(sql,(account, machine_id))
    row = cursor.fetchone()
    if row:
        return row
    else:
        return (0, 0, 0, 0)

def save_diet(food: Food, account, machine_id):
    db = conncet()
    cursor = db.cursor()
    sql = "SELECT calories,fat,carbs,protein FROM Daily WHERE account=%s and machine_id= %s;"
    cursor.execute(sql,(account, machine_id))
    row = cursor.fetchone()
    calories, fat, carbs, protein = food.calories, food.fat, food.carbs, food.protein

    if row: #if data is already in daily
        sql = "UPDATE Daily SET calories=%s,fat=%s,carbs=%s,protein=%s WHERE account=%s and machine_id=%s;"
        calories, fat, carbs, protein = row[0]+food.calories, row[1]+food.fat, row[2]+food.carbs, row[3]+food.protein
        try:
            print(calories,fat,carbs,protein,account,machine_id)
            cursor.execute(sql,(calories, fat, carbs, protein, account, machine_id))
            db.commit()
        except:
            print('Update fail')
            db.rollback()
            return (0, 0, 0, 0)
    
    else: #data is not in daily
        sql = "INSERT INTO Daily (account,machine_id,calories,fat,carbs,protein) VALUES (%s,%s,%s,%s,%s,%s);"
        try:
            cursor.execute(sql,(account, machine_id, calories, fat, carbs, protein))
            db.commit()
        except:
            print('Insert fail')
            db.rollback()
            return (0, 0, 0, 0)
    db.close()
    return (calories, fat, carbs, protein)
    

if __name__ == "__main__":
    # foods = get_foods("cola",50)
    # if foods:
    #     for food in foods:
    #         print(food.name,food.per,food.calories,food.fat,food.carbs,food.protein,food.url)
    # else:
    #     print("no data")
    food = get_foods("apple",1)[0]
    print(save_diet(food,"chench1",'fsdaasdfas'))
