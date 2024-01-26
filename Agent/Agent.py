import time

import pandas as pd
import time as pytime
import sys

sys.path.append("..")
from Data import Time


class Agent:
    def __init__(self, client, stockData:list, strategy:list):
        self.client = client
        self.init_Money = 200000
        self.Money = 200000
        self.stock = {}
        self.use_time = ''
        self.current_price = {}
        self.buy_cnt = {}
        self.sell_cnt = {}
        self.transfer_fee = 0.00002
        self.tax = 0.001
        self.last_opt_time = {}

        self.stock_tool = {}
        cur_time = Time.Get_BeiJing_Time(get_second=True)
        for i in range(len(stockData)):
            stock_code = stockData[i].Get_Stock_Code()
            self.stock_tool[stock_code] = {'stockData': stockData[i], 'strategy': strategy[i]}
            self.buy_cnt[stock_code] = 0
            self.sell_cnt[stock_code] = 0
            self.last_opt_time[stock_code] = cur_time

        cur_time = Time.Get_BeiJing_Time(beautiful=True)
        self.log_file_path = 'D:\\code_for_python\\Quantitative_Investment_PE\\Log\\{}.txt'.format(cur_time)
        self.init_Money, self.Money, stock_hold, self.stock = self.client.Check_Hold(total_money=True,
                                                                                     available_money=True,
                                                                                     stock_hold=True,
                                                                                     stock_hold_available=True)

        message = '\n==========================Agent Init==========================\n' + \
                  'time:{}\n'.format(cur_time) + \
                  'current_all_money:{}\n'.format(self.init_Money) + \
                  'current_available_money:{}\n'.format(self.Money) + \
                  'holding_stocks:{}'.format(str(stock_hold))

        self.Record_Log(message)

    def If_Market_Open(self):
        current_time = Time.Get_BeiJing_Time()
        hour, minute = Time.Split_Time(current_time, Hour=True, Minute=True)
        if(hour>=15 or (hour==14 and minute==59)):
            return False
        return True

    def If_Market_Sleep(self):
        current_time = Time.Get_BeiJing_Time()
        hour, minute = Time.Split_Time(current_time, Hour=True, Minute=True)
        if(hour == 11 and minute >= 29):
            return True
        if (hour == 12):
            return True
        return False

    def If_New_Data(self, data, stock_code):
        last_hour, last_minute = Time.Split_Time(self.last_opt_time[stock_code], Hour=True, Minute=True)
        new_hour, new_minute = Time.Split_Time(data['time'][0], Hour=True, Minute=True)
        if(new_hour>last_hour):
            return True
        elif(new_hour==last_hour and new_minute > last_minute):
            return True
        else:
            return False

    def Refresh_Status(self):
        self.Money, self.stock = self.client.Check_Hold(available_money=True, stock_hold_available=True)

    def Operation(self, stock_code):
        stockData = self.stock_tool[stock_code]['stockData']
        strategy = self.stock_tool[stock_code]['strategy']
        code, current_stock = stockData.get_stock_currentData(stockData.location, stockData.stock_no)
        if (not self.If_New_Data(current_stock, stock_code)):
            return
        self.current_price[stock_code] = current_stock['close'][0]
        if (code):
            strategy.GetNewData(current_stock)
            suggest = strategy.Suggest()
            if (suggest['OPT'] != 'None'):
                if (suggest['OPT'] == 'Buy'):
                    com_fee = suggest['Num'] * suggest['Price'] * strategy.commission
                    if (com_fee < 5):
                        com_fee = 5
                    ex_fee = suggest['Num'] * suggest['Price'] * self.transfer_fee
                    if (self.Money < suggest['Num'] * suggest['Price'] + com_fee + ex_fee):
                        return
                    else:
                        self.buy_cnt[stock_code] += 1
                        self.client.Buy(stock_code, str(suggest['Num']), str(suggest['Price']))

                if (suggest['OPT'] == 'Sell'):
                    if (stock_code in self.stock.keys()):
                        self.sell_cnt[stock_code] += 1
                        if (self.stock[stock_code] < suggest['Num']):
                            self.client.Sell(stock_code, str(self.stock[stock_code]), str(suggest['Price']))
                        else:
                            self.client.Sell(stock_code, str(suggest['Num']), str(suggest['Price']))
                self.last_opt_time[stock_code] = current_stock['time'][0]

                message = '\n==========================Operation==========================\n' +\
                          'stock_code:{}\n'.format(stock_code)+\
                          'time:{}\n'.format(current_stock['time'][0])+\
                          'operation:{}\n'.format(str(suggest))+\
                          'buy_cnt:{}\n'.format(self.buy_cnt[stock_code])+\
                          'sell_cnt:{}\n'.format(self.sell_cnt[stock_code])
                self.Record_Log(message)

    def run(self):
        self.use_time = Time.Get_BeiJing_Time(get_second=True) + ' - '
        while(self.If_Market_Open()):
            if(not self.If_Market_Sleep()):
                time.sleep(30)
                continue
            for stock_code in self.stock_tool.keys():
                cur_time = Time.Get_BeiJing_Time(beautiful=True, get_second=True)
                all_money, self.Money, stock_hold, self.stock = self.client.Check_Hold(total_money=True,
                                                                                       available_money=True,
                                                                                       stock_hold=True,
                                                                                       stock_hold_available=True)

                message = '\n==========================Record Status==========================\n'+\
                          'time:{}\n'.format(cur_time)+\
                          'current_all_money:{}\n'.format(all_money)+\
                          'current_available_money:{}\n'.format(self.Money)+\
                          'holding_stocks:{}\n'.format(str(stock_hold))
                self.Record_Log(message)
                self.Operation(stock_code)
            time.sleep(10)
        self.use_time += Time.Get_BeiJing_Time(get_second=True)
        all_money, self.Money, stock_hold, self.stock = self.client.Check_Hold(total_money=True,
                                                                               available_money=True,
                                                                               stock_hold=True,
                                                                               stock_hold_available=True)

        message = '\n==========================Summary==========================\n'+\
                  'time:{}\n'.format(self.use_time)+\
                  'current_all_money:{}\n'.format(all_money)+\
                  'income(include stock):{}\n'.format(all_money-self.init_Money)+\
                  'yield(include stock):{}%\n'.format(((all_money-self.init_Money)/self.init_Money-1)*100)+\
                  'current_available_money:{}\n'.format(self.Money)+\
                  'current_stock_value:{}\n'.format(all_money-self.Money)+\
                  'holding_stocks:{}\n'.format(str(stock_hold))

        self.Record_Log(message)

    def Report(self):
        self.Refresh_Status()
        print('use time: {}'.format(self.use_time))
        print('init money: {}'.format(self.init_Money))
        print('current money: {}'.format(self.Money))
        print('income: {}'.format(self.Money - self.init_Money))
        print('yield: {}%'.format((self.Money / self.init_Money - 1) * 100))
        all_money = self.client.Check_Hold(total_money=True)
        if (len(self.stock.keys()) > 0):
            print('holding stock: {}, num: {}, single price: {}, all price: {}'.format(list(self.stock.keys())[0],
                                                                                       self.stock[
                                                                                           list(self.stock.keys())[0]],
                                                                                       self.current_price,
                                                                                       float(self.current_price) *
                                                                                       self.stock[
                                                                                           list(self.stock.keys())[0]]))

        print('current money(include stock): {}'.format(all_money))
        print('income(include stock): {}'.format(all_money - self.init_Money))
        print('yield(include stock): {}%'.format((all_money / self.init_Money - 1) * 100))
        print('buy operation: {}'.format(self.buy_cnt))
        print('sell operation: {}'.format(self.sell_cnt))

    def Record_Log(self, message):
        with open(self.log_file_path, 'a+') as f:
            f.write(message)