from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
Builder.load_file("editnomesenha.kv")

class editnomesenha(BoxLayout):
    pass

class MyApp(App):
    def build(self):
        return editnomesenha()

if __name__ == '__main__':
    MyApp().run()