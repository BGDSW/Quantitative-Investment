from Client.Client import MUMUClient
from Data.DataFetch import StockData
from Strategy.Strategy import MeanStrategy
from Agent.TestAgent import Test
from Agent.Agent import Agent
from Data import Time

'''
上海银行 sh601229
北京银行 sh601169
浦发银行 sh600000
工商银行 sh601398
招商银行 sh600036
'''

def test():
    client = MUMUClient()
    # stockData = StockData('sh', '601229')
    # stockData = StockData('sh', '601169')
    stockData = StockData('sh', '601398')
    # stockData = StockData('sh', '600036')
    strategy = MeanStrategy(rate=0.004, buy_num=1000,commission=0.0003)
    agent = Test(client, stockData, strategy)
    agent.run()
    agent.Report()


def main():
    client = MUMUClient()
    client.Connect()
    stockData1 = StockData('sh', '601398')
    strategy1 = MeanStrategy(rate=0.004, buy_num=1000,commission=0.0003)
    stockData2 = StockData('sh', '601169')
    strategy2 = MeanStrategy(rate=0.004, buy_num=1000,commission=0.0003)
    agent = Agent(client, [stockData1, stockData2], [strategy1, strategy2])
    agent.run()
    agent.Report()
    client.Disconnect()


if __name__ == '__main__':
    test()

