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
    def __init__(self, key_press_queue, sound_request_queue, MODE):
        # Find the emulator window using partial title match
        self.emulator_window = self.find_and_activate_window(constants.EMULATOR_WINDOW)
        self.tiktok_live_studio_window = self.find_and_activate_window(constants.TIKTOK_LIVE_STUDIO_WINDOW)

        self.key_press_queue = key_press_queue
        self.sound_request_queue = sound_request_queue
        self.votes = {}
        self.vote_interval = constants.VOTE_INTERVAL
        self.last_vote_time = time.time()
        self.key_press_thread = threading.Thread(target=self.simulate_key_presses)
        self.exit_event = threading.Event()  # Event to signal the thread to exit

        self.focus_tiktok_studio_thread = threading.Thread(target=self.focus_tiktok_with_timer)
        self.sound_request_thread = threading.Thread(target=self.process_sound_requests)
        self.mode = MODE

        self.emulator_window_lock = threading.Lock()  # Create a lock for self.emulator_window
        self.votes_lock = threading.Lock()  # Create a lock for accessing self.votes

    def find_and_activate_window(self, window_title):
        try:
            windows = gw.getWindowsWithTitle(window_title)
            if windows:
                window = windows[0]
                window.activate()  # Activating the window
                return window
            else:
                print(f"{window_title} window not found.")
                return None
        except gw.PyGetWindowException as e:
            print(f"Error while activating {window_title} window: {e}")
            return None

    def focus_tiktok_with_timer(self):
        try:
            while True:
                if self.tiktok_live_studio_window:
                    self.tiktok_live_studio_window.activate()
                    pydirectinput.press('space')
                time.sleep(constants.TIKTOK_FOCUS_TIMER * 60)
        except gw.PyGetWindowException as e:
            print("An exception occurred:", e)
            pass  # Continue execution

    def start(self):
        self.key_press_thread.start()
        self.focus_tiktok_studio_thread.start()
        self.sound_request_thread.start()  # Start the sound request processing thread

    def stop(self):
        self.exit_event.set()
        self.key_press_queue.put(None)
        self.sound_request_queue.put(None)
        self.key_press_thread.join()
        self.focus_tiktok_studio_thread.join()
        self.sound_request_thread.join()

    def simulate_key_presses(self):
        while not self.exit_event.is_set():
            commands_to_press = self.key_press_queue.get()
            if commands_to_press is None:
                continue

            if self.mode[0] == "CHAOS":
                self.press(commands_to_press)
            else:
                current_time = time.time()
                if (len(self.votes) > 0) and (current_time - self.last_vote_time >= self.vote_interval):
                    print("VOTES: ")
                    print(self.votes)
                    most_common_command = max(self.votes, key=self.votes.get)
                    self.press([most_common_command])
                    with self.votes_lock:
                        self.votes.clear()
                    self.last_vote_time = current_time  # Update last_vote_time after performing vote
                else:
                    self.collect_vote(commands_to_press)

    def press(self, command):
        try:
            with self.emulator_window_lock:
                self.emulator_window.activate()  # Activating the window
                print("Command registered: ", command)
                pydirectinput.press(command, interval=0.2)
        except gw.PyGetWindowException as e:
            print(f"Error while activating {window_title} window: {e}")
            pass

    def collect_vote(self, command):
        with self.votes_lock:
            if command[0] in self.votes:
                self.votes[command[0]] += 1
            else:
                self.votes[command[0]] = 1

    def process_sound_requests(self):
        while not self.exit_event.is_set():
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
        self.press(constants.TOGGLE_MUTE_INPUT)  # Simulate pressing the mute key