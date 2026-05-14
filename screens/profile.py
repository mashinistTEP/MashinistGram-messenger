from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.app import App
from config import PURPLE, DARK, WHITE, GOLD, icon
from api import API

class ProfileScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        l = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        top = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        back = Button(size_hint_x=None, width=50, background_normal='', background_color=(0,0,0,0))
        back.add_widget(Image(source=icon('back.png'), size=(25, 25), pos_hint={'center_x': 0.5, 'center_y': 0.5}))
        back.bind(on_press=lambda x: setattr(self.manager, 'current', 'chats'))
        top.add_widget(back)
        top.add_widget(Label(text='Профиль', font_size=22, color=PURPLE))
        l.add_widget(top)
        
        res = API.request('check_token.php', data={'token': App.get_running_app().token})
        if res.get('valid'):
            u = res['user']
            l.add_widget(Image(source=icon('user.png'), size=(80, 80), pos_hint={'center_x': 0.5}))
            name = f"{u['first_name']} {u['last_name']}"
            if u.get('verified'):
                name += ' ✅'
            l.add_widget(Label(text=name, font_size=24, color=WHITE, halign='center'))
            l.add_widget(Label(text=f"Email: {u['email']}", color=WHITE, halign='center'))
            l.add_widget(Label(text=f"⭐ {u.get('stars_balance', 0)}", color=GOLD, halign='center'))
        
        l.add_widget(Button(text='Выйти', size_hint_y=None, height=50, background_color=DARK, on_press=self.logout))
        self.add_widget(l)

    def logout(self, i):
        API.request('logout.php', 'POST', {'token': App.get_running_app().token})
        App.get_running_app().token = None
        App.get_running_app().user_id = None
        self.manager.current = 'login'
