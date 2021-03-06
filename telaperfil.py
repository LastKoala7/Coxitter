from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ObjectProperty
from menu import Menu
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from titulo import Titulo
Builder.load_file("telas/perfil.kv")

#class appConfig
from appConfig import AppConfig
from postagem import Postagem

class Perfil(Screen):
    #Elementos da tela .kv
    setNome = ObjectProperty(None)
    setLogin = ObjectProperty(None)
    setFoto = ObjectProperty(None)
    setSeguidores = ObjectProperty(None)
    setSeguindo = ObjectProperty(None)
    caixinha = ObjectProperty(None)

    menu = Menu(2)

    #Barra superior
    def __init__(self, **kw):
        super().__init__(**kw)
        # Adiciona o menu a tela
        self.add_widget(self.menu)
        #Adiciona o título à tela
        Titulo(self,"Perfil")

    def retornaPerfil(self, login):
        #busca informações básicas do usuario
        UrlRequest(f'{AppConfig.servidor}/api/perfil/{login}',
                req_headers = {
                    'Authorization': f'Bearer {AppConfig.get_config("token")}'
                },
                on_success = self.perfil_sucesso,
                on_error = self.erro,
        )

        #busca a foto do perfil
        UrlRequest(f"{AppConfig.servidor}/api/foto/{login}",
            req_headers = {
                'Authorization': f'Bearer {AppConfig.get_config("token")}'
            },
            on_success = self.foto_sucesso,
            on_error = self.erro,
        )

        #pega as mensagens
        UrlRequest(f'{AppConfig.servidor}/api/buscar_msg/{login}',
            req_headers = {
                'Authorization': f'Bearer {AppConfig.get_config("token")}'
            },
            on_success = self.postagens_sucesso
        )

        self.atualizaNumeros(login)
    
    '''
    Recebe a resposta da requisição do perfil.
    Em caso de sucesso, exibe os dados do perfil.
    Em caso de erro, exibe uma mensagem vermelha.
    '''
    def perfil_sucesso(self, req, resposta):
        if (resposta['status'] == 0):
            # Exibe os dados do perfil na interface
            self.setNome.text =  resposta['nome'] 
            self.setLogin.text = f'@{resposta["login"]}'
        else:
            # Exibe a mensagem de erro na resposta
            self.setNome.text = ''
            self.setLogin.text = resposta['msg']

    def atualizaNumeros(self, login):
        #busca os seguidores
        UrlRequest(f'{AppConfig.servidor}/api/feed_SEGUIDORES/{login}',
            req_headers = {
                'Authorization': f'Bearer {AppConfig.get_config("token")}'
            },
            on_success = self.seguidores_sucesso
        )

        #busca quem o usuario segue
        UrlRequest(f'{AppConfig.servidor}/api/feed_SEGUINDO/{login}',
            req_headers = {
                'Authorization': f'Bearer {AppConfig.get_config("token")}'
            },
            on_success = self.seguindo_sucesso
        )

    '''
    Efetua o tratamento em caso de erro ao efetuar a requisição.
    '''
    def erro(self, req, erro):
        self.setNome.text = ''
        self.setLogin.text = 'Não foi possível conectar ao servidor.\nTente novamente mais tarde.'

    def foto_sucesso(self, req, resposta):
        if (resposta['status'] == 0):
            # Atualiza a foto na interface
            self.setFoto.source = resposta['url']
            self.setFoto.reload()
    
    def sair(self):
        UrlRequest(f'{AppConfig.servidor}/api/sair',
            req_headers = {
                'Authorization': f'Bearer {AppConfig.get_config("token")}'
            },
            on_success = self.saida_sucesso,
            on_error = self.erro,
        )
        AppConfig.set_config('token', None)
        
    def saida_sucesso(self, req, resposta):
        if (resposta['status'] == 0):
            self.manager.transition.direction = 'right'
            self.manager.current = 'login'        

    def postagens_sucesso(self, req, resposta):
        self.caixinha.clear_widgets()
        if (resposta['status'] == 0):
            # Exibe os dados do feed na interface
            lista = resposta['lista']
            for post in lista:
                armazem = Postagem(
                    id_post=post["id_post"],
                    nome = post['nome'],
                    usuario = post['usuario'],
                    mensagem = post['texto'],
                    data_hora = post['datahora'],
                    fota = post['foto'],
                    quantCurtidas = post["quantCurtidas"]
                )
                self.caixinha.add_widget(armazem)
    
    def seguidores_sucesso(self, req, resposta):
        num = resposta["lista"]
        num = len(num)
        if num == 1:
            self.setSeguidores.text=f"1 seguidor"
        else:
            self.setSeguidores.text=f"{num} seguidores"
    
    def seguindo_sucesso(self, req, resposta):
        num = resposta["lista"]
        self.setSeguindo.text=f"{len(num)} seguindo"


