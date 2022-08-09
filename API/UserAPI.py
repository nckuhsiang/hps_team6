import pymysql
import hashlib

"""
input:
    account(string)
    password(string)
output:
    result(bool):create success or fail
"""
def createUser(account,password):
    result = True
    md5_hash = hashlib.md5()
    md5_hash.update(password.encode())
    password = md5_hash.hexdigest()
    db = pymysql.connect(
    host= '34.80.39.159',
    user='chench',
    database= 'Fiteat')
    cursor = db.cursor()
    sql = "INSERT INTO User (account,password) VALUES ('" + account + "', '"+ password + "');"
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        result = False
        print('create fail,please check the data')
    db.close()
    return result
         
"""
input:
    account(string),height(float),weight(float),workload(string),BMI(float),TDEE(float)
output:
    result(bool):update success or fail
"""
def updateUser(account,height,weight,workload,BMI,TDEE):
    result = True
    db = pymysql.connect(
    host= '34.80.39.159',
    user='chench',
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
    

"""
input:
    account(string):account that you want to delete
output:
    result(bool):delete success or fail
"""
def deleteUser(account):
    result = True
    db = pymysql.connect(
    host= '34.80.39.159',
    user='chench',
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


"""
input:
    account(string)
output:
    info(tuple): (height,weight,workload,BMI,TDEE),if accunt is not exist return None
"""
def searchUser(account):
    db = pymysql.connect(
    host= '34.80.39.159',
    user='chench',
    database= 'Fiteat')
    cursor = db.cursor()
    sql = "SELECT * FROM User WHERE account='" + account + "';"
    info = None
    try:
        cursor.execute(sql)
        row = cursor.fetchone()
        info = (row[2],row[3],row[4],row[5],row[6])
    except:
        db.rollback()
        print('this account is not exist')
    db.close()
    return  info

if __name__ == "__main__":
    print('start')
