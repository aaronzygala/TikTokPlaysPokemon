# key_press_simulator.py
import pydirectinput
import threading
import time
import path_constants
import constants
import pygetwindow as gw
from playsound import playsound


class KeyPressSimulator:
    """
    A class that simulates batched key presses based on commands from a queue.
    It provides the ability to batch commands and simulate them as key presses
    with specified timing intervals.

    Args:
        key_press_queue (Queue): A queue to receive key press commands.
        batch_interval (float): Time interval for batching commands before simulation.

    Attributes:
        key_press_queue (Queue): The queue for receiving key press commands.
        batch_interval (float): The time interval for batching commands.
        batch_commands (list): List to hold commands for the current batch.
        last_batch_time (float): Time when the last batch was processed.
        thread (Thread): The simulation thread.

    Methods:
        start(): Start the key press simulation thread.
        stop(): Stop the key press simulation thread.
        simulate_key_presses(): Continuously process commands and simulate key presses.
        press_batch(commands): Simulate a batch of key presses.
    """

    def __init__(self, key_press_queue, sound_request_queue):
        print("Entering Key_press_simulator.__init__: ")

        self.initialized = True
        self.emulator_window = self.find_and_activate_window(constants.EMULATOR_WINDOW)
        self.tiktok_live_studio_window = self.find_and_activate_window(constants.TIKTOK_LIVE_STUDIO_WINDOW)

        self.key_press_queue = key_press_queue
        self.sound_request_queue = sound_request_queue

        self.key_press_thread = threading.Thread(target=self.simulate_key_presses)

        self.focus_tiktok_studio_thread = threading.Thread(target=self.focus_tiktok_with_timer)
        self.sound_request_thread = threading.Thread(target=self.process_sound_requests)

        self.emulator_window_lock = threading.Lock()  # Create a lock for self.emulator_window

    def find_and_activate_window(self, window_title):
        print("Entering Key_press_simulator.find_and_activate_window: ", window_title)
        windows = gw.getWindowsWithTitle(window_title)
        if windows:
            window = windows[0]
            try:
                window.activate()
            except gw.PyGetWindowException:
                # print(f"Error while activating {window_title} window: {e}")
                window.minimize()
                window.restore()
            return window
        else:
            print(f"{window_title} window not found.")
            return None

    def focus_tiktok_with_timer(self):
        print("Entering Key_press_simulator.focus_tiktok_timer thread: ")
        while True:
            if self.tiktok_live_studio_window:
                try:
                    self.tiktok_live_studio_window.activate()
                except gw.PyGetWindowException:
                    self.tiktok_live_studio_window.minimize()
                    self.tiktok_live_studio_window.restore()
                pydirectinput.press('space')
            time.sleep(constants.TIKTOK_FOCUS_TIMER * 60)

    def start(self):
        print("Entering Key_press_simulator.start : ")

        self.key_press_thread.start()
        self.focus_tiktok_studio_thread.start()
        self.sound_request_thread.start()  # Start the sound request processing thread

    def stop(self):
        print("Entering Key_press_simulator.stop : ")

        self.key_press_queue.put(None)
        self.sound_request_queue.put(None)
        self.key_press_thread.join()
        self.focus_tiktok_studio_thread.join()
        self.sound_request_thread.join()

    def simulate_key_presses(self):
        print("Entering Key_press_simulator.simulate_key_presses : ")

        while True:
            commands_to_press = self.key_press_queue.get()
            if commands_to_press is None:
                continue

            self.press(commands_to_press)

    def press(self, command):
        print("Entering Key_press_simulator.press : ")

        with self.emulator_window_lock:
            try:
                self.emulator_window.activate()
            except gw.PyGetWindowException:
                self.emulator_window.minimize()
                self.emulator_window.restore()
            print("Command registered: ", command)
            pydirectinput.press(command)

    def process_sound_requests(self):
        print("Entering Key_press_simulator.process_sound_requests : ")

        while True:
            request = self.sound_request_queue.get()
            if request is None:
                continue
            if request == "theme_song":
                print("PLAYING THEME SONG:")
                print("MUTING THE GAME...")
                self.toggle_mute()
                # Play the sound
                playsound(path_constants.THEME_SONG)
                print("THEME SONG COMPLETE")

                # Wait for the sound to finish playing
                time.sleep(constants.THEME_SONG_DURATION_SECONDS)
                print("UN-MUTING THE GAME...")
                self.toggle_mute()
            # Add more conditions for handling other sound requests

    def toggle_mute(self):
        print("Entering Key_press_simulator.toggle_mute : ")

        self.press(constants.TOGGLE_MUTE_INPUT)  # Simulate pressing the mute key
