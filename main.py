import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import requests
import json

# ====== НАСТРОЙКИ ======
API_URL = "https://mashinistgrammsg.atwebpages.com/api/mg"
Window.clearcolor = get_color_from_hex('#1A1A2E')
PURPLE = get_color_from_hex('#B659FF')
GOLD = get_color_from_hex('#FFD700')
DARK = get_color_from_hex('#2A2A3E')
WHITE = (1, 1, 1, 1)

# ====== API ======
class API:
    @staticmethod
    def request(endpoint, method='GET', data=None):
        url = f"{API_URL}/{endpoint}"
        try:
            r = requests.get(url, params=data, timeout=10) if method == 'GET' else requests.post(url, data=data, timeout=10)
            return r.json()
        except Exception as e:
            return {'error': str(e)}

# ====== ЭКРАНЫ ======
class LoginScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        l = BoxLayout(orientation='vertical', padding=[40, 120, 40, 280], spacing=15)
        l.add_widget(Label(text='MashinistGram', font_size=32, color=PURPLE, bold=True, size_hint_y=None, height=80))
        self.email = TextInput(hint_text='Email', multiline=False, size_hint_y=None, height=50)
        self.pw = TextInput(hint_text='Пароль', password=True, multiline=False, size_hint_y=None, height=50)
        l.add_widget(self.email)
        l.add_widget(self.pw)
        l.add_widget(Button(text='Войти', size_hint_y=None, height=50, background_color=PURPLE, on_press=self.login))
        l.add_widget(Button(text='Регистрация', size_hint_y=None, height=50, background_color=DARK, on_press=lambda x: setattr(self.manager, 'current', 'register')))
        self.add_widget(l)
    
    def login(self, i):
        res = API.request('login.php', 'POST', {'email': self.email.text, 'password': self.pw.text})
        if 'token' in res:
            app = App.get_running_app()
            app.token, app.user_id = res['token'], res['user_id']
            self.manager.current = 'chats'
        else:
            self.email.text = res.get('error', 'Ошибка')

class RegisterScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        l = BoxLayout(orientation='vertical', padding=[40, 60, 40, 220], spacing=12)
        l.add_widget(Label(text='Регистрация', font_size=28, color=PURPLE, bold=True, size_hint_y=None, height=60))
        self.fn = TextInput(hint_text='Имя', multiline=False, size_hint_y=None, height=50)
        self.ln = TextInput(hint_text='Фамилия', multiline=False, size_hint_y=None, height=50)
        self.email = TextInput(hint_text='Email', multiline=False, size_hint_y=None, height=50)
        self.pw = TextInput(hint_text='Пароль (мин 6)', password=True, multiline=False, size_hint_y=None, height=50)
        for w in [self.fn, self.ln, self.email, self.pw]: l.add_widget(w)
        l.add_widget(Button(text='Зарегистрироваться', size_hint_y=None, height=50, background_color=PURPLE, on_press=self.reg))
        l.add_widget(Button(text='Назад', size_hint_y=None, height=50, background_color=DARK, on_press=lambda x: setattr(self.manager, 'current', 'login')))
        self.add_widget(l)
    
    def reg(self, i):
        res = API.request('register.php', 'POST', {'email': self.email.text, 'password': self.pw.text, 'first_name': self.fn.text, 'last_name': self.ln.text})
        if 'token' in res:
            app = App.get_running_app()
            app.token, app.user_id = res['token'], res['user_id']
            self.manager.current = 'chats'
        else:
            self.fn.text = res.get('error', 'Ошибка')

class ChatsScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        l = BoxLayout(orientation='vertical')
        l.add_widget(Label(text='Чаты', font_size=24, color=PURPLE, size_hint_y=None, height=60))
        sv = ScrollView()
        cl = BoxLayout(orientation='vertical', spacing=5, padding=10, size_hint_y=None)
        cl.bind(minimum_height=cl.setter('height'))
        
        res = API.request('get_chats.php', data={'token': App.get_running_app().token})
        if 'chats' in res:
            for chat in res['chats']:
                name = chat.get('title', 'Чат')
                if chat.get('with_user'):
                    u = chat['with_user']
                    name = f"{u.get('first_name','')} {u.get('last_name','')}"
                btn = Button(text=f"{name}\n{chat.get('last_message','')[:50]}", size_hint_y=None, height=70, background_color=DARK, on_press=lambda x, cid=chat['id']: self.open_chat(cid))
                cl.add_widget(btn)
        sv.add_widget(cl)
        l.add_widget(sv)
        self.add_widget(l)
    
    def open_chat(self, cid):
        App.get_running_app().current_chat = cid
        self.manager.current = 'chat'

class ChatScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        cid = App.get_running_app().current_chat
        l = BoxLayout(orientation='vertical')
        l.add_widget(Label(text=f'Чат #{cid}', font_size=20, color=PURPLE, size_hint_y=None, height=50))
        sv = ScrollView()
        ml = BoxLayout(orientation='vertical', spacing=5, padding=10, size_hint_y=None)
        ml.bind(minimum_height=ml.setter('height'))
        
        res = API.request('get_messages.php', data={'token': App.get_running_app().token, 'chat_id': cid, 'limit': 20})
        if 'messages' in res:
            for msg in res['messages']:
                sender = f"{msg.get('first_name','')} {msg.get('last_name','')}"
                ml.add_widget(Label(text=f"{sender}: {msg['text']}", size_hint_y=None, height=40, color=WHITE))
        sv.add_widget(ml)
        l.add_widget(sv)
        
        bl = BoxLayout(size_hint_y=None, height=50)
        self.msg_input = TextInput(hint_text='Сообщение...', multiline=False)
        bl.add_widget(self.msg_input)
        bl.add_widget(Button(text='→', size_hint_x=None, width=60, background_color=PURPLE, on_press=self.send))
        l.add_widget(bl)
        self.add_widget(l)
    
    def send(self, i):
        API.request('send_message.php', 'POST', {
            'token': App.get_running_app().token,
            'chat_id': App.get_running_app().current_chat,
            'text': self.msg_input.text
        })
        self.msg_input.text = ''
        self.on_enter()

class SearchScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        l = BoxLayout(orientation='vertical', padding=20, spacing=10)
        l.add_widget(Label(text='Поиск', font_size=24, color=PURPLE, size_hint_y=None, height=50))
        self.query = TextInput(hint_text='Username, email или телефон', multiline=False, size_hint_y=None, height=50)
        l.add_widget(self.query)
        l.add_widget(Button(text='Искать', size_hint_y=None, height=50, background_color=PURPLE, on_press=self.search))
        self.result = Label(text='', color=WHITE)
        l.add_widget(self.result)
        l.add_widget(Button(text='Назад', size_hint_y=None, height=50, background_color=DARK, on_press=lambda x: setattr(self.manager, 'current', 'chats')))
        self.add_widget(l)
    
    def search(self, i):
        res = API.request('search_user.php', data={'q': self.query.text})
        if res.get('found'):
            u = res['user']
            self.result.text = f"{u['first_name']} {u['last_name']}\n@{u['username']}\nID: {u['id']}"
        else:
            self.result.text = 'Не найдено'

# ====== ПРИЛОЖЕНИЕ ======
class MashinistGramApp(App):
    token = None
    user_id = None
    current_chat = None
    
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(ChatsScreen(name='chats'))
        sm.add_widget(ChatScreen(name='chat'))
        sm.add_widget(SearchScreen(name='search'))
        sm.current = 'login'
        return sm

if __name__ == '__main__':
    MashinistGramApp().run()
