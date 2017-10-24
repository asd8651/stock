import pymysql
db =pymysql.connect(host='0.tcp.ngrok.io', port=12714, user='root', passwd='ncutim', db='onmarket')
sql = """CREATE TABLE IF NOT EXISTS `ooo`(
                ID INT AUTO_INCREMENT PRIMARY KEY,
                date  varchar(30) ,
                sid varchar(20),
                name varchar(20),  
                shareTrades	varchar(30),
                turnover varchar(30) ,
                open varchar(30),
                high varchar(30) ,
                low varchar(30) ,
                closing varchar(30))
                ENGINE = InnoDB,
                CHARSET=utf8,
                COLLATE utf8_unicode_ci;"""
cursor = db.cursor()

cursor.execute(sql)
    #pymysql.connect("0.tcp.ngrok.io",12714,"root","ncutim","onmarket",charset="utf8")
