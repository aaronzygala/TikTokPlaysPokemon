# constants.py
import win32con

command_to_key_mapping = {'aa': ord('a'),
                          'bb': ord('b'),
                          'up': win32con.VK_UP,
                          'down': win32con.VK_DOWN,
                          'left': win32con.VK_LEFT,
                          'right': win32con.VK_RIGHT,
                          'll': ord('l'),
                          'rr': ord('r'),
                          'save': ord('s'),
                          'load': ord('l'),
                          'select': ord('o'),
                          'start': ord('p'),
                          }
EMULATOR_WINDOW = 'mGBA'
TIKTOK_LIVE_STUDIO_WINDOW = 'TikTok LIVE Studio'
TIKTOK_USERNAME = '@baz4k'
ORDER_MODE_AVAILABLE = True
THEME_SONG_AVAILABLE = True
BUDDY_AVAILABLE = True
ORDER_MODE_GIFT = 'Pizza'
THEME_SONG_GIFT = 'Enjoy Music'
BUDDY_GIFT = 'Rose'
VOTE_BAN_MINIMUM = 5
TIKTOK_FOCUS_TIMER = 30
TOGGLE_SCRIPT_TIMER = 30
DEFAULT_MODE = 'CHAOS'
VOTE_INTERVAL = 10
THEME_SONG_DURATION_SECONDS = 197
TOGGLE_MUTE_INPUT = 'y'
