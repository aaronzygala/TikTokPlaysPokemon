# singleton_instances.py

from tiktok_live_client import TikTokLiveManager  # Import your TikTokLiveManager class
from key_press_simulator import KeyPressSimulator
from queue import Queue  # Import Queue (or any other queue implementation you are using)
import constants

# Initialize the live_manager instance
key_press_queue = Queue()
sound_request_queue = Queue()
MODE = [constants.DEFAULT_MODE]  # Your MODE initialization

live_manager = TikTokLiveManager(key_press_queue, sound_request_queue, MODE)
key_press_simulator = KeyPressSimulator(key_press_queue, sound_request_queue, MODE)

# Function to get the live_manager instance
def get_live_manager():
    return live_manager

def get_key_press_simulator():
    return key_press_simulator