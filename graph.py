from iss import *
from client import Config
from client import MicexAuth
from client import MicexISSClient
import matplotlib.pyplot as plt
import matplotlib.dates as dates


def main():
    my_config = Config(user='', password='')
    my_auth = MicexAuth(my_config)
    iss = MicexISSClient(my_config, my_auth, MyDataHandler, MyData)
    engine = 'stock'
    market = 'shares'
    secid = 'ABRD'
    iss.get_sec_prices(engine, market, secid)
    history = iss.handler.data.history
    datetimes = []
    prices = []
    for point in history:
        datetimes.append(point[0])
        prices.append(point[1])
    datetimes = dates.date2num(datetimes)
    fig, graph = plt.subplots()
    graph.plot_date(datetimes, prices, ms=0.1, lw=2, ls='-')
    graph.set(xlabel='date', ylabel='close price', title=secid)
    graph.grid()
    plt.show()


if __name__ == '__main__':
    try:
        main()
    except:
        print("Sorry:", sys.exc_info()[0], ":", sys.exc_info()[1])
