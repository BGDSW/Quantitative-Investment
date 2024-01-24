import os
import time
from abc import ABCMeta, abstractmethod
import cv2
import numpy as np
import pytesseract

class Client:
    __meta_class__ = ABCMeta

    @abstractmethod
    def SetMoney(self):
        pass

    @abstractmethod
    def Buy(self):
        pass

    @abstractmethod
    def Sell(self):
        pass

    @abstractmethod
    def Operate(self, cmd):
        pass


class BackTestClient(Client):
    def __init__(self):
        '''
        stock: stock that have been bought {'Stock_num':amount}
        money: how much money do we left
        '''
        self.stock = {}
        self.money = 0

    def Buy(self, stock_num:str, amount:str, price:str=None):
        self.stock[stock_num] += amount
        if(price is None):
            raise Exception
        self.money -= amount * price

    def Sell(self, stock_num:str, amount:str, price:str=None):
        self.stock[stock_num] -= amount
        if (price is None):
            raise Exception
        self.money += amount * price

    def Operate(self, cmd):
        if(cmd['opt']=='BUY'):
            self.Buy(stock_num=cmd['STOCK_NUM'], amount=cmd['AMOUNT'], price=cmd['PRICE'])
        if (cmd['opt'] == 'SELL'):
            self.Sell(stock_num=cmd['STOCK_NUM'], amount=cmd['AMOUNT'], price=cmd['PRICE'])




