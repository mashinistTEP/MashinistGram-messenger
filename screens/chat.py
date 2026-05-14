from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from config import PURPLE, DARK, WHITE, MSG_MINE, MSG_THEIR, icon
from api import API

class MessageBubble(Label):
    def __init__(self, mine=False, **kwargs):
        super().__init__(**kwargs)
        self.mine = mine
        self.bind(pos=self.update, size=self.update)
    def update(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*MSG_MINE if self.mine else MSG_THEIR)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[10])

class ChatScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        cid = App.get_running_app().current_chat
        l = BoxLayout(orientation='vertical')
        
        top = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=[10, 5])
        back = Button(size_hint_x=None, width=50, background_normal='', background_color=(0,0,0,0))
        back.add_widget(Image(source=icon('back.png'), size=(25, 25), pos_hint={'center_x': 0.5, 'center_y': 0.5}))
        back.bind(on_press=lambda x: setattr(self.manager, 'current', 'chats'))
        top.add_widget(back)
        top.add_widget(Label(text=f'Чат', font_size=18, color=PURPLE))
        l.add_widget(top)
        
        sv = ScrollView()
        self.ml = BoxLayout(orientation='vertical', spacing=5, padding=10, size_hint_y=None)
        self.ml.bind(minimum_height=self.ml.setter('height'))
        
        res = API.request('get_messages.php', data={'token': App.get_running_app().token, 'chat_id': cid, 'limit': 20})
        if 'messages' in res:
            for msg in res['messages']:
                mine = (msg['sender_id'] == App.get_running_app().user_id)
                sender = "Я" if mine else f"{msg.get('first_name','')}"
                bubble = MessageBubble(text=f"{sender}: {msg['text']}", size_hint_y=None, height=40, color=WHITE, mine=mine)
                self.ml.add_widget(bubble)
        sv.add_widget(self.ml)
        l.add_widget(sv)
        
        bl = BoxLayout(size_hint_y=None, height=50, padding=[5, 5])
        self.msg_input = TextInput(hint_text='Сообщение...', multiline=False, background_color=DARK, foreground_color=WHITE, cursor_color=WHITE)
        bl.add_widget(self.msg_input)
        send_btn = Button(size_hint_x=None, width=50, background_normal='', background_color=(0,0,0,0))
        send_btn.add_widget(Image(source=icon('send.png'), size=(25, 25), pos_hint={'center_x': 0.5, 'center_y': 0.5}))
        send_btn.bind(on_press=self.send)
        bl.add_widget(send_btn)
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
