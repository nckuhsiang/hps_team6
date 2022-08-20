import pymysql

def conncet():
    db = pymysql.connect(
    host= '35.194.208.208',
    user='root',
    passwd= 'team6isbest',
    database= 'Fiteat')
    return db


if __name__ == '__main__':
    db = conncet()
    print(db)
    