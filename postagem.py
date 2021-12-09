from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color
from kivy.uix.image import AsyncImage
from kivy.clock import Clock

global larguraBox

#Classe para o corpo da mensagem
class Mensagem(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_x = 1

        #Nunca tire essa linha se não seu aparelho vai explodir
        Clock.schedule_interval(self.atualizaLargura, 1/10)

    def atualizaLargura(self, *args):
        global larguraBox
        self.size= self.texture_size
        self.text_size = larguraBox, None
        
#Sem ela a mensagem não vai ficar legal
class Caixa(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(size=self.update_rect)
    
    def update_rect(instance, value, *args):
        #Armazena a largura do box lateral direito para passar ao labelMensagem
        global larguraBox
        larguraBox = instance.size[0]

#pode tirar dps
class Grid(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(pos=self.update_rect, size=self.update_rect)
        
        with self.canvas.before:
            Color(.0, .11, 0.1, 1)
            #ARMAZENANDO A FORMA EM UMA VARIÁVEL
            self.rect=Rectangle(pos=self.pos, size=self.size)
    
    def update_rect(instance, value, *args):
        #E ATUALIZANDO ELA ATRAVÉS DE UMA FUNÇÃO
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

#classe para botão
class Botao(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size=(30,30)
        self.size_hint = (None, None)
        self.border=(0,0,0,0)

class DataHora(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size="15sp"
        self.halign = 'right'
        #QUANDO TRABALHAR COM O TAMANHO TEM QUE USAR O DEF ON_SIZE()
    def on_size(self, *args):
        #tamanho
        self.text_size=self.size

class Postagem(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spacing=0
        self.padding=0

        layout=GridLayout(
            cols=2
        )

        #Imagem de perfil
        #LADO ESQUERDO
        imgPerfil=AsyncImage(
            source="telas/imagens/padrao.png",
            size_hint_x = 0.3,
            size_hint_y=1, #centraliza a imagem na postagem
            
        )
        layout.add_widget(imgPerfil)

        #Esse boxlayout está pegando algumas configurações padrão 
        # do nosso 'widgets_confi.kv'. Por isso algumas variáveis
        # são necessárias
        #LADO DIREITO
        box=Caixa(
            padding=0,
            spacing=40 
        )

        #Nome e login
        gridNome=GridLayout(
            spacing = 20,
            cols=2
        )
        labelNome=Label(
            text="FuracãoDaCPI"
        )
        labelLogin=Label(
            text="@robsu"
        )
        gridNome.add_widget(labelNome)
        gridNome.add_widget(labelLogin)
        box.add_widget(gridNome)

        #Texto da mensagem
        labelTexto=Mensagem(
            text="Gente, fui hackeado! se eu aparecer no privado pedindo 5000 reais, sou eu mesmo! pfv paguem"

        )
        box.add_widget(labelTexto)

        #Botões
        gridIcones=GridLayout(
            cols=4,
            spacing=50
        )
        aux = Label(text="")
        btnCurtir=Botao(
            background_normal='telas/imagens/curtir.png'
        )
        btnComentar=Botao(
            background_normal='telas/imagens/comentario.png'
        )
        aux2 = Label(text="")
        gridIcones.add_widget(aux)
        gridIcones.add_widget(btnComentar)
        gridIcones.add_widget(btnCurtir)
        gridIcones.add_widget(aux2)
        box.add_widget(gridIcones)

        #Data e hora
        labelDataHora=DataHora(
            text="08/12/2021 · 22:30"
        )
        box.add_widget(labelDataHora)

        #Termina de montar o grid
        layout.add_widget(box)

        #Armazena em um boxlayout
        self.add_widget(layout)

        #Para poder adicionar essa linha no fim
        imgLinha=AsyncImage(
            source='telas/imagens/barrinha.png',
            # size_hint_y=0.4
        )
        self.add_widget(imgLinha)