import pymysql
import uuid

def checkAccount(account):
    db = pymysql.connect(
    host= '34.80.39.159',
    user='root',
    database= 'Fiteat')
    cursor = db.cursor()
    sql = "SELECT account FROM User WHERE account='" + account + "';"
    cursor.execute(sql)
    row = cursor.fetchone()
    try:
        if row[0]:
            return False
    except:
        return True

def createUser(account,height,weight,workload,BMI,TDEE):
    if not checkAccount(account):
        print("account has already existed!")
        return False
    db = pymysql.connect(
    host= '34.80.39.159',
    user='root',
    database= 'Fiteat')
    cursor = db.cursor()
    #create user
    sql = "INSERT INTO User (account,height,weight,workload,BMI,TDEE) VALUES ('" + \
    account + "'," + str(height) + "," + str(weight) + ",'" + workload + "'," + str(BMI) + "," + str(TDEE) + ");"
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        print('create fail,please check the data')
        return False
    
    #enter user info into machine
    macaddr = uuid.UUID(int = uuid.getnode()).hex[-12:]
    sql = "INSERT INTO Machine_user_info (macaddr,account) VALUES ('" + macaddr + "','" + account + "');"
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        print("enter fail")
        return False
    db.close()
    return True
         
def updateUser(account,height,weight,workload,BMI,TDEE):
    result = True
    db = pymysql.connect(
    host= '34.80.39.159',
    user='root',
    database= 'Fiteat')
    cursor = db.cursor()
    sql = "UPDATE User SET height=" + str(height) + ",weight=" + str(weight) +",workload='"+ workload +"',BMI="+ str(BMI) + ",TDEE="+ str(TDEE) + " WHERE account='" + account + "';"
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        result = False
        print('update fail,please check the data')
    db.close()
    return result
    
def deleteUser(account):
    result = True
    db = pymysql.connect(
    host= '34.80.39.159',
    user='root',
    database= 'Fiteat')
    cursor = db.cursor()
    sql = "DELETE FROM User WHERE account='" + account + "';"
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        result = False
        print('delete fail, please check the data')
    db.close()
    return result

def getUserInfo(account):
    db = pymysql.connect(
    host= '34.80.39.159',
    user='root',
    database= 'Fiteat')
    cursor = db.cursor()
    sql = "SELECT * FROM User WHERE account='" + account + "';"
    print(sql)
    info = None
    try:
        cursor.execute(sql)
        row = cursor.fetchone()
        info = (row[1],row[2],row[3],row[4],row[5])
    except:
        db.rollback()
        print('this account is not exist')
    db.close()
    return info
    
def listUser():
    macaddr = uuid.UUID(int = uuid.getnode()).hex[-12:]
    db = pymysql.connect(
    host= '34.80.39.159',
    user='root',
    database= 'Fiteat')
    cursor = db.cursor()
    sql = "SELECT account FROM Machine_user_info WHERE macaddr='" + macaddr + "';"
    cursor.execute(sql)
    rows = cursor.fetchall()
    users = []
    for row in rows:
        users.append(row[0])
    return users

if __name__ == "__main__":
    print('test')

#不需要密碼所以好像不需要login了
# def login(account,password):
#     db = pymysql.connect(
#     host= '34.80.39.159',
#     user='chench',
#     database= 'Fiteat')
#     cursor = db.cursor()
#     sql = "Select * FROM User WHERE account='" + account + "';"
#     cursor.execute(sql)
#     row = cursor.fetchone()
#     if account == row[0] and password == row[1]:
#         return True
#     else:
#         print("login fail, please check!")
#         return False