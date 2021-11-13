import http.cookiejar
import json
import urllib.error
import urllib.parse
import urllib.request

requests = {
    'history_secs': 'http://iss.moex.com/iss/history/engines/%(engine)s/markets/%(market)s/boards/%(board)s/securities.json?date=%(date)s',
    'sec_list': 'http://iss.moex.com/iss/securities.json?market=%(market)s'}


class Config:
    def __init__(self, user='', password='', debug_level=0):
        """ контейнер для логинов:
            user: логин на moex.com
            password: пароль
            proxy_url: прокси в формате http://proxy:port
            debug_level: 0 - без вывода, 1 - выводит в консоль инфу о дебаге
        """
        self.debug_level = debug_level
        self.user = user
        self.password = password
        self.auth_url = "https://passport.moex.com/authenticate"


class MicexAuth:
    """ данные и методы аутентификации пользователя
    """

    def __init__(self, config):
        self.config = config
        self.cookie_jar = http.cookiejar.CookieJar()
        self.passport = None


class MicexISSDataHandler:
    """ обработчик скачанных данных
    """

    def __init__(self, container):
        """ контейнер для данных
        """
        self.data = container()

    def do(self, market_data):
        """ тут что-то делаем с данными
        """
        pass


class MicexISSClient:
    """ методы взаимодействий с сервером мосбиржи
    """

    def __init__(self, config, auth, handler, container):
        """ создаем коннект с сервером
            config: экземпляр класса Config
            auth: экземпляр класса MicexAuth
            handler: класс обработчика пользователя, унаследованный от MicexISSDataHandler
            container: класс контейнера пользователя
        """
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(auth.cookie_jar),
                                                  urllib.request.HTTPHandler(debuglevel=config.debug_level))
        urllib.request.install_opener(self.opener)
        self.handler = handler(container)

    def get_history_securities(self, engine, market, board, date):
        """ получить и пропарсить исторические данные по всем ценным бумагам
            на торговой системе (engine), рынке (market), режиме торгов (board) в дату (date)
        """
        url = requests['history_secs'] % {'engine': engine,
                                          'market': market,
                                          'board': board,
                                          'date': date}

        # переменная start нужна для обработки длинных ответов
        start = 0
        cnt = 1
        while cnt > 0:
            res = self.opener.open(url + '?start=' + str(start))
            jres = json.load(res)
            jhist = jres['history']
            jdata = jhist['data']
            jcols = jhist['columns']
            # тут выбираем какие колонки нам нужны
            secIdx = jcols.index('SECID')
            closeIdx = jcols.index('LEGALCLOSEPRICE')
            tradesIdx = jcols.index('NUMTRADES')

            result = []
            for sec in jdata:
                result.append((sec[secIdx],
                               del_null(sec[closeIdx]),
                               del_null(sec[tradesIdx])))
            # данные закидываем в контейнер по частям
            self.handler.do(result)
            cnt = len(jdata)
            start = start + cnt
        return True

    def get_sec_list(self, market, limit, searchtext = ''):
        """ получить и пропарсить список всех ценных бумаг
            на торговой системе (engine), рынке (market)
        """
        url = requests['sec_list'] % {'market': market}
        start = 0
        cnt = 1
        while cnt > 0 and start < limit:
            res = self.opener.open(url + '&start=' + str(start) + '&q=' + searchtext)
            jres = json.load(res)
            jsec = jres['securities']
            jdata = jsec['data']
            jcols = jsec['columns']
            secIdx = jcols.index('secid')
            nameIdx = jcols.index('name')

            result = []
            for sec in jdata:
                result.append((sec[secIdx],
                               sec[nameIdx]))
            self.handler.do(result)
            cnt = len(jdata)
            start = start + cnt
        return True


def del_null(num):
    """ заменяет null на 0
    """
    return 0 if num is None else num

