import uuid
from dbconnect import conncet
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

def createUser(user):
    if not checkAccount(user[0]):
        print("account has already existed!")
        return False
    db = conncet()
    cursor = db.cursor()
    #create user
    sql = "INSERT INTO User VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    try:
        cursor.execute(sql,user)
        db.commit()
    except:
        db.rollback()
        print('create fail,please check the data')
        return False
    
    #enter user info into machine
    macaddr = uuid.UUID(int = uuid.getnode()).hex[-12:]
    sql = "INSERT INTO MachineList (macaddr,account) VALUES (%s,%s);"
    try:
        cursor.execute(sql,(macaddr,user[0]))
        db.commit()
    except:
        db.rollback()
        print("enter fail")
        return False
    db.close()
    return True

def updateUser(user):
    result = True
    db = conncet()
    cursor = db.cursor()
    sql = "UPDATE User SET height=%s,weight=%s,workload=%s,gender=%s,calories=%s,fat=%s,carbs=%s,protein=%s WHERE account=%s;"
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
    
def listUser():
    macaddr = uuid.UUID(int = uuid.getnode()).hex[-12:]
    db = conncet()
    cursor = db.cursor()
    sql = "SELECT account FROM MachineList WHERE macaddr= %s;"
    cursor.execute(sql,(macaddr))
    rows = cursor.fetchall()
    users = []
    for row in rows:
        users.append(row[0])
    return users

# def today():
#     return datetime.datetime.now().strftime(r"%Y-%m-%d")
