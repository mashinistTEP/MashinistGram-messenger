from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.app import App
from config import PURPLE, DARK, WHITE, GOLD, icon
from api import API

class SearchScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        l = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        top = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        back = Button(size_hint_x=None, width=50, background_normal='', background_color=(0,0,0,0))
        back.add_widget(Image(source=icon('back.png'), size=(25, 25), pos_hint={'center_x': 0.5, 'center_y': 0.5}))
        back.bind(on_press=lambda x: setattr(self.manager, 'current', 'chats'))
        top.add_widget(back)
        top.add_widget(Label(text='Поиск', font_size=22, color=PURPLE))
        l.add_widget(top)
        
        self.query = TextInput(hint_text='Username, email или телефон', multiline=False, size_hint_y=None, height=50, background_color=DARK, foreground_color=WHITE, cursor_color=WHITE)
        l.add_widget(self.query)
        l.add_widget(Button(text='Искать', size_hint_y=None, height=50, background_color=PURPLE, on_press=self.search))
        
        self.result = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None, height=200)
        l.add_widget(self.result)
        self.add_widget(l)

    def search(self, i):
        self.result.clear_widgets()
        res = API.request('search_user.php', data={'q': self.query.text})
        if res.get('found'):
            u = res['user']
            self.result.add_widget(Label(text=f"{u['first_name']} {u['last_name']}\n@{u['username']}\nID: {u['id']}", color=WHITE, size_hint_y=None, height=80))
            self.result.add_widget(Button(text='Написать', size_hint_y=None, height=40, background_color=GOLD, on_press=lambda x: self.start_chat(u['id'])))
        else:
            self.result.add_widget(Label(text='Не найдено', color=WHITE))

    def start_chat(self, uid):
        res = API.request('send_message.php', 'POST', {
            'token': App.get_running_app().token,
            'recipient_id': uid,
            'text': 'Привет!'
        })
        if res.get('success'):
            App.get_running_app().current_chat = res['chat_id']
            self.manager.current = 'chat'
