from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from config import BG

Window.clearcolor = BG

from screens.login import LoginScreen, RegisterScreen
from screens.chats import ChatsScreen
from screens.chat import ChatScreen
from screens.search import SearchScreen
from screens.profile import ProfileScreen

class MashinistGramApp(App):
    token = None
    user_id = None
    current_chat = None

    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(ChatsScreen(name='chats'))
        sm.add_widget(ChatScreen(name='chat'))
        sm.add_widget(SearchScreen(name='search'))
        sm.add_widget(ProfileScreen(name='profile'))
        return sm

if __name__ == '__main__':
    MashinistGramApp().run()
