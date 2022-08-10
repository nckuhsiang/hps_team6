import requests
import nums_from_string
from dbconnect import conncet

def get_token():
    url = "https://oauth.fatsecret.com/connect/token"
    client_ID = "ac2f660ad05f41a3b9f18b927e74c71f"
    client_secret = "67eddc79e83c4ea78c9d97d7189fffea"
    options = {
        
        "headers": { 'content-type': 'application/x-www-form-urlencoded'},
        "grant_type": "client_credentials",
        "scope":"basic",
        "json": True
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
    }
    auth = (client_ID,client_secret)
    response = requests.post(url, data=options,headers=headers,auth=auth).json()
    return response["access_token"]

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
    url = "https://platform.fatsecret.com/rest/server.api"
    token = get_token()
    options = {
        "method":"foods.search",
        "format":"json",
        "search_expression":name,
        "max_results": num
    }
    headers = {
        "Authorization":"Bearer "+ token
    }
    response = requests.post(url,data=options, headers=headers).json()
    food_list = []
    try:
        res = response["foods"]
        if "food" in res.keys(): #check for the presence of this food that user search
            if num == 1:
                items = [res["food"]]
            else:
                items = res["food"]
            for item in items:
                description = item["food_description"]
                #remove item that per uint is not g
                tmp = description.split(" - ")
                if(tmp[0][-1] != "g"): continue
                #get food info
                info = nums_from_string.get_nums(description)
                food = Food(item["food_name"],info[0],info[1],info[2],info[3],info[4],item["food_url"])
                food_list.append(food)
        else:
            print(name + "is not exist")
    except:
        print(response["error"]['message'])
        return None
    if(not food_list): #check food_list still have data after filter
        print(name + "is not exist")  
    return food_list
 
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
