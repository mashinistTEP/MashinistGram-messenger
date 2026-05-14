from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from config import PURPLE, DARK, WHITE
from api import API

class ChatScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        cid = App.get_running_app().current_chat
        l = BoxLayout(orientation='vertical')
        
        # Верхняя панель
        top = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=[10, 5])
        back = Button(text='←', size_hint_x=None, width=50, background_color=DARK, on_press=lambda x: setattr(self.manager, 'current', 'chats'))
        top.add_widget(back)
        top.add_widget(Label(text=f'Чат #{cid}', font_size=18, color=PURPLE))
        l.add_widget(top)
        
        # Сообщения
        sv = ScrollView()
        self.ml = BoxLayout(orientation='vertical', spacing=5, padding=10, size_hint_y=None)
        self.ml.bind(minimum_height=self.ml.setter('height'))
        
        res = API.request('get_messages.php', data={'token': App.get_running_app().token, 'chat_id': cid, 'limit': 20})
        if 'messages' in res:
            for msg in res['messages']:
                sender = f"{msg.get('first_name','')} {msg.get('last_name','')}"
                self.ml.add_widget(Label(text=f"{sender}: {msg['text']}", size_hint_y=None, height=40, color=WHITE))
        sv.add_widget(self.ml)
        l.add_widget(sv)
        
        # Поле ввода
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
