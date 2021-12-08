import os.path

import numpy as np
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from numpy import savez as npsave, load as npload
from graph import *
from iss import MyDataHandler, MyData
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

kv = """
<Row@RecycleKVIDsDataViewBehavior+BoxLayout>:
    canvas.before:
        Color:
            rgba: 0.5, 0.5, 0.5, 1
        Rectangle:
            size: self.size
            pos: self.pos
    value: ''
    Button:
        id: name
        background_normal: ''
        background_color: (1.0, 1.0, 1.0, 1.0)
        color: (0.0, 0.0, 0.0, 1.0)
        on_press: app.transition(self)

<MainScreen>:
    canvas:
        Color:
            rgba: 0.8, 0.8, 0.8, 1
        Rectangle:
            size: self.size
            pos: self.pos
    rv: rv
    orientation: 'vertical'
    AnchorLayout:
        size_hint: [1, 0.2]
        anchor_x: "right"
        anchor_y: "top"
        Image:
            source: 'icons/header.png'
            keep_ratio: False
            allow_stretch: True
        Label:
            text: "Главная"
            font_size: '25sp'
        TextInput:
            id: searchText
            multiline: False
            hint_text: 'Поиск'
            size_hint: [0.25, 0.3]
            on_text_validate: app.on_enter(self)
    RecycleView:
        id: rv
        scroll_type: ['bars', 'content']
        scroll_wheel_distance: dp(114)
        bar_width: dp(10)
        viewclass: 'Row'
        data: root.data
        RecycleBoxLayout:
            default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
            spacing: dp(2)
    
    AnchorLayout:
        anchor_x: "center"
        anchor_y: "bottom"
        size_hint: [1, 0.12]
        BoxLayout:
            Button:
                text: 'Главная'
                text_size: None, self.height
                color: (0.26, 0.36, 0.58, 1.0)
                background_normal: ''
                background_color: (1.0, 1.0, 1.0, 1.0)
                on_press: root.manager.current = 'main'
                Image:
                    source: 'icons/home.png'
                    size: self.parent.size
                    x: self.parent.x
                    y: self.parent.y + 5
            Button:
                text: 'Избранное'
                text_size: None, self.height
                color: (0.26, 0.36, 0.58, 1.0)
                background_normal: ''
                background_color: (1.0, 1.0, 1.0, 1.0)
                on_press: 
                    root.manager.current = 'fav'
                Image:
                    source: 'icons/fav.png'
                    size: self.parent.size
                    x: self.parent.x
                    y: self.parent.y + 5
            Button:
                text: 'Настройки'
                text_size: None, self.height
                color: (0.26, 0.36, 0.58, 1.0)
                background_normal: ''
                background_color: (1.0, 1.0, 1.0, 1.0)
                Image:
                    source: 'icons/settings.png'
                    size: self.parent.size
                    x: self.parent.x
                    y: self.parent.y + 5
                                
<GraphScreen>:
    canvas:
        Color:
            rgba: 1.0, 1.0, 1.0, 1
        Rectangle:
            size: self.size
            pos: self.pos
    BoxLayout:
        id: screen
        orientation: 'vertical'
        RelativeLayout:
            size_hint: [1, 0.2]
            Image:
                source: 'icons/header.png'
                keep_ratio: False
                allow_stretch: True 
            Label:
                id: nameShare
                font_size: '25sp'
            Button:
                size_hint: [0.1, 1]
                background_normal: ''
                background_color: (0.26, 0.36, 0.58, 0.0)
                on_press: root.manager.current = 'main'
                Image:
                    source: 'icons/back.png'
                    size: self.parent.size
                    x: self.parent.x
                    y: self.parent.y
            Button:
                size_hint: [0.1, 1]
                pos: self.parent.size[0] - self.size[0], 1
                background_normal: ''
                background_color: (0.26, 0.36, 0.58, 0.0)
                on_press:
                    root.addFav()
                Image:
                    source: 'icons/addtofav.png'
                    size: self.parent.size
                    x: self.parent.x
                    y: self.parent.y
        BoxLayout:
            background_normal: ''
            background_color: (1.0, 1.0, 1.0, 1.0)
            color: (0.0, 0.0, 0.0, 1.0)
            size_hint: [1, 0.05]
            Label:
                size_hint: [0.7, 1]
                color: (0.0, 0.0, 0.0, 1.0)
                text: 'Степень экстраполяции:'
            Button:
                size_hint: [0.1, 1]
                font_size: dp(20)
                background_normal: ''
                background_color: (0.34, 0.47, 0.63, 1.0)
                color: (0.0, 0.0, 0.0, 1.0)
                text: '1'
                on_press: root.pressOne()
            Button:
                size_hint: [0.1, 1]
                font_size: dp(20)
                background_normal: ''
                background_color: (0.34, 0.47, 0.63, 1.0)
                color: (0.0, 0.0, 0.0, 1.0)
                text: '2'
                on_press: root.pressTwo()
            Button:
                size_hint: [0.1, 1]
                font_size: dp(20)
                background_normal: ''
                background_color: (0.34, 0.47, 0.63, 1.0)
                color: (0.0, 0.0, 0.0, 1.0)
                text: '3'
                on_press: root.pressThree()
        BoxLayout:
            orientation: 'vertical'
            id: graphLayout
            BoxLayout:
                background_normal: ''
                background_color: (1.0, 1.0, 1.0, 1.0)
                color: (0.0, 0.0, 0.0, 1.0)
                size_hint: [1, 0.05]
                Label:
                    size_hint: [0.6, 1]
                    color: (0.0, 0.0, 0.0, 1.0)
                    text: 'Масштаб:'
                Button:
                    size_hint: [0.1, 1]
                    font_size: dp(20)
                    background_normal: ''
                    background_color: (0.34, 0.47, 0.63, 1.0)
                    color: (0.0, 0.0, 0.0, 1.0)
                    text: 'H'
                    on_press: root.pressH()
                Button:
                    size_hint: [0.1, 1]
                    font_size: dp(20)
                    background_normal: ''
                    background_color: (0.34, 0.47, 0.63, 1.0)
                    color: (0.0, 0.0, 0.0, 1.0)
                    text: 'D'
                    on_press: root.pressD()
                Button:
                    size_hint: [0.1, 1]
                    font_size: dp(20)
                    background_normal: ''
                    background_color: (0.34, 0.47, 0.63, 1.0)
                    color: (0.0, 0.0, 0.0, 1.0)
                    text: 'M'
                    on_press: root.pressM()
                Button:
                    size_hint: [0.1, 1]
                    font_size: dp(20)
                    background_normal: ''
                    background_color: (0.34, 0.47, 0.63, 1.0)
                    color: (0.0, 0.0, 0.0, 1.0)
                    text: 'Y'
                    on_press: root.pressY()
        BoxLayout:
            size_hint: [1, 0.12]
            Button:
                text: 'Главная'
                text_size: None, self.height
                color: (0.26, 0.36, 0.58, 1.0)
                background_normal: ''
                background_color: (1.0, 1.0, 1.0, 1.0)
                on_press: root.manager.current = 'main'
                Image:
                    source: 'icons/home.png'
                    size: self.parent.size
                    x: self.parent.x
                    y: self.parent.y + 5
            Button:
                text: 'Избранное'
                text_size: None, self.height
                color: (0.26, 0.36, 0.58, 1.0)
                background_normal: ''
                background_color: (1.0, 1.0, 1.0, 1.0)
                on_press: root.manager.current = 'fav'
                Image:
                    source: 'icons/fav.png'
                    size: self.parent.size
                    x: self.parent.x
                    y: self.parent.y + 5
            Button:
                text: 'Настройки'
                text_size: None, self.height
                color: (0.26, 0.36, 0.58, 1.0)
                background_normal: ''
                background_color: (1.0, 1.0, 1.0, 1.0)
                Image:
                    source: 'icons/settings.png'
                    size: self.parent.size
                    x: self.parent.x
                    y: self.parent.y + 5
                    
<FavouritesScreen>:
    canvas:
        Color:
            rgba: 0.8, 0.8, 0.8, 1
        Rectangle:
            size: self.size
            pos: self.pos
    rv: rv1
    orientation: 'vertical'
    AnchorLayout:
        size_hint: [1, 0.2]
        anchor_x: "right"
        anchor_y: "top"
        Image:
            source: 'icons/header.png'
            keep_ratio: False
            allow_stretch: True
        Label:
            text: "Избранное"
            font_size: '25sp'
    RecycleView:
        id: rv1
        scroll_type: ['bars', 'content']
        scroll_wheel_distance: dp(114)
        bar_width: dp(10)
        viewclass: 'Row'
        data: root.data1
        RecycleBoxLayout:
            default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
            spacing: dp(2)
    
    AnchorLayout:
        anchor_x: "center"
        anchor_y: "bottom"
        size_hint: [1, 0.12]
        BoxLayout:
            Button:
                text: 'Главная'
                text_size: None, self.height
                color: (0.26, 0.36, 0.58, 1.0)
                background_normal: ''
                background_color: (1.0, 1.0, 1.0, 1.0)
                on_press: root.manager.current = 'main'
                Image:
                    source: 'icons/home.png'
                    size: self.parent.size
                    x: self.parent.x
                    y: self.parent.y + 5
            Button:
                text: 'Избранное'
                text_size: None, self.height
                color: (0.26, 0.36, 0.58, 1.0)
                background_normal: ''
                background_color: (1.0, 1.0, 1.0, 1.0)
                on_press: 
                    root.manager.current = 'fav'
                Image:
                    source: 'icons/fav.png'
                    size: self.parent.size
                    x: self.parent.x
                    y: self.parent.y + 5
            Button:
                text: 'Настройки'
                text_size: None, self.height
                color: (0.26, 0.36, 0.58, 1.0)
                background_normal: ''
                background_color: (1.0, 1.0, 1.0, 1.0)
                Image:
                    source: 'icons/settings.png'
                    size: self.parent.size
                    x: self.parent.x
                    y: self.parent.y + 5
"""

