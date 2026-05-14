from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.app import App
from config import PURPLE, DARK, WHITE, GOLD
from api import API
import os

class SettingsScreen(Screen):
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
        cache_dir = App.get_running_app().user_data_dir
        if os.path.exists(cache_dir):
            import shutil
            for item in os.listdir(cache_dir):
                path = os.path.join(cache_dir, item)
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
        popup = Popup(title='Готово', content=Label(text='Кэш очищен!'), size_hint=(0.6, 0.3))
        popup.open()
        self.on_enter()

    def on_enter(self):
        self.clear_widgets()
        l = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        top = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        top.add_widget(Button(text='←', size_hint_x=None, width=50, background_color=DARK, on_press=lambda x: setattr(self.manager, 'current', 'chats')))
        top.add_widget(Label(text='Настройки', font_size=22, color=PURPLE))
        l.add_widget(top)
        
        # Звёзды и премиум
        res = API.request('check_token.php', data={'token': App.get_running_app().token})
        if res.get('valid'):
            u = res['user']
            l.add_widget(Label(text=f"⭐ Звёзды: {u.get('stars_balance', 0)}", font_size=18, color=GOLD, size_hint_y=None, height=40))
            premium = 'Да ✅' if u.get('has_premium') else 'Нет'
            l.add_widget(Label(text=f"👑 Премиум: {premium}", font_size=18, color=GOLD, size_hint_y=None, height=40))
        
        # Кэш
        cache_size = self.get_cache_size()
        l.add_widget(Label(text=f"📦 Кэш: {cache_size}", color=WHITE, size_hint_y=None, height=40))
        l.add_widget(Button(text='🗑️ Очистить кэш', size_hint_y=None, height=50, background_color=DARK, on_press=self.clear_cache))
        
        self.add_widget(l)
