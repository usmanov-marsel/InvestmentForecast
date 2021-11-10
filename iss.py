import sys
from client import Config
from client import MicexAuth
from client import MicexISSClient
from client import MicexISSDataHandler


class MyData:
    """ контейнер, используемый обработчиком MyDataHandler
    """

    def __init__(self):
        self.history = []

    def print_sec_list(self):
        print("=" * 69)
        print("|%15s|%30s||" % ("SECID", "SECNAME"))
        print("=" * 69)
        for sec in self.history:
            print("|%15s|%50s|" % (sec[0], sec[1]))
        print("=" * 69)


class MyDataHandler(MicexISSDataHandler):
    """ обработчик данных, полученных клиентом
    """

    def do(self, market_data):
        self.data.history = self.data.history + market_data


def main():
    my_config = Config(user='', password='')
    my_auth = MicexAuth(my_config)
    iss = MicexISSClient(my_config, my_auth, MyDataHandler, MyData)
    market = 'shares'
    limit = 50
    iss.get_sec_list(market, limit)
    iss.handler.data.print_sec_list()


if __name__ == '__main__':
    try:
        main()
    except:
        print("Sorry:", sys.exc_info()[0], ":", sys.exc_info()[1])