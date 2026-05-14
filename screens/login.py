from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from config import PURPLE, DARK, WHITE, DARKER
from api import API

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0,0,0,0)
        self.bind(pos=self.update, size=self.update)
    def update(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[10])

class LoginScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        l = BoxLayout(orientation='vertical', padding=[50, 80, 50, 320], spacing=15)
        l.add_widget(Label(text='MashinistGram', font_size=34, color=PURPLE, bold=True, size_hint_y=None, height=90))
        self.email = TextInput(hint_text='Email', multiline=False, size_hint_y=None, height=50, background_color=DARK, foreground_color=WHITE, cursor_color=WHITE)
        self.pw = TextInput(hint_text='Пароль', password=True, multiline=False, size_hint_y=None, height=50, background_color=DARK, foreground_color=WHITE, cursor_color=WHITE)
        l.add_widget(self.email)
        l.add_widget(self.pw)
        btn1 = RoundedButton(text='Войти', size_hint_y=None, height=50, on_press=self.login)
        btn1.bg = PURPLE
        btn1.color = WHITE
        l.add_widget(btn1)
        btn2 = RoundedButton(text='Регистрация', size_hint_y=None, height=50, on_press=lambda x: setattr(self.manager, 'current', 'register'))
        btn2.bg = DARK
        btn2.color = WHITE
        l.add_widget(btn2)
        self.add_widget(l)

    def login(self, i):
        res = API.request('login.php', 'POST', {'email': self.email.text, 'password': self.pw.text})
        if 'token' in res:
            app = App.get_running_app()
            app.token, app.user_id = res['token'], res['user_id']
            app.save_session()
            self.manager.current = 'chats'
        else:
            self.email.text = res.get('error', 'Ошибка')

class RegisterScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        l = BoxLayout(orientation='vertical', padding=[50, 20, 50, 200], spacing=10)
        l.add_widget(Label(text='Регистрация', font_size=28, color=PURPLE, bold=True, size_hint_y=None, height=60))
        self.fn = TextInput(hint_text='Имя', multiline=False, size_hint_y=None, height=45, background_color=DARK, foreground_color=WHITE, cursor_color=WHITE)
        self.ln = TextInput(hint_text='Фамилия', multiline=False, size_hint_y=None, height=45, background_color=DARK, foreground_color=WHITE, cursor_color=WHITE)
        self.uname = TextInput(hint_text='Username (необязательно)', multiline=False, size_hint_y=None, height=45, background_color=DARK, foreground_color=WHITE, cursor_color=WHITE)
        self.email = TextInput(hint_text='Email', multiline=False, size_hint_y=None, height=45, background_color=DARK, foreground_color=WHITE, cursor_color=WHITE)
        self.pw = TextInput(hint_text='Пароль (мин 6)', password=True, multiline=False, size_hint_y=None, height=45, background_color=DARK, foreground_color=WHITE, cursor_color=WHITE)
        for w in [self.fn, self.ln, self.uname, self.email, self.pw]: l.add_widget(w)
        btn1 = RoundedButton(text='Зарегистрироваться', size_hint_y=None, height=50, on_press=self.reg)
        btn1.bg = PURPLE
        btn1.color = WHITE
        l.add_widget(btn1)
        btn2 = RoundedButton(text='Назад', size_hint_y=None, height=50, on_press=lambda x: setattr(self.manager, 'current', 'login'))
        btn2.bg = DARK
        btn2.color = WHITE
        l.add_widget(btn2)
        self.add_widget(l)

    def reg(self, i):
        res = API.request('register.php', 'POST', {
            'email': self.email.text,
            'password': self.pw.text,
            'first_name': self.fn.text,
            'last_name': self.ln.text,
            'username': self.uname.text
        })
        if 'token' in res:
            app = App.get_running_app()
            app.token, app.user_id = res['token'], res['user_id']
            app.save_session()
            self.manager.current = 'chats'
        else:
            self.fn.text = res.get('error', 'Ошибка')
