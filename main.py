from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

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

<Test>:
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
        data: app.data
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
                text: 'Button 1'
            Button:
                text: 'Button 2'
            Button:
                text: 'Button 3'
"""

Builder.load_string(kv)


class Test(BoxLayout):
    pass
    # def populate(self):
    #     self.rv.data = [
    #         {'name.text': ''.join(sample(ascii_lowercase, 6)),
    #          'value': str(randint(0, 2000))}
    #         for x in range(50)]
    #
    # def sort(self):
    #     self.rv.data = sorted(self.rv.data, key=lambda x: x['name.text'])
    #
    # def clear(self):
    #     self.rv.data = []
    #
    # def insert(self, value):
    #     self.rv.data.insert(0, {
    #         'name.text': value or 'default value', 'value': 'unknown'})
    #
    # def update(self, value):
    #     if self.rv.data:
    #         self.rv.data[0]['name.text'] = value or 'default new value'
    #         self.rv.refresh_from_data()
    #
    # def remove(self):
    #     if self.rv.data:
    #         self.rv.data.pop(0)


class TestApp(App):
    data = [
        {'name.text': ''.join("item %i" % x),}
        for x in range(50)]
    def build(self):
        return Test()


if __name__ == '__main__':
    TestApp().run()