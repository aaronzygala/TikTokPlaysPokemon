# constants.py
import os


command_to_key_mapping = {
    "up": 'up',
    "down": 'down',
    "left": 'left',
    "right": 'right',
    "aa": 'a',
    "bb": 'b',
    "select": 'o',
    "start": 'p',
}
# Number of whitelist votes needed to ban a user
VOTE_BAN_MINIMUM = 5

# The number of MINUTES for the timer to re-focus the TikTok Live Studio app
TIKTOK_FOCUS_TIMER = 30.0

# The default mode of the program
DEFAULT_MODE = "CHAOS"

# Number of seconds for each vote in Order mode
VOTE_INTERVAL = 10.0

# Number of seconds in theme song in SECONDS
THEME_SONG_DURATION_SECONDS = 197

# Inputs to mute/unmute
TOGGLE_MUTE_INPUT = 'y'

# PATH CONSTANTS - using absolute values
script_directory = os.path.dirname(os.path.abspath(__file__))
CHAOS_IMAGE = os.path.join(script_directory, "OBS_Files", "Chaos.png")
ORDER_IMAGE = os.path.join(script_directory, "OBS_Files", "Order.png")
CURRENT_MODE_IMAGE = os.path.join(script_directory, "OBS_Files", "CurrentMode.png")
CURRENT_BUDDY_IMAGE = os.path.join(script_directory, "OBS_Files", "CurrentBuddy.png")
POKEMON_DIRECTORY = os.path.join(script_directory, "assets", "Pokemon")
DEFAULT_BUDDY_IMAGE = os.path.join(POKEMON_DIRECTORY, "pikachu.png")
THEME_SONG = os.path.join(script_directory, "assets", "Pokemon.mp3")

WHITELIST_PATH = os.path.join(script_directory, "users", "whitelist.txt")
ADMIN_PATH = os.path.join(script_directory, "users", "admin.txt")
BANNED_PATH = os.path.join(script_directory, "users", "banned.txt")
