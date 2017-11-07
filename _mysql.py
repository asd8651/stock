import pymysql
db =pymysql.connect(host='60.249.6.104', port=33060, user='root', passwd='ncutim', db='onmarket' , charset='utf8')
cursor = db.cursor()
sql='''select count(*) from `2330`'''
a = cursor.execute(sql)
if (a):
    print 'existed'