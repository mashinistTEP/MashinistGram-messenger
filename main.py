from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from config import BG
import traceback
import os

Window.clearcolor = BG

def log_error(exc):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'crash.log')
    with open(path, 'a') as f:
        f.write(f"\n{'='*50}\n")
        traceback.print_exc(file=f)

from screens.login import LoginScreen, RegisterScreen
from screens.chats import ChatsScreen
from screens.chat import ChatScreen
from screens.search import SearchScreen
from screens.profile import ProfileScreen
from screens.settings import SettingsScreen

class MashinistGramApp(App):
    token = None
    user_id = None
    current_chat = None

    def build(self):
        try:
            self.store = JsonStore('session.json')
            if self.store.exists('user'):
                data = self.store.get('user')
                self.token = data.get('token')
                self.user_id = data.get('user_id')
            
            sm = ScreenManager()
            sm.add_widget(LoginScreen(name='login'))
            sm.add_widget(RegisterScreen(name='register'))
            sm.add_widget(ChatsScreen(name='chats'))
            sm.add_widget(ChatScreen(name='chat'))
            sm.add_widget(SearchScreen(name='search'))
            sm.add_widget(ProfileScreen(name='profile'))
            sm.add_widget(SettingsScreen(name='settings'))
            
            if self.token:
                from api import API
                res = API.request('check_token.php', data={'token': self.token})
                if res.get('valid'):
                    sm.current = 'chats'
                else:
                    self.token = None
                    self.user_id = None
                    self.store.delete('user')
            
            return sm
        except Exception as e:
            log_error(e)
            raise

    def save_session(self):
        if self.token:
            self.store.put('user', token=self.token, user_id=self.user_id)
