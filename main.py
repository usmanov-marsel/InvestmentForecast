from kivy.app import App
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from client import *
from iss import MyDataHandler, MyData

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
        on_press: app.transition(self)

<MainScreen>:
    canvas:
        Color:
            rgba: 0.3, 0.3, 0.3, 1
        Rectangle:
            size: self.size
            pos: self.pos
    rv: rv
    orientation: 'vertical'
    AnchorLayout:
        anchor_x: "center"
        anchor_y: "top"
        size_hint: [1, 0.15]
        Label:
            text: "Главная"

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
        size_hint: [1, 0.1]
        BoxLayout:
            Button:
                text: 'Главная'
            Button:
                text: 'Избранное'
            Button:
                text: 'Настройки'
                
<GraphScreen>:
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            size_hint: [1, 0.15]
            Button:
                text: 'Back'
                size_hint: [0.1, 1]
                on_press: root.manager.current = 'main'
            Label:
                id: nameShare  
        Label:
            text: 'График'  
        BoxLayout:
            size_hint: [1, 0.1]
            Button:
                text: 'Главная'
                on_press: root.manager.current = 'main'
            Button:
                text: 'Избранное'
            Button:
                text: 'Настройки'
"""

Builder.load_string(kv)


def getCompanyShares():
    my_config = Config(user='', password='')
    my_auth = MicexAuth(my_config)
    iss = MicexISSClient(my_config, my_auth, MyDataHandler, MyData)
    market = 'shares'
    limit = 50
    iss.get_sec_list(market, limit)
    return iss.handler.data.history

idShares = getCompanyShares()

def getFullNameShare(idShareName):
    for elem in idShares:
        if elem[0] == idShareName:
            return elem[1]
    return 'Error, don\'t find name'


class MainScreen(BoxLayout, Screen):
    data = [
        {'name.text': ''.join(idShares[x][0])}
        for x in range(50)]


class GraphScreen(Screen):
    pass


class TestApp(App):
    sm = ScreenManager()
    ms = MainScreen(name='main')
    gs = GraphScreen(name='graph')
    sm.add_widget(ms)
    sm.add_widget(gs)

    def transition(self, btn):
        self.ms.manager.current = 'graph'
        self.gs.nameShare = btn.text
        self.gs.ids.nameShare.text = getFullNameShare(btn.text)

    def build(self):
        return self.sm


if __name__ == '__main__':
    TestApp().run()