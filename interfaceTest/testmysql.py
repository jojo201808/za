import pymysql

db = pymysql.connect(host='106.14.193.137',user='tester',password='^tJgfeoiKRe_ZWYO',db='bubble',port=6603)
cursor = db.cursor()
sql = 'select * from mp_user_wallet where user_id=237052' 
cursor.execute(sql)
db.close() 