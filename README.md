# stock
### 金融系統開發
#### 資料來源
-   [TWSE臺灣證券交易所](http://www.twse.com.tw/zh/)
-   [本國上市證券國際證券辨識號碼一覽表](http://isin.twse.com.tw/isin/C_public.jsp?strMode=2)
-   [本國上櫃證券國際證券辨識號碼一覽表](http://isin.twse.com.tw/isin/C_public.jsp?strMode=4)
#### Import
```
- requests
- json
- pymysql
- datetime
```
##### Get昨天日期
```
yesterday = datetime.datetime.now().strftime("%Y%m%d")
```
##### 證交所資料爬蟲
```
params = {"date": yesterday,
          "stockNo":"2330"}
#parms為在url末端加上文字，此處範例為抓取2330資料
res = requests.get('http://www.twse.com.tw/exchangeReport/STOCK_DAY',
                     params=params)
```
##### 將JSON資料解成python可用格式
```
allData = json.loads(res.text)
```
