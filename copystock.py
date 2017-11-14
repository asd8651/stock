from bs4 import BeautifulSoup
import requests
import json
import csv
import time, datetime, os

#SINCE 2004/10/15 to this year
start_date = datetime.datetime( 2004, 10, 15)
end_date = datetime.datetime.now()
start_date = update()               #update
totaldays = (end_date - start_date).days + 1

for day_list in range(totaldays):
    date_str = (start_date + datetime.timedelta(days = day_list)).date()
    year = date_str.year
    month = date_str.month
    day = date_str.day
    #print(date_str.strftime("%Y%m%d"))
    directory = 'D:/stock/Raw_data/TWSE_5MIN/'
    filename = date_str.strftime("%Y%m%d")+'.csv'
    makedirs()                                         #create directory
function
    json_data = get_webmsg( year, month, day)                #put the data
into smt
    if (json_data != False):
        write_csv( directory, filename, json_data)              #write csv
function
        time.sleep(1)
    else:
        continue

def get_webmsg( year, month, day):
    date = str(year) + "{0:0=2d}".format(month) + "{0:0=2d}".format(day)
    url_twse =
'http://www.twse.com.tw/exchangeReport/MI_5MINS?response=json&date='+ date
    res = requests.post( url_twse)
    soup = BeautifulSoup( res.text, 'html.parser')
    smt = json.loads( soup.text)
    s1 = {'stat': '很抱歉，沒有符合條件的資料!'}
    if(smt != s1):
        return smt
    else:
        return False

def write_csv( directory, filename, json_data):
    writefile = directory + filename
    outputFile = open( writefile,'w', newline='')
    outputWriter = csv.writer( outputFile)
    head = ''.join( json_data['title']).split()
    a = [ head, ""]
    outputWriter.writerow(a)
    outputWriter.writerow( json_data['fields'])
    for data in (json_data['data']):
        outputWriter.writerow(data)
    outputFile.close()

def makedirs():
    directory = 'D:/stock/Raw_data/TWSE_5MIN'
    if not os.path.isdir(directory):
        os.makedirs(directory)

def update():
    path = 'D:\stock\Raw_data\TWSE_5MIN'
    files_list = os.listdir(path)
    date_str = files_list[-1]
    y = int(date_str[:4])
    m = int(date_str[5:6])
    d = int(date_str[6:8]) + 1
    update_date = datetime.datetime( y, m, d)
    return update_date
