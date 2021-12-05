from datetime import datetime, timedelta, date
from iss import *
from client import Config
from client import MicexAuth
from client import MicexISSClient
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from numpy import polyfit, poly1d

currentdate = datetime.now().date()
futuredate = date(currentdate.year + 3, currentdate.month, 1)

def extrapolate(datetimes, prices, power=1):
    fit = polyfit(datetimes, prices, power)
    line = poly1d(fit)
    new_points = dates.drange(currentdate, futuredate, timedelta(days=30))
    return new_points.tolist(), line


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
        datetimes.append(dates.date2num(point[0]))
        prices.append(point[1])
    new_points, line = extrapolate(datetimes, prices, power=2)
    datetimes_ex = datetimes + new_points
    prices_ex = line(datetimes_ex)
    fig, graph = plt.subplots()
    graph.plot_date(datetimes, prices, 'b', ms=0.1, lw=1, ls='-')
    graph.plot_date(datetimes_ex, prices_ex, 'r', ms=0.1, lw=1, ls='-')
    graph.set(xlabel='date', ylabel='close price', title=secid)
    # plt.xlim([735400, 735500])
    graph.grid()
    plt.show()


if __name__ == '__main__':
    try:
        main()
    except:
        print("Sorry:", sys.exc_info()[0], ":", sys.exc_info()[1])
