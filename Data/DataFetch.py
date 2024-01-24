import requests
import pandas as pd

class StockData():
    def __init__(self, location, stock_no):
        self.stockdata = None
        self.location = location
        self.stock_no = stock_no

    def get_stock_today1minData(self):
        url = 'https://web.ifzq.gtimg.cn/appstock/app/minute/query?code={}{}'.format(self.location, self.stock_no)
        page = requests.get(url)
        stock_info = eval(page.text)
        success = stock_info['code'] == 0
        if (success):
            stock_list = stock_info['data']['{}{}'.format(self.location, self.stock_no)]['data']['data']
            stock_time = stock_info['data']['{}{}'.format(self.location, self.stock_no)]['data']['date']
            # print(stock_time)
            # input('-----------')
            # time = Time()
            # time.Year = int(stock_time[:4])
            # time.Month = int(stock_time[4:6])
            # time.Day = int(stock_time[6:8])
            # date =
            df = pd.DataFrame([data.split(' ')[:2] for data in stock_list])
            df.columns = ['time', 'close']
            for i in range(len(df['time'])):
                df['time'][i] = stock_time + df['time'][i]
            # print(df)
            # print(df['time'].size)
            # input('---------------')
            df['close'].astype(float)
            self.stockdata = df
            return success, df
        else:
            return success, None

    def get_stock_history1minData(self, location, stock_no, day_before):
        # 800 pieces of data from Tencent at most
        data_count = day_before * 241
        if(data_count>800):
            data_count = 800
        url = 'https://ifzq.gtimg.cn/appstock/app/kline/mkline?param={}{},m1,,{}'.format(location, stock_no, data_count)
        page = requests.get(url)
        stock_info = eval(page.text)
        success = stock_info['code'] == 0
        if (success):
            stock_list = stock_info['data']['{}{}'.format(location, stock_no)]['m1']
            df_list = []
            for data in stock_list:
                df_list.append([data[0], data[2]])
            df = pd.DataFrame(df_list)
            df.columns = ['time', 'close']
            df['close'].astype(float)
            return success, df
        else:
            return success, None


    def get_stock_currentData(self, location, stock_no):
        if(location==None):
            location = self.location
        if(stock_no==None):
            stock_no = self.stock_no
        url = 'https://qt.gtimg.cn/q={}{}'.format(location, stock_no)
        page = requests.get(url)
        stock_info = page.text
        success = 'v_pv_none_match="1"' not in stock_info
        if success:
            stock_info = stock_info.split('~')
            open = float(stock_info[5])
            high = float(stock_info[33])
            low = float(stock_info[34])
            close = float(stock_info[3])
            date_time = stock_info[30]
            df = pd.DataFrame({'time': [date_time], 'close': ['%.2f' % close]})
            return success, df
        else:
            return success, None

    def add_stock_data(self, df, new_data):
        return pd.concat([df, new_data], axis=0, ignore_index=True)

    def Get_Stock(self):
        return self.location+self.stock_no