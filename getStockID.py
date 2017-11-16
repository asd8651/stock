import pymysql
#import twstock
db =pymysql.connect(host='60.249.6.104', port=33060, user='root', passwd='ncutim', db='otc' , charset='utf8')
cursor = db.cursor()
cursor.execute("""SELECT stockID FROM `stockID`""")
searchID = cursor.fetchall()
#get execute data(list)
sid=searchID
codeList=[]
for i in range(len(sid)):
    sid = searchID.__str__()
    sid = sid.strip('()')
    sid = sid.replace('(', '')
    sid = sid.replace(')', '')
    sid = sid.replace(',', '')
    sid = sid.split(' ')
    codeList.append(sid[i])
cursor.execute("""SELECT name FROM `stockID`""")
searchName = cursor.fetchall()
#get execute data(list)
_name=searchName
nameList=[]
for i in range(len(_name)):
    _name = searchID.__str__()
    _name = _name.strip('()')
    _name = _name.replace('(', '')
    _name = _name.replace(')', '')
    _name = _name.replace(',', '')
    _name = _name.split(' ')
    nameList.append(_name[i])
