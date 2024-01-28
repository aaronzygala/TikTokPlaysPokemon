# main.py
from queue import Queue
import constants
from tiktok_live_client import TikTokLiveManager
from key_press_simulator import KeyPressSimulator


def main():
    key_press_queue = Queue()
    sound_request_queue = Queue()
    MODE = [constants.DEFAULT_MODE]

    live_manager = TikTokLiveManager(key_press_queue, sound_request_queue, MODE)
    key_press_simulator = KeyPressSimulator(key_press_queue, sound_request_queue, MODE)

    try:
        key_press_simulator.start()
        live_manager.run()

    finally:
        key_press_simulator.stop()
        live_manager.stop()

if __name__ == '__main__':
    main()

