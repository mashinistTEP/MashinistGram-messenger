from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from config import PURPLE, DARK, WHITE, DARKER, icon
from api import API

class IconButton(Button):
    def __init__(self, icon_name, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0,0,0,0)
        self.img = Image(source=icon(icon_name), size=(30, 30), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(self.img)
        self.bind(pos=self.update, size=self.update)
    def update(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*DARK)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[8])

class ChatButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0,0,0,0)
        self.bind(pos=self.update, size=self.update)
    def update(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*DARKER)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[8])

class ChatsScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        l = BoxLayout(orientation='vertical')
        
        top = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, padding=[10, 10])
        top.add_widget(IconButton('menu.png', size_hint_x=None, width=50, on_press=self.open_menu))
        top.add_widget(Label(text='MashinistGram', font_size=22, color=PURPLE, bold=True))
        top.add_widget(IconButton('search.png', size_hint_x=None, width=50, on_press=lambda x: setattr(self.manager, 'current', 'search')))
        l.add_widget(top)
        
        res = API.request('check_token.php', data={'token': App.get_running_app().token})
        if res.get('valid'):
            u = res['user']
            name = f"{u['first_name']} {u['last_name']}"
            if u.get('verified'): name += ' ✅'
            if u.get('has_premium'): name += ' ⭐'
            l.add_widget(Label(text=f"  {name}", size_hint_y=None, height=30, color=WHITE, halign='left'))
        
        sv = ScrollView()
        cl = BoxLayout(orientation='vertical', spacing=5, padding=10, size_hint_y=None)
        cl.bind(minimum_height=cl.setter('height'))

        chats_res = API.request('get_chats.php', data={'token': App.get_running_app().token})
        if 'chats' in chats_res and len(chats_res['chats']) > 0:
            for chat in chats_res['chats']:
                name = chat.get('title', 'Чат')
                if chat.get('with_user'):
                    u = chat['with_user']
                    name = f"{u.get('first_name','')} {u.get('last_name','')}"
                    if u.get('verified'): name += ' ✅'
                    if u.get('has_premium'): name += ' ⭐'
                btn = ChatButton(text=name, size_hint_y=None, height=70, on_press=lambda x, cid=chat['id']: self.open_chat(cid))
                cl.add_widget(btn)
        else:
            cl.add_widget(Label(text='Нет чатов\n\nНажмите на лупу для поиска', color=WHITE, halign='center'))
        sv.add_widget(cl)
        l.add_widget(sv)
        self.add_widget(l)

    def open_menu(self, instance):
        content = BoxLayout(orientation='vertical', spacing=15, padding=20)
        items = [
            ('user.png', 'Профиль', 'profile'),
            ('search.png', 'Контакты', 'search'),
            ('settings.png', 'Настройки', 'settings'),
        ]
        for icon_name, text, screen in items:
            row = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=None, height=50)
            row.add_widget(Image(source=icon(icon_name), size=(35, 35)))
            lbl = Label(text=text, color=WHITE, halign='left', valign='middle')
            lbl.bind(size=lbl.setter('text_size'))
            row.add_widget(lbl)
            row.bind(on_touch_down=lambda instance, touch, s=screen: self.menu_action(s) if instance.collide_point(*touch.pos) else None)
            content.add_widget(row)
        self.popup = Popup(title='Меню', content=content, size_hint=(0.7, 0.45), auto_dismiss=True)
        self.popup.open()

    def menu_action(self, screen):
        self.popup.dismiss()
        self.manager.current = screen

    def open_chat(self, cid):
        App.get_running_app().current_chat = cid
        self.manager.current = 'chat'
