from dbconnect import conncet
import socket
import json

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
    # HOST = "127.0.0.1"
    HOST = "34.81.42.246"
    PORT = 8001
    data = {"name":name,"num":num}
    data = json.dumps(data)
    try:
    # Connect to server and send data
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        client.send(data.encode())
        foods = []
        size = int(client.recv(1024).decode())
        print(size)
        received = b""
        while len(received) < size:
            received += client.recv(1024)
        received = json.loads(received)
        if received["message"] == "success":
            for food in received["foods"]:
                food = Food(food[0],food[1],food[2],food[3],food[4],food[5],food[6])
                foods.append(food)
    finally:
        client.close()
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





# if __name__ == "__main__":
#     foods = get_foods("beef",50)
#     if foods:
#         for food in foods:
#             print(food.name,food.per,food.calories,food.fat,food.carbs,food.protein,food.url)
#     else:
#         print("no data")
   