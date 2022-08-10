from getpass import getuser
import uuid
from dbconnect import conncet

def checkAccount(account):
    db = conncet()
    cursor = db.cursor()
    sql = "SELECT account FROM User WHERE account=%s;"
    cursor.execute(sql,(account))
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
    db = conncet()
    cursor = db.cursor()
    #create user
    sql = "INSERT INTO User (account,height,weight,workload,BMI,TDEE) VALUES (%s,%s,%s,%s,%s,%s);"
    try:
        cursor.execute(sql,(account,height,weight,workload,BMI,TDEE))
        db.commit()
    except:
        db.rollback()
        print('create fail,please check the data')
        return False
    
    #enter user info into machine
    macaddr = uuid.UUID(int = uuid.getnode()).hex[-12:]
    sql = "INSERT INTO MachineList (macaddr,account) VALUES (%s,%s);"
    try:
        cursor.execute(sql,(macaddr,account))
        db.commit()
    except:
        db.rollback()
        print("enter fail")
        return False
    db = conncet()
    return True
         
def updateUser(account,height,weight,workload,BMI,TDEE):
    result = True
    db = conncet()
    cursor = db.cursor()
    sql = "UPDATE User SET height=%s,weight=%s,workload=%s,BMI=%s,TDEE=%s WHERE account=%s;"
    try:
        cursor.execute(sql,(height,weight,workload,BMI,TDEE,account))
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
        row = cursor.fetchone()
        info = (row[1],row[2],row[3],row[4],row[5])
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

if __name__ == "__main__":
    # updateUser('worker',176,66,'mid',18.5,1745)
    print(getUserInfo('worker'))
