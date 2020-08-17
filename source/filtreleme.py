from kivy.app import App
from kivy.uix.floatlayout import FloatLayout



class FiltrelemeTasarim(FloatLayout):
    pass

class FiltrelemeApp(App):
    def build(self):
        return FiltrelemeTasarim()


if __name__ == '__main__':   
    FiltrelemeApp().run()