Builder.load_string(kv)


def getCompanyShares():
    my_config = Config(user='', password='')
    my_auth = MicexAuth(my_config)
    iss = MicexISSClient(my_config, my_auth, MyDataHandler, MyData)
    engine = 'stock'
    market = 'shares'
    limit = 50
    iss.get_sec_list(engine, market, limit)
    return iss.handler.data.history


idShares = getCompanyShares()
Window.size = (480, 854)


def getFullNameShare(idShareName):
    for elem in idShares:
        if elem[0] == idShareName:
            return elem[1]
    return 'Error, can\'t find name'


def getTextMultiline(text):
    if len(text) > 50:
        for i in range(49, 0, -1):
            if text[i] == ' ':
                text = text[:i] + '\n' + text[i + 1:]
                return text
    else:
        return text


isH = False
isD = False
isM = False
isY = True


class MainScreen(BoxLayout, Screen):
    data = [
        {'name.text': ''.join(idShares[x][0])}
        for x in range(50)]


class GraphScreen(Screen):
    my_config = Config(user='', password='')
    my_auth = MicexAuth(my_config)
    iss = MicexISSClient(my_config, my_auth, MyDataHandler, MyData)
    engine = 'stock'
    market = 'shares'
    startdate = currentdate
    enddate = futuredate
    power = 3
    nowsecid = ''

    def pressH(self):
        self.iss.handler.data.history.clear()
        self.startdate = date(currentdate.year, currentdate.month, currentdate.day - 1)
        self.enddate = date(futuredate.year - 3, futuredate.month, futuredate.day + 1)
        TestApp.updateGraph(App.get_running_app())

    def pressD(self):
        self.iss.handler.data.history.clear()
        self.startdate = date(currentdate.year, currentdate.month - 1, currentdate.day)
        if futuredate.month == 12:
            self.enddate = date(futuredate.year - 2, 1, futuredate.day)
        else:
            self.enddate = date(futuredate.year - 3, futuredate.month + 1, futuredate.day)
        TestApp.updateGraph(App.get_running_app())

    def pressM(self):
        self.iss.handler.data.history.clear()
        self.startdate = date(currentdate.year - 1, currentdate.month, currentdate.day)
        self.enddate = date(futuredate.year - 2, futuredate.month, futuredate.day)
        TestApp.updateGraph(App.get_running_app())

    def pressY(self):
        self.iss.handler.data.history.clear()
        self.startdate = currentdate
        self.enddate = futuredate
        TestApp.updateGraph(App.get_running_app())

    def pressOne(self):
        self.power = 1
        TestApp.updateGraph(App.get_running_app())

    def pressTwo(self):
        self.power = 2
        TestApp.updateGraph(App.get_running_app())

    def pressThree(self):
        self.power = 3
        TestApp.updateGraph(App.get_running_app())

    def addFav(self):
        if not os.path.exists('cache'):
            os.mkdir('cache')
        with open("cache/fav.txt", "r") as f:
            lines = f.readlines()
        if self.nowsecid + '\n' in lines:
            with open("cache/fav.txt", "w") as f:
                for line in lines:
                    if line.strip("\n") != self.nowsecid:
                        f.write(line)
        else:
            with open("cache/fav.txt", "a+") as f:
                f.write(self.nowsecid + '\n')


