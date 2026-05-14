from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.app import App
from config import PURPLE, DARK
from api import API

class LoginScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        l = BoxLayout(orientation='vertical', padding=[40, 40, 40, 400], spacing=15)
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
        l = BoxLayout(orientation='vertical', padding=[40, 10, 40, 350], spacing=12)
        l.add_widget(Label(text='Регистрация', font_size=28, color=PURPLE, bold=True, size_hint_y=None, height=60))
        self.fn = TextInput(hint_text='Имя', multiline=False, size_hint_y=None, height=45)
        self.ln = TextInput(hint_text='Фамилия', multiline=False, size_hint_y=None, height=45)
        self.email = TextInput(hint_text='Email', multiline=False, size_hint_y=None, height=45)
        self.pw = TextInput(hint_text='Пароль (мин 6)', password=True, multiline=False, size_hint_y=None, height=45)
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
