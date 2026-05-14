from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.app import App
from config import PURPLE, DARK, WHITE
from api import API

class ChatsScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        l = BoxLayout(orientation='vertical')
        
        # Верхняя панель
        top = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, padding=[10, 10])
        menu_btn = Button(text='☰', size_hint_x=None, width=50, background_color=DARK, on_press=self.open_menu)
        top.add_widget(menu_btn)
        top.add_widget(Label(text='MashinistGram', font_size=22, color=PURPLE, bold=True))
        top.add_widget(Button(text='🔍', size_hint_x=None, width=60, background_color=DARK, on_press=lambda x: setattr(self.manager, 'current', 'search')))
        l.add_widget(top)
        
        # Никнейм
        res = API.request('check_token.php', data={'token': App.get_running_app().token})
        if res.get('valid'):
            u = res['user']
            l.add_widget(Label(text=f"Вы: {u['first_name']} {u['last_name']}", size_hint_y=None, height=30, color=WHITE, padding=[10, 0]))
        
        # Список чатов
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
                btn = Button(text=name, size_hint_y=None, height=70, background_color=DARK, on_press=lambda x, cid=chat['id']: self.open_chat(cid))
                cl.add_widget(btn)
        else:
            cl.add_widget(Label(text='Нет чатов\n\nНажмите 🔍 для поиска', color=WHITE, halign='center'))
        sv.add_widget(cl)
        l.add_widget(sv)
        self.add_widget(l)

    def open_menu(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)
        content.add_widget(Button(text='💬 Чаты', size_hint_y=None, height=50, background_color=PURPLE, on_press=lambda x: self.menu_action('chats')))
        content.add_widget(Button(text='👥 Контакты', size_hint_y=None, height=50, background_color=PURPLE, on_press=lambda x: self.menu_action('search')))
        content.add_widget(Button(text='⚙️ Настройки', size_hint_y=None, height=50, background_color=PURPLE, on_press=lambda x: self.menu_action('settings')))
        content.add_widget(Button(text='👤 Профиль', size_hint_y=None, height=50, background_color=PURPLE, on_press=lambda x: self.menu_action('profile')))
        
        self.popup = Popup(title='Меню', content=content, size_hint=(0.7, 0.5), auto_dismiss=True)
        self.popup.open()

    def menu_action(self, screen):
        self.popup.dismiss()
        self.manager.current = screen

    def open_chat(self, cid):
        App.get_running_app().current_chat = cid
        self.manager.current = 'chat'
