from kivy.utils import get_color_from_hex
import os

API_URL = "https://mashinistgrammsg.atwebpages.com/api/mg"

PURPLE = get_color_from_hex('#B659FF')
GOLD = get_color_from_hex('#FFD700')
DARK = get_color_from_hex('#2A2A3E')
DARKER = get_color_from_hex('#1E1E2E')
WHITE = (1, 1, 1, 1)
BG = get_color_from_hex('#1A1A2E')
MSG_MINE = get_color_from_hex('#3A1A5E')
MSG_THEIR = get_color_from_hex('#2A2A3E')

def icon(name):
    # Ищем иконки в папке icons рядом с main.py
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, 'icons', name)