class MUMUClient(Client):
    def __init__(self):
        os.chdir('D:\\code_for_python\\Quantitative_Investment_PE\\adb\\platform-tools\\')
        self._Commands = {'START_CONNECTION': 'adb connect 127.0.0.1:16384',
                          'KILL_CONNECTION': 'adb kill-server',
                          'CLICK': 'adb shell input tap {} {}',
                          'INPUT_KEY': 'adb shell input keyevent {}'}

        self._Key_Code = {'0': 7,
                          '1': 8,
                          '2': 9,
                          '3': 10,
                          '4': 11,
                          '5': 12,
                          '6': 13,
                          '7': 14,
                          '8': 15,
                          '9': 16,

                          'CAPS_LOCK': 115,
                          'a': 29,
                          'b': 30,
                          'c': 31,
                          'd': 32,
                          'e': 33,
                          'f': 34,
                          'g': 35,
                          'h': 36,
                          'i': 37,
                          'j': 38,
                          'k': 39,
                          'l': 40,
                          'm': 41,
                          'n': 42,
                          'o': 43,
                          'p': 44,
                          'q': 45,
                          'r': 46,
                          's': 47,
                          't': 48,
                          'u': 49,
                          'v': 50,
                          'w': 51,
                          'x': 52,
                          'y': 53,
                          'z': 54,

                          'BACK': 4,
                          'ENTER': 66,
                          'DPAD_CENTER': 23,

                          '.': 56
                          }

        '''
        BUY:指模拟炒股界面，买入圆圈所在位置
        BUY_STOCK_NUM:指点击买入圆圈后， 股票代码/简拼 输入栏所在位置
        BUY_PRICE:指点击买入圆圈后， 价格 输入栏所在位置
        BUY_AMOUNT:指点击买入圆圈后， 数量 输入栏所在位置
        BUY_INPUT_CONFIRM:指点击买入圆圈后，点击股票代码/简拼 输入栏，输入后，确认按键在位置
        BUY_INPUT_CLEAR:指点击买入圆圈后，点击 价格 输入栏，清空按键在位置
        BUY_STOCK:指点击买入圆圈后，买入按键在位置
        BUY_CONFIRM:指点击买入圆圈后，点击买入后，确认买入按键位置
        
        SELL:指模拟炒股界面，卖出圆圈所在位置
        SELL_STOCK_NUM:指点击卖出圆圈后， 股票代码/简拼 输入栏所在位置
        SELL_PRICE:指点击卖出圆圈后， 价格 输入栏所在位置
        SELL_AMOUNT:指点击卖出圆圈后， 数量 输入栏所在位置
        SELL_INPUT_CONFIRM:指点击卖出圆圈后，点击股票代码/简拼 输入栏，输入后，确认按键在位置
        SELL_INPUT_CLEAR:指点击卖出圆圈后，点击 价格 输入栏，清空按键在位置
        SELL_STOCK:指点击卖出圆圈后，卖出按键在位置
        SELL_CONFIRM:指点击卖出圆圈后，点击买入后，确认卖出按键位置
        
        HOLD:指模拟炒股界面，持仓圆圈所在位置
        
        000.png:指遇到000弹窗时，确认按键位置
        '''
        self._Coordinates = {'BUY': [105, 701],
                             'BUY_STOCK_NUM': [350, 350],
                             'BUY_PRICE':[357,482],
                             'BUY_AMOUNT':[357,657],
                             'BUY_INPUT_CONFIRM':[934,1841],
                             'BUY_INPUT_CLEAR':[934,1505],
                             'BUY_STOCK':[364,949],
                             'BUY_CONFIRM':[729,1285],

                             'SELL': [420, 701],
                             'SELL_STOCK_NUM': [350, 350],
                             'SELL_PRICE': [357, 482],
                             'SELL_AMOUNT': [357, 657],
                             'SELL_INPUT_CONFIRM': [934, 1841],
                             'SELL_INPUT_CLEAR': [934, 1505],
                             'SELL_STOCK': [364, 949],
                             'SELL_CONFIRM': [729, 1285],

                             'HOLD': [800, 701],

                             '000.png': [1000, 540]
                             }

        self.PopWindows = {}
        self.Init_PopWindows()

        self.Stock_Code = {'上海银行': 'sh601229',
                           '北京银行': 'sh601169',
                           '浦发银行': 'sh600000',
                           '工商银行': 'sh601398',
                           '招商银行': 'sh600036'}

    def Get_Commands(self):
        return self._Commands

    def Connect(self, port=None):
        if (port is None):
            message = os.popen(self._Commands['START_CONNECTION']).read()
            return message

    def Disconnect(self):
        return os.popen(self._Commands['KILL_CONNECTION']).read()

    def Click(self, x, y):
        read = os.popen(self._Commands['CLICK'].format(x, y)).read()
        time.sleep(1)
        return read

    def Input_Key(self, k):
        read = os.popen(self._Commands['INPUT_KEY'].format(self._Key_Code[k])).read()
        time.sleep(0.1)
        return read

    def Input_String(self, s):
        for c in s:
            self.Input_Key(c)

    def Back(self):
        return os.popen(self._Commands['INPUT_KEY'].format(self._Key_Code['BACK'])).read()

    def Enter(self):
        return os.popen(self._Commands['INPUT_KEY'].format(self._Key_Code['ENTER'])).read()

    def Dpad_Center(self):
        return os.popen(self._Commands['INPUT_KEY'].format(self._Key_Code['DPAD_CENTER'])).read()

    def Capture(self):
        file_path = 'D:\\code_for_python\\Quantitative_Investment_PE\\Pictures\\tmp.png'
        os.system('adb shell screencap -p > '+file_path)
        with open(file_path, 'rb') as f:
            data = f.read()
            data = data.replace(b'\r\n', b'\n')
        with open(file_path, 'wb') as f:
            f.write(data)
        return file_path


    def Operate(self, cmd):
        if (cmd['opt'] == 'BUY'):
            self.Buy(stock_num=cmd['STOCK_NUM'], amount=cmd['AMOUNT'], price=cmd['PRICE'])
        if (cmd['opt'] == 'SELL'):
            self.Sell(stock_num=cmd['STOCK_NUM'], amount=cmd['AMOUNT'], price=cmd['PRICE'])

    def Buy(self, stock_num:str, amount:str, price:str=None):
        self.Click(self._Coordinates['BUY'][0], self._Coordinates['BUY'][1])
        self.Click(self._Coordinates['BUY_STOCK_NUM'][0], self._Coordinates['BUY_STOCK_NUM'][1])
        self.Input_String(stock_num)
        self.Click(self._Coordinates['BUY_INPUT_CONFIRM'][0], self._Coordinates['BUY_INPUT_CONFIRM'][1])
        if(price is not None):
            self.Click(self._Coordinates['BUY_PRICE'][0], self._Coordinates['BUY_PRICE'][1])
            self.Click(self._Coordinates['BUY_INPUT_CLEAR'][0], self._Coordinates['BUY_INPUT_CLEAR'][1])
            self.Input_String(price)
        self.Click(self._Coordinates['BUY_AMOUNT'][0], self._Coordinates['BUY_AMOUNT'][1])
        self.Input_String(amount)
        self.Click(self._Coordinates['BUY_STOCK'][0], self._Coordinates['BUY_STOCK'][1])
        self.Click(self._Coordinates['BUY_CONFIRM'][0], self._Coordinates['BUY_CONFIRM'][1])
        time.sleep(2)
        self.Back()
        time.sleep(3)
        self.Back()

    def Check_Hold(self, total_money=False, stock_value=False, available_money=False, retrievable_money=False, stock_hold=False, stock_hold_available=False, stock_cost=False):
        '''
        :return: 总资产， 总市值， 可用， 可取，{股票代码：股票数量}, {股票代码：可用股票数量}，{股票代码：成本}
        '''
        ans = []
        self.Click(self._Coordinates['HOLD'][0], self._Coordinates['HOLD'][1])
        file_path = self.Capture()
        img = cv2.imread(file_path)
        if(total_money):
            img_crop = img[430:500,20:300,0]
            text = pytesseract.image_to_string(img_crop)
            text = text.replace('\n', '').replace(',', '')
            ans.append(float(text))
        if(stock_value):
            img_crop = img[610:680,20:300,0]
            text = pytesseract.image_to_string(img_crop)
            text = text.replace('\n', '').replace(',', '')
            ans.append(float(text))
        if(available_money):
            img_crop = img[610:680,360:640,0]
            text = pytesseract.image_to_string(img_crop)
            text = text.replace('\n', '').replace(',', '')
            ans.append(float(text))
        if(retrievable_money):
            img_crop = img[610:680,680:960,0]
            text = pytesseract.image_to_string(img_crop)
            text = text.replace('\n', '').replace(',', '')
            ans.append(float(text))

        if(stock_hold or stock_hold_available or stock_cost):
            # 第一支股票
            img_crop = img[1060:1130,20:350,0] + img[1060:1130,20:350,2]
            text = pytesseract.image_to_string(img_crop, lang='chi_sim')
            stock_name_1 = text.replace('\n', '').replace(' ', '')
            # 第二支股票
            img_crop = img[1230:1300, 20:350, 0] + img[1230:1300, 20:350, 2]
            text = pytesseract.image_to_string(img_crop, lang='chi_sim')
            stock_name_2 = text.replace('\n', '').replace(' ', '')
            if (stock_hold):
                ans_stock_hold = {}
                img_crop = img[1060:1130, 660:860, 0] + img[1060:1130, 660:860, 2]
                text = pytesseract.image_to_string(img_crop)
                text = text.replace('\n', '').replace(',', '')
                ans_stock_hold[self.Stock_Code[stock_name_1]] = int(text)

                img_crop = img[1230:1300, 660:860, 0] + img[1230:1300, 660:860, 2]
                text = pytesseract.image_to_string(img_crop)
                text = text.replace('\n', '').replace(',', '')
                ans_stock_hold[self.Stock_Code[stock_name_2]] = int(text)

                ans.append(ans_stock_hold)

            if(stock_hold_available):
                ans_stock_hold_available = {}
                img_crop = img[1130:1190, 660:860, 0] + img[1130:1190, 660:860, 2]
                text = pytesseract.image_to_string(img_crop)
                text = text.replace('\n', '').replace(',', '')
                ans_stock_hold_available[self.Stock_Code[stock_name_1]] = int(text)

                img_crop = img[1290:1350, 660:860, 0] + img[1290:1350, 660:860, 2]
                text = pytesseract.image_to_string(img_crop)
                text = text.replace('\n', '').replace(',', '')
                ans_stock_hold_available[self.Stock_Code[stock_name_2]] = int(text)

                ans.append(ans_stock_hold_available)
            if (stock_cost):
                ans_stock_cost = {}
                img_crop = img[1060:1130,920:1070,0] + img[1060:1130,920:1070,2]
                text = pytesseract.image_to_string(img_crop)
                text = text.replace('\n', '').replace(',', '')
                ans_stock_cost[self.Stock_Code[stock_name_1]] = float(text)

                img_crop = img[1230:1300,920:1070,0] + img[1230:1300,920:1070,2]
                text = pytesseract.image_to_string(img_crop)
                text = text.replace('\n', '').replace(',', '')
                ans_stock_cost[self.Stock_Code[stock_name_2]] = float(text)

                ans.append(ans_stock_cost)

        if(len(ans)==1):
            ans = ans[0]

        self.Back()
        return ans

    def Sell(self, stock_num:str, amount:str, price:str=None):
        self.Click(self._Coordinates['SELL'][0], self._Coordinates['SELL'][1])
        self.Click(self._Coordinates['SELL_STOCK_NUM'][0], self._Coordinates['SELL_STOCK_NUM'][1])
        self.Input_String(stock_num)
        self.Click(self._Coordinates['SELL_INPUT_CONFIRM'][0], self._Coordinates['SELL_INPUT_CONFIRM'][1])
        if (price is not None):
            self.Click(self._Coordinates['SELL_PRICE'][0], self._Coordinates['SELL_PRICE'][1])
            self.Click(self._Coordinates['SELL_INPUT_CLEAR'][0], self._Coordinates['SELL_INPUT_CLEAR'][1])
            self.Input_String(price)
        self.Click(self._Coordinates['SELL_AMOUNT'][0], self._Coordinates['SELL_AMOUNT'][1])
        self.Input_String(amount)
        self.Click(self._Coordinates['SELL_STOCK'][0], self._Coordinates['SELL_STOCK'][1])
        self.Click(self._Coordinates['SELL_CONFIRM'][0], self._Coordinates['SELL_CONFIRM'][1])
        time.sleep(2)
        self.Back()
        time.sleep(3)
        self.Back()

    def Init_PopWindows(self):
        img_paths = [
            'D:\\code_for_python\\Quantitative_Investment_PE\\Pictures\\PopWindows\\000.png',
        ]
        for path in img_paths:
            img = cv2.imread(path, 0)
            self.PopWindows[path.split('\\')[-1]] = img

    def Resolve_PopWindows(self):
        '''
        偶尔会出现一些弹窗，用这个函数消除那些弹窗
        '''
        cap_path = self.Capture()
        img = cv2.imread(cap_path)
        img_crop = img[750:1220, 150:900, 0] #如果有新的弹窗不在这个位置，需要改变截图位置，这个是截中间区域
        for k in self.PopWindows.keys():
            if(np.sum(self.PopWindows[k]-img_crop)<352500): #给每个像素留1的误差允许
                self.Click(self._Coordinates[k][0], self._Coordinates[k][1])
                return

