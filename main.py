from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
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
            font_size: 25
        TextInput:
            id: searchText
            multiline: False
            hint_text: 'search'
            size_hint: [0.25, 0.6]
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

    def transition(self, btn):
        self.ms.manager.current = 'graph'
        self.gs.ids.nameShare.text = getTextMultiline(getFullNameShare(btn.text))

    def build(self):
        return self.sm


if __name__ == '__main__':
    TestApp().run()
