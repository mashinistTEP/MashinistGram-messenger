from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.app import App
from config import PURPLE, DARK, WHITE, GOLD, icon
from api import API
import os

class SettingsScreen(Screen):
    def stars_popup(self):
        res = API.request('check_token.php', data={'token': App.get_running_app().token})
        balance = res['user']['stars_balance'] if res.get('valid') else 0
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        content.add_widget(Image(source=icon('star.png'), size=(50, 50), pos_hint={'center_x': 0.5}))
        content.add_widget(Label(text=f'Ваш баланс: {balance} ⭐', font_size=20, color=GOLD, halign='center'))
        p = Popup(title='Звёзды', content=content, size_hint=(0.6, 0.4))
        p.open()

    def premium_popup(self):
        res = API.request('check_token.php', data={'token': App.get_running_app().token})
        has_premium = res['user'].get('has_premium', False) if res.get('valid') else False
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        content.add_widget(Image(source=icon('premium_star.png'), size=(50, 50), pos_hint={'center_x': 0.5}))
        status = 'Активен ✅' if has_premium else 'Не активен'
        content.add_widget(Label(text=f'Премиум: {status}', font_size=20, color=PURPLE, halign='center'))
        content.add_widget(Label(text='Функции:\n- Звёздочка у ника\n- Жирный фиолетовый ник\n- Приоритетная поддержка', color=WHITE, halign='center'))
        p = Popup(title='Премиум', content=content, size_hint=(0.7, 0.5))
        p.open()

    def get_cache_size(self):
        cache_dir = App.get_running_app().user_data_dir
        total = 0
        if os.path.exists(cache_dir):
            for root, dirs, files in os.walk(cache_dir):
                for f in files:
                    total += os.path.getsize(os.path.join(root, f))
        mb = total / (1024 * 1024)
        return f"{mb:.1f} MB" if mb > 0.1 else f"{total} B"

    def clear_cache(self, instance):
        import shutil
        cache_dir = App.get_running_app().user_data_dir
        if os.path.exists(cache_dir):
            for item in os.listdir(cache_dir):
                path = os.path.join(cache_dir, item)
                if os.path.isfile(path): os.remove(path)
                elif os.path.isdir(path): shutil.rmtree(path)
        Popup(title='Готово', content=Label(text='Кэш очищен!'), size_hint=(0.6, 0.3)).open()
        self.on_enter()

    def on_enter(self):
        self.clear_widgets()
        l = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        top = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        back = Button(size_hint_x=None, width=50, background_normal='', background_color=(0,0,0,0))
        back.add_widget(Image(source=icon('back.png'), size=(25, 25), pos_hint={'center_x': 0.5, 'center_y': 0.5}))
        back.bind(on_press=lambda x: setattr(self.manager, 'current', 'chats'))
        top.add_widget(back)
        top.add_widget(Label(text='Настройки', font_size=22, color=PURPLE))
        l.add_widget(top)
        
        row1 = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        row1.add_widget(Image(source=icon('star.png'), size=(30, 30)))
        row1.add_widget(Label(text='Звёзды', color=WHITE))
        btn1 = Button(text='>', size_hint_x=None, width=50, background_color=(0,0,0,0), on_press=lambda x: self.stars_popup())
        row1.add_widget(btn1)
        l.add_widget(row1)
        
        row2 = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        row2.add_widget(Image(source=icon('premium_star.png'), size=(30, 30)))
        row2.add_widget(Label(text='Премиум', color=WHITE))
        btn2 = Button(text='>', size_hint_x=None, width=50, background_color=(0,0,0,0), on_press=lambda x: self.premium_popup())
        row2.add_widget(btn2)
        l.add_widget(row2)
        
        cache_size = self.get_cache_size()
        l.add_widget(Label(text=f'Кэш: {cache_size}', color=WHITE, size_hint_y=None, height=40))
        l.add_widget(Button(text='Очистить кэш', size_hint_y=None, height=50, background_color=DARK, on_press=self.clear_cache))
        
        self.add_widget(l)
