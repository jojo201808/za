import pymysql

#connet database
def connectDb():
    db = pymysql.connect(
        host='101.132.76.217',
        user='root',
        password='root',
        port=3306,
        db='bubble_test')
    return db

#excute mysql
def excuteDB(cursor,sql):
    cursor.excute(sql)

#close database
def closeDb(db):
    db.close()
