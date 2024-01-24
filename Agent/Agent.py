import time

import pandas as pd
import time as pytime
import sys

sys.path.append("..")
from Data import Time


class Agent:
    def __init__(self, client, stockData, strategy):
        self.client = client
        self.stockData = stockData
        self.strategy = strategy
        self.init_Money = 200000
        self.Money = 200000
        self.stock = {}
        self.use_time = ''
        self.current_price = -1
        self.buy_cnt = 0
        self.sell_cnt = 0
        self.commission = strategy.commission
        self.transfer_fee = 0.00002
        self.tax = 0.001
        self.last_opt_time = ''

        self.init_Money = self.client.Check_Hold(total_money=True)


    def If_Market_Open(self):
        current_time = Time.Get_BeiJing_Time()
        hour, minute = Time.Split_Time(current_time, Hour=True, Minute=True)
        if(hour>=15 or (hour==14 and minute==59)):
            return False
        return True

    def If_New_Data(self, data):
        last_hour, last_minute = Time.Split_Time(self.last_opt_time, Hour=True, Minute=True)
        new_hour, new_minute = Time.Split_Time(data['time'], Hour=True, Minute=True)
        if(new_hour>last_hour):
            return True
        elif(new_hour==last_hour and new_minute > last_minute):
            return True
        else:
            return False

    def Refresh_Status(self):
        self.Money, self.stock = self.client.Check_Hold(available_money=True, stock_hold_available=True)


    def run(self):
        self.last_opt_time = Time.Get_BeiJing_Time(get_second=True)
        self.use_time = self.last_opt_time + ' - '
        while(self.If_Market_Open()):
            self.Refresh_Status()
            code, current_stock = self.stockData.get_stock_currentData(self.stockData.location, self.stockData.stock_no)
            if(not self.If_New_Data(current_stock)):
                time.sleep(20)
                continue
            self.current_price = current_stock['close']
            if (code):
                self.strategy.GetNewData(current_stock)
                suggest = self.strategy.Suggest()
                if (suggest['OPT'] != 'None'):
                    stock_code = self.stockData.Get_Stock()
                    if (suggest['OPT'] == 'Buy'):
                        com_fee = suggest['Num'] * suggest['Price'] * self.commission
                        if(com_fee < 5):
                            com_fee = 5
                        ex_fee = suggest['Num'] * suggest['Price'] * self.transfer_fee
                        if (self.Money < suggest['Num'] * suggest['Price'] + com_fee + ex_fee):
                            continue
                        else:
                            self.buy_cnt += 1
                            # if (stock_code in self.stock.keys()):
                            #     self.stock[stock_code] += suggest['Num']
                            # else:
                            #     self.stock[stock_code] = suggest['Num']
                            self.client.Buy(stock_code, str(suggest['Num']), str(suggest['Price']))
                            self.Money -= suggest['Num'] * suggest['Price'] + com_fee + ex_fee

                    if (suggest['OPT'] == 'Sell'):
                        if (stock_code in self.stock.keys()):
                            self.sell_cnt += 1
                            if (self.stock[stock_code] < suggest['Num']):
                                com_fee = self.stock[stock_code] * suggest['Price'] * self.commission
                                if (com_fee < 5):
                                    com_fee = 5
                                ex_fee = self.stock[stock_code] * suggest['Price'] * (self.transfer_fee + self.tax)
                                self.client.Sell(stock_code, str(self.stock[stock_code]), str(suggest['Price']))
                                self.Money += self.stock[stock_code] * suggest['Price'] - com_fee - ex_fee

                            else:
                                com_fee = suggest['Num'] * suggest['Price'] * self.commission
                                if (com_fee < 5):
                                    com_fee = 5
                                ex_fee = suggest['Num'] * suggest['Price'] * (self.transfer_fee + self.tax)
                                # self.stock[stock_code] -= suggest['Num']
                                self.client.Sell(stock_code, str(suggest['Num']), str(suggest['Price']))
                                self.Money += suggest['Num'] * suggest['Price'] - com_fee - ex_fee
                            # if (self.stock[stock_code] == 0):
                            #     del self.stock[stock_code]
        self.use_time += Time.Get_BeiJing_Time(get_second=True)

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
