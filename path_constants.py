import os


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
