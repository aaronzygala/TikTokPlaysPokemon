# key_press_simulator.py
import pydirectinput
import threading
import time
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
    def __init__(self, emulator_window_title, key_press_queue, sound_request_queue, MODE):
        # Find the emulator window using partial title match
        emulator_windows = gw.getWindowsWithTitle(emulator_window_title)
        self.emulator_window = emulator_windows[0] if emulator_windows else None
        if self.emulator_window:
            self.emulator_window.activate()  # Activating the window
        else:
            print("Emulator window not found.")

        tiktok_live_studio_windows = gw.getWindowsWithTitle("TikTok")
        self.tiktok_live_studio_window = tiktok_live_studio_windows[0]
        self.tiktok_focus_timer = constants.TIKTOK_FOCUS_TIMER # number of minutes to focus the window and press spacebar

        self.key_press_queue = key_press_queue
        self.sound_request_queue = sound_request_queue
        self.votes = {}
        self.vote_interval = constants.VOTE_INTERVAL
        self.last_vote_time = time.time()
        self.key_press_thread = threading.Thread(target=self.simulate_key_presses)
        self.focus_tiktok_studio_thread = threading.Thread(target=self.focus_tiktok_with_timer)
        self.sound_request_thread = threading.Thread(target=self.process_sound_requests)
        self.mode = MODE

    def focus_tiktok_with_timer(self):
        while True:
            # If the window is found, focus it and press the spacebar
            self.tiktok_live_studio_window.activate()
            pydirectinput.press('space')

            time.sleep(self.tiktok_focus_timer * 60)  # Sleep for 30 minutes

    def start(self):
        self.key_press_thread.start()
        self.focus_tiktok_studio_thread.start()
        self.sound_request_thread.start()  # Start the sound request processing thread

    def stop(self):
        self.key_press_queue.put(None)
        self.sound_request_queue.put(None)
        self.key_press_thread.join()
        self.focus_tiktok_studio_thread.join()
        self.sound_request_thread.join()

    def simulate_key_presses(self):
        while True:
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
                    self.votes.clear()
                    self.last_vote_time = current_time  # Update last_vote_time after performing vote
                else:
                    self.collect_vote(commands_to_press)

    def press(self, command):
        self.emulator_window.activate()  # Activating the window
        print("Command registered: ", command)
        pydirectinput.press(command, interval=0.2)

    def collect_vote(self, command):
        if command[0] in self.votes:
            self.votes[command[0]] += 1
        else:
            self.votes[command[0]] = 1

    def process_sound_requests(self):
        while True:
            request = self.sound_request_queue.get()
            if request == "theme_song":
                self.mute()
                # Play the sound
                playsound(constants.THEME_SONG)
                # Wait for the sound to finish playing
                time.sleep(constants.THEME_SONG_DURATION_SECONDS)
                self.unmute()
            # Add more conditions for handling other sound requests

    def mute(self):
        if self.emulator_window:
            self.emulator_window.activate()  # Activate the emulator window
            pydirectinput.press(constants.MUTE_INPUT)  # Simulate pressing the mute key

    def unmute(self):
        if self.emulator_window:
            self.emulator_window.activate()  # Activate the emulator window
            pydirectinput.press(constants.UNMUTE_INPUT)  # Simulate pressing the unmute key
