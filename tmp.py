import os
from Client.Client import MUMUClient
import cv2
import numpy as np
from Data import Time
import pytesseract
from PIL import Image
from Data import DataFetch

if __name__ == '__main__':

    data = DataFetch.StockData('sh', '601398')
    _, d1 = data.get_stock_history1minData()
    _, d2 = data.get_stock_currentData()
    d2 = d2.loc[0]
    print(d1)
    print('-------------')
    print(d2)
    print('--------------')
    print(d2['time'])
    print('--------------')
    print(type(d2['time']))
    print(type(d2['close']))


    # client = MUMUClient()
    # client.Connect()
    # client.Capture()
    # client.Disconnect()
    # a = client.Check_Hold(total_money=True, stock_value=True, available_money=True, retrievable_money=True, stock_hold_available=True, stock_cost=True)
    # print(a)
    # client.Disconnect()
    # print(b)
    # print(c)
    # print(d)
    # client.Connect()
    # client.Click(client._Coordinates['HOLD'][0], client._Coordinates['HOLD'][1])

    # img = cv2.imread('D:\\code_for_python\\Quantitative_Investment_PE\\Pictures\\tmp.png')
    # img_crop = img[1230:1300, 660:860, 0] + img[1230:1300, 660:860, 2]
    # # img_crop = img[1130:1190,660:860,0] + img[1130:1190,660:860,2]
    # # text = pytesseract.image_to_string(img_crop, lang='chi_sim')
    # # print(text.repalce[])
    # # print(np.max(img_crop))
    # cv2.imshow('1', img_crop)
    # cv2.waitKey(0)

    # available_moneye_img = img[610:680,680:960,0]
    # # # stock_value_img = img[610:680,20:300,0]
    # # # cv2.imwrite('D:\\code_for_python\\Quantitative_Investment_PE\\Pictures\\tmp_stock_value.png', stock_value_img)
    # cv2.imshow('1',available_moneye_img)
    # cv2.waitKey(0)
    # # total_money_img = img[430:500,20:300,0]
    # # cv2.imwrite('D:\\code_for_python\\Quantitative_Investment_PE\\Pictures\\tmp_total_money.png', total_money_img)
    #
    # # text = pytesseract.image_to_string(Image.open('D:\\code_for_python\\Quantitative_Investment_PE\\Pictures\\tmp_total_money.png'), lang="eng")
    # #
    # # print(float(text))
    # # print(type(text))




