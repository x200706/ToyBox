import requests
from bs4 import BeautifulSoup
import datetime
import lxml
import psycopg2
from enum import Enum
import time


class CommonSetting(Enum):
    OVERSIZEDRANGE = 9999999999
    FLOATVAR = 1
    INTVAR = 2
    STRVAR = 3


conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port="5432")

table_columns = [
    "code",
    "datatime",
    "type",
    "openvalue",
    "highvalue",
    "lowvalue",
    "closevalue",
    "volume",
    "name"
]

response = requests.get('https://isin.twse.com.tw/isin/C_public.jsp?strMode=2')
response.encoding = 'big5'  # 目標網頁的編碼

soup = BeautifulSoup(response.text, features='lxml')
table = soup.find('table', {'class': 'h4'})
rows = table.find_all('tr')[1:]

stocks = []

cursor = conn.cursor()

for row in rows:
    cols = row.find_all('td')
    stock_code = cols[0].text.strip().split()[0]
    try:
        market_type = cols[3].text.strip()
        name = cols[0].text.strip().split()[1]
    except:
        continue
    stocks.append((stock_code, market_type, name))

# 印出所有股票代號和市場別
for code, market_type, name in stocks:
    now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
    time_open = '2018/01/01'
    time_close = '2023/03/01'
    res_stock_data = requests.get(
        'https://www.cnyes.com/twstock/ps_historyprice.aspx?code=' + code + '&ctl00$ContentPlaceHolder1$startText=' + time_open + '&ctl00$ContentPlaceHolder1$endText=' + time_close)
    soup_stock_data = BeautifulSoup(res_stock_data.text)
    try:
        for data_stock in range(1, CommonSetting.OVERSIZEDRANGE.value):
            def getColumnValue(index_num, var_type):
                match var_type:
                    case CommonSetting.STRVAR:
                        column_value = \
                            soup_stock_data.find_all('div', class_='tab')[0].find_all('tr')[data_stock].find_all('td')[
                                index_num].text
                        return column_value
                    case CommonSetting.INTVAR:
                        column_value = \
                            soup_stock_data.find_all('div', class_='tab')[0].find_all('tr')[data_stock].find_all('td')[
                                index_num].text
                        column_value = column_value.replace(',', '')
                        column_value = int(column_value) * 1
                        return column_value
                    case CommonSetting.FLOATVAR:
                        column_value = \
                            soup_stock_data.find_all('div', class_='tab')[0].find_all('tr')[data_stock].find_all('td')[
                                index_num].text
                        column_value = column_value.replace(',', '')
                        column_value = float(column_value) * 1
                        return column_value


            data_time = getColumnValue(0, CommonSetting.STRVAR)
            open_value = getColumnValue(1, CommonSetting.FLOATVAR)
            high_value = getColumnValue(2, CommonSetting.FLOATVAR)
            low_value = getColumnValue(3, CommonSetting.FLOATVAR)
            close_value = getColumnValue(4, CommonSetting.FLOATVAR)
            volume = getColumnValue(7, CommonSetting.INTVAR)

            # 更好的話可以做爬蟲檢查

            print(code, data_time, market_type, open_value, high_value, low_value, close_value, volume, name)
            query = 'INSERT INTO stock (code, datatime, type, openvalue, highvalue, lowvalue, closevalue, volume, name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);'
            cursor.execute(query,
                           (code, data_time, market_type, open_value, high_value, low_value, close_value, volume, name))
            conn.commit()

    except IndexError:
        path = 'errorlog.txt'
        with open(path, 'a') as f:  # 錯誤紀錄會append加在檔案尾端
            f.write(code)
            f.write(str(time.time()))
        pass

cursor.close()
conn.close()
