from sre_constants import SUCCESS
import pymysql

def createUser(account,password):
    db = pymysql.connect(
    host= '34.80.39.159',
    user='chench',
    database= 'Fiteat')
    cursor = db.cursor()
    sql = "INSERT INTO User (account,password) VALUES ('" + account + "', '"+ password + "');"
    try:
        cursor.execute(sql)
        db.commit()
        print("success")
    except:
        db.rollback()
        print('fail')
    db.close()

def listUser(account,password):
    db = pymysql.connect(
    host= '34.80.39.159',
    user='chench',
    database= 'Fiteat')
    cursor = db.cursor()
    sql = 'SELECT * FROM User'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            print(row[0])
    except:
        db.rollback()
        print('fail')
    db.close()

def updateUser(account,height,weight,workload,BMI,TDEE):
    db = pymysql.connect(
    host= '34.80.39.159',
    user='chench',
    database= 'Fiteat')
    cursor = db.cursor()
    sql = "UPDATE User SET height=" + str(height) + ",weight=" + str(weight) +",workload='"+ workload +"',BMI="+ str(BMI) + ",TDEE="+ str(TDEE) + " WHERE account='" + account + "';"
    try:
        cursor.execute(sql)
        db.commit()
        print("success")
    except:
        db.rollback()
        print('fail')
    db.close()

def deleteUser(account):
    db = pymysql.connect(
    host= '34.80.39.159',
    user='chench',
    database= 'Fiteat')
    cursor = db.cursor()
    sql = "DELETE FROM User WHERE account='" + account + "';"
    try:
        cursor.execute(sql)
        db.commit()
        print("success")
    except:
        db.rollback()
        print('fail')
    db.close()


if __name__ == "__main__":
    # updateUser("test00",177,67,'light',19.5,1733)
    deleteUser("test00")

