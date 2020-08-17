from kivy.app import App
from kivy.uix.floatlayout import FloatLayout



class MorfolojiTasarim(FloatLayout):
    pass

class MorfolojiApp(App):
    def build(self):
        return MorfolojiTasarim()


if __name__ == '__main__':   
    MorfolojiApp().run()