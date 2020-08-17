from kivy.app import App
from kivy.uix.floatlayout import FloatLayout



class SegmentasyonTasarim(FloatLayout):
    pass

class SegmentasyonApp(App):
    def build(self):
        return SegmentasyonTasarim()


if __name__ == '__main__':   
    SegmentasyonApp().run()