class FavouritesScreen(BoxLayout, Screen):
    data1 = []

    def on_pre_enter(self):
        if not os.path.exists('cache'):
            os.mkdir('cache')
        if not os.path.exists('cache/fav.txt'):
            open("cache/fav.txt", "a+")
        favFile = open("cache/fav.txt", "r+")
        favList = favFile.read().rstrip('\n').split('\n')
        self.data1 = [{'name.text': ''.join(i.rstrip())}
                      for i in favList]
        self.ids.rv1.data = self.data1
        self.ids.rv1.refresh_from_data()


class TestApp(App):
    sm = ScreenManager()
    ms = MainScreen(name='main')
    gs = GraphScreen(name='graph')
    fs = FavouritesScreen(name='fav')
    sm.add_widget(ms)
    sm.add_widget(gs)
    sm.add_widget(fs)

    def on_enter(self, textInput):
        if textInput.text == '':
            self.ms.data = [
                {'name.text': ''.join(idShares[x][0])} for x in range(50)
            ]
            self.ms.ids.rv.data = self.ms.data
        else:
            my_config = Config(user='', password='')
            my_auth = MicexAuth(my_config)
            iss = MicexISSClient(my_config, my_auth, MyDataHandler, MyData)
            engine = 'stock'
            market = 'shares'
            limit = 50
            iss.handler.data.history.clear()
            iss.search_sec_list(engine, market, limit, textInput.text)
            names = iss.handler.data.history
            self.ms.data = [
                {'name.text': ''.join(names[x][0])} for x in range(0, len(names))
            ]
            self.ms.ids.rv.data = self.ms.data
        # nameShare = textInput.text
        # if nameShare in list(names[0] for names in idShares):
        #     self.ms.manager.current = 'graph'
        #     self.gs.ids.nameShare.text = getFullNameShare(nameShare)

    def updateGraph(self):
        secid = self.gs.nowsecid
        plt.clf()
        self.gs.iss.handler.data.history.clear()
        cache_path = 'cache/' + secid + str(currentdate) + '.npz'
        if os.path.isfile(cache_path):
            with npload(cache_path) as cache:
                datetimes = cache["arr_0"]
                prices = cache["arr_1"]
                arr_datetimes_ex = cache["arr_2"]
                datetimes_ex = arr_datetimes_ex[self.gs.power - 1]
                arr_prices_ex = cache["arr_3"]
                prices_ex = arr_prices_ex[self.gs.power - 1]
                if not self.gs.startdate == currentdate:
                    idxstart = np.where(datetimes < dates.date2num(self.gs.startdate))[0][-1]
                    idxend = np.where(datetimes_ex < dates.date2num(self.gs.enddate))[0][-1]
                    datetimes = datetimes[idxstart:]
                    prices = prices[idxstart:]
                    datetimes_ex = datetimes_ex[idxstart:idxend]
                    prices_ex = prices_ex[idxstart:idxend]
        else:
            self.gs.iss.get_sec_prices(self.gs.engine, self.gs.market, secid)
            history = self.gs.iss.handler.data.history
            datetimes = []
            prices = []
            for point in history:
                datetimes.append(dates.date2num(point[0]))
                prices.append(point[1])
            arr_datetimes_ex = []
            arr_prices_ex = []
            for i in range(0, 3):
                new_points, line = extrapolate(datetimes, prices, i + 1)
                datetimes_ex = datetimes + new_points
                prices_ex = line(datetimes_ex)
                arr_datetimes_ex.append(datetimes_ex)
                arr_prices_ex.append(prices_ex)
            if not os.path.exists('cache'):
                os.mkdir('cache')
            npsave(cache_path, datetimes, prices, arr_datetimes_ex, arr_prices_ex)
        fig, graph = plt.subplots()
        graph.plot_date(datetimes, prices, 'b', ms=0.1, lw=1.5, ls='-')
        graph.plot_date(datetimes_ex, prices_ex, 'r', ms=0.1, lw=2, ls='-')
        graph.set(xlabel='date', ylabel='close price', title=secid)
        locator = dates.AutoDateLocator()
        formatter = dates.ConciseDateFormatter(locator)
        graph.xaxis.set_major_locator(locator)
        graph.xaxis.set_major_formatter(formatter)
        graph.grid()
        if len(self.gs.ids.graphLayout.children) > 1:
            self.gs.ids.graphLayout.remove_widget(self.gs.ids.graphLayout.children[0])
        self.gs.ids.graphLayout.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def transition(self, btn):
        self.ms.manager.current = 'graph'
        self.gs.ids.nameShare.text = getTextMultiline(getFullNameShare(btn.text))
        plt.clf()
        self.gs.iss.handler.data.history.clear()
        self.gs.nowsecid = btn.text
        self.updateGraph()

    def build(self):
        return self.sm


if __name__ == '__main__':
    TestApp().run()
