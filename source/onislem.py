from kivy.app import App
from kivy.uix.floatlayout import FloatLayout



class OnIslemTasarim(FloatLayout):
    pass

class OnIslemApp(App):
    def build(self):
        return OnIslemTasarim()


if __name__ == '__main__':   
    OnIslemApp().run()