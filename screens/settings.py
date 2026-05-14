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
        c = BoxLayout(orientation='vertical', padding=20, spacing=15)
        c.add_widget(Image(source=icon('star.png'), size=(60, 60), pos_hint={'center_x': 0.5}))
        c.add_widget(Label(text=f'Ваш баланс: {balance} ⭐', font_size=22, color=GOLD, halign='center'))
        Popup(title='Звёзды', content=c, size_hint=(0.65, 0.4)).open()

    def premium_popup(self):
        res = API.request('check_token.php', data={'token': App.get_running_app().token})
        has = res['user'].get('has_premium', False) if res.get('valid') else False
        c = BoxLayout(orientation='vertical', padding=20, spacing=15)
        c.add_widget(Image(source=icon('premium_star.png'), size=(60, 60), pos_hint={'center_x': 0.5}))
        c.add_widget(Label(text=f'Премиум: {"Активен ✅" if has else "Не активен"}', font_size=20, color=PURPLE, halign='center'))
        c.add_widget(Label(text='Функции:\n• Звёздочка у ника\n• Жирный фиолетовый ник', color=WHITE, halign='center'))
        Popup(title='Премиум', content=c, size_hint=(0.7, 0.5)).open()

    def sponsor_popup(self):
        res = API.request('check_token.php', data={'token': App.get_running_app().token})
        cnt = res['user'].get('sponsor_count', 0) if res.get('valid') else 0
        levels = {1:'Спонсор (1 уровень)',2:'Хороший спонсор (2 уровень)',3:'Особый спонсор (3 уровень)',4:'Супер спонсор (4 уровень)'}
        title = levels.get(cnt, f'УЛЬТРА СПОНСОР (5+ уровень)') if cnt > 0 else 'Нет спонсорства'
        c = BoxLayout(orientation='vertical', padding=20, spacing=15)
        c.add_widget(Label(text='💎', font_size=50, halign='center'))
        c.add_widget(Label(text=title, color=WHITE, halign='center'))
        Popup(title='Спонсор', content=c, size_hint=(0.7, 0.4)).open()

    def verified_popup(self):
        res = API.request('check_token.php', data={'token': App.get_running_app().token})
        u = res.get('user', {})
        if u.get('is_creator'):
            text = 'Это создатель этого мессенджера 👑'
        elif u.get('verified'):
            text = 'Это верифицированный аккаунт ✅'
        else:
            text = 'Ваш аккаунт не верифицирован'
        c = BoxLayout(orientation='vertical', padding=20, spacing=15)
        c.add_widget(Label(text='✅' if u.get('verified') or u.get('is_creator') else '❌', font_size=50, halign='center'))
        c.add_widget(Label(text=text, color=WHITE, halign='center'))
        Popup(title='Верификация', content=c, size_hint=(0.7, 0.4)).open()

    def get_cache_size(self):
        cache_dir = App.get_running_app().user_data_dir
        total = 0
        if os.path.exists(cache_dir):
            for root, dirs, files in os.walk(cache_dir):
                for f in files: total += os.path.getsize(os.path.join(root, f))
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
        
        res = API.request('check_token.php', data={'token': App.get_running_app().token})
        if res.get('valid'):
            u = res['user']
            l.add_widget(Label(text=f"ID аккаунта: {u['id']}", color=WHITE, size_hint_y=None, height=30))
        
        items = [('star.png', 'Звёзды', self.stars_popup), ('premium_star.png', 'Премиум', self.premium_popup), ('verify.png', 'Верификация', self.verified_popup), ('star.png', 'Спонсор', self.sponsor_popup)]
        for icon_name, text, func in items:
            row = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
            row.add_widget(Image(source=icon(icon_name), size=(35, 35)))
            lbl = Label(text=text, color=WHITE, halign='left', valign='middle')
            lbl.bind(size=lbl.setter('text_size'))
            row.add_widget(lbl)
            row.add_widget(Button(text='>', size_hint_x=None, width=50, background_color=(0,0,0,0), on_press=lambda x, f=func: f()))
            l.add_widget(row)
        
        l.add_widget(Label(text=f'Кэш: {self.get_cache_size()}', color=WHITE, size_hint_y=None, height=40))
        l.add_widget(Button(text='Очистить кэш', size_hint_y=None, height=50, background_color=DARK, on_press=self.clear_cache))
        self.add_widget(l)
