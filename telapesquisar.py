from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from menu import Menu
from telaperfil import Titulo
from kivy.uix.boxlayout import BoxLayout

# Carrega a interface
Builder.load_file('telas/pesquisar.kv')

class Pesquisar(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        # Adiciona o menu a tela
        menu = Menu.criar(3)
        self.add_widget(menu)
        layout = BoxLayout(size_hint_y=0.1, pos_hint={"top": 1})
        titulo = Titulo(text="Pesquisar")
        layout.add_widget(titulo)
        self.add_widget(layout)