from dbconnect import conncet
#import uuid
#import datetime

# class User:
#     def __init__(self,account,height,weight,workload,gender,calories,fat,carbs,protein):
#         self.account = account
#         self.height = height
#         self.weight = weight
#         self.gender = gender
#         self.calories = calories
#         self.fat = fat
#         self.carbs = carbs
#         self.protein = protein

def checkAccount(account):
    db = conncet()
    cursor = db.cursor()
    sql = "SELECT account FROM User WHERE account=%s;"
    cursor.execute(sql,(account))
    row = cursor.fetchone()
    if row:
        return False
    return True

def createUser(user): # user = (account,machine_id,height,weight,workload,gender,calories,fat,carbs,protein)
    if not checkAccount(user[0]):
        print("account has already existed!")
        return False
    result = True
    db = conncet()
    cursor = db.cursor()
    sql = "INSERT INTO User VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    try:
        cursor.execute(sql,user)
        db.commit()
    except:
        db.rollback()
        print('create fail,please check the data')
        result = False
    db.close()
    return result

def updateMachineID(old_id,new_id):
    result = True
    db = conncet()
    cursor = db.cursor()
    sql = "UPDATE User SET machine_id=%s WHERE machine_id=%s;"
    try:
        cursor.execute(sql,(new_id,old_id))
        db.commit()
    except:
        db.rollback()
        result = False
        print('update fail,please check the data')
    db.close()
    return result

def updateUser(user): #user= (height,weight,workload,gender,calories,fat,carbs,protein,account)
    result = True
    db = conncet()
    cursor = db.cursor()
    sql = "UPDATE User SET height=%s,weight=%s,workload=%s,gender=%s, \
        calories=%s,fat=%s,carbs=%s,protein=%s WHERE account=%s;"
    try:
        cursor.execute(sql,user)
        db.commit()
    except:
        db.rollback()
        result = False
        print('update fail,please check the data')
    db.close()
    return result
    
def deleteUser(account):
    result = True
    db = conncet()
    cursor = db.cursor()
    sql = "DELETE FROM User WHERE account=%s;"
    try:
        cursor.execute(sql,(account))
        db.commit()
    except:
        db.rollback()
        result = False
        print('delete fail, please check the data')
    db.close()
    return result

def getUserInfo(account):
    db = conncet()
    cursor = db.cursor()
    sql = "SELECT * FROM User WHERE account='" + account + "';"
    info = None
    try:
        cursor.execute(sql)
        info = cursor.fetchone()
    except:
        db.rollback()
        print('this account is not exist')
    db.close()
    return info
    
def listUser(machine_id):
    db = conncet()
    cursor = db.cursor()
    sql = "SELECT account FROM MachineList WHERE macaddr= %s;"
    cursor.execute(sql,(machine_id))
    rows = cursor.fetchall()
    users = []
    for row in rows:
        users.append(row[0])
    return users

# def today():
#     return datetime.datetime.now().strftime(r"%Y-%m-%d")
