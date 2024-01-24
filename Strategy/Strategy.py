import queue
from abc import ABCMeta, abstractmethod


class Strategy:
    __meta_class__ = ABCMeta

    @abstractmethod
    def GetNewData(self, data):
        pass

    @abstractmethod
    def Suggest(self):
        '''
        :return: {'OPT':'None/Buy/Sell', 'Num':int, 'Price':float}
        '''
        pass


class MeanStrategy(Strategy):
    def __init__(self, rate=0.05, buy_num=100, commission=0.03):
        self.mean = queue.Queue()
        self.mean_value = 0
        self.cnt = 0
        self.current_data = -1
        self.rate = rate
        self.buy_num = buy_num
        self.commission = commission

    def GetNewData(self, data):
        price = float(data['close'])
        if (self.cnt < 10):
            self.mean.put(price)
            self.mean_value += price
            self.current_data = price
            self.cnt += 1
        else:
            old = self.mean.get()
            self.mean.put(price)
            self.mean_value -= old
            self.mean_value += price
            self.current_data = price

    def Suggest(self):
        if (self.cnt < 10):
            return {'OPT': 'None', 'Num': 0, 'Price': 0}
        if (self.current_data >= self.mean_value / 10 * (1 + self.rate)):
            return {'OPT': 'Sell', 'Num': self.buy_num, 'Price': self.current_data}
        elif (self.current_data <= self.mean_value / 10 * (1 - self.rate)):
            return {'OPT': 'Buy', 'Num': self.buy_num, 'Price': self.current_data}
        else:
            return {'OPT': 'None', 'Num': 0, 'Price': 0}
