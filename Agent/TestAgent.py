import pandas as pd


class Test:
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


    def run(self):
        # code, today_stock = self.stockData.get_stock_today1minData()
        code, two_day_stock = self.stockData.get_stock_history1minData(self.stockData.location, self.stockData.stock_no, 2)
        self.use_time = '{} - {}'.format(two_day_stock['time'].get(0),
                                         two_day_stock['time'].get(len(two_day_stock['time']) - 1))
        self.current_price = two_day_stock['close'][len(two_day_stock['close']) - 1]
        if (code):
            for i in range(len(two_day_stock['time'])):
                self.strategy.GetNewData(two_day_stock.loc[i])
                suggest = self.strategy.Suggest()
                if (suggest['OPT'] != 'None'):
                    stock_code = self.stockData.Get_Stock_Code()
                    if (suggest['OPT'] == 'Buy'):
                        com_fee = suggest['Num'] * suggest['Price'] * self.commission
                        if(com_fee < 5):
                            com_fee = 5
                        ex_fee = suggest['Num'] * suggest['Price'] * self.transfer_fee
                        if (self.Money < suggest['Num'] * suggest['Price'] + com_fee + ex_fee):
                            continue
                        else:
                            self.buy_cnt += 1
                            if (stock_code in self.stock.keys()):
                                self.stock[stock_code] += suggest['Num']
                            else:
                                self.stock[stock_code] = suggest['Num']
                            self.Money -= suggest['Num'] * suggest['Price'] + com_fee + ex_fee

                    if (suggest['OPT'] == 'Sell'):
                        if (stock_code in self.stock.keys()):
                            self.sell_cnt += 1
                            if (self.stock[stock_code] < suggest['Num']):
                                com_fee = self.stock[stock_code] * suggest['Price'] * self.commission
                                if (com_fee < 5):
                                    com_fee = 5
                                ex_fee = self.stock[stock_code] * suggest['Price'] * (self.transfer_fee + self.tax)
                                self.Money += self.stock[stock_code] * suggest['Price'] - com_fee - ex_fee
                                del self.stock[stock_code]
                            else:
                                com_fee = suggest['Num'] * suggest['Price'] * self.commission
                                if (com_fee < 5):
                                    com_fee = 5
                                ex_fee = suggest['Num'] * suggest['Price'] * (self.transfer_fee + self.tax)
                                self.stock[stock_code] -= suggest['Num']
                                self.Money += suggest['Num'] * suggest['Price'] - com_fee - ex_fee
                                if (self.stock[stock_code] == 0):
                                    del self.stock[stock_code]

    def Report(self):
        print('use time: {}'.format(self.use_time))
        print('init money: {}'.format(self.init_Money))
        print('current money: {}'.format(self.Money))
        print('income: {}'.format(self.Money - self.init_Money))
        print('yield: {}%'.format((self.Money / self.init_Money - 1) * 100))
        all_money = self.Money
        if (len(self.stock.keys()) > 0):
            all_money += float(self.current_price) * self.stock[list(self.stock.keys())[0]]
            print('holding stock: {}, num: {}, single price: {}, all price: {}'.format(list(self.stock.keys())[0],
                                    self.stock[list(self.stock.keys())[0]],
                                    self.current_price,
                                    float(self.current_price) * self.stock[list(self.stock.keys())[0]]))

        print('current money(include stock): {}'.format(all_money))
        print('income(include stock): {}'.format(all_money - self.init_Money))
        print('yield(include stock): {}%'.format((all_money / self.init_Money - 1) * 100))
        print('buy operation: {}'.format(self.buy_cnt))
        print('sell operation: {}'.format(self.sell_cnt))
