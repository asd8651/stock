import twstock
import pymysql

'''db = pymysql.connect("localhost","root","123456","stockPrice" )
cursor = db.cursor()
sql = """INSERT INTO closing(id,name,price)
         VALUES (1,2365,50)"""
try:
 cursor.execute(sql)
 db.commit()
except:
 db.rollback()
'''

sid=input("sid:")
def newPrice():
 stock=twstock.Stock(sid)
 print(stock.price[30])

def newHigh():
 stock=twstock.Stock(sid)
 print(stock.high[30])
newPrice()
newHigh()

