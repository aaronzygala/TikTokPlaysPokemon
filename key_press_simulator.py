# key_press_simulator.py
import pyautogui
import threading
import time


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
    def __init__(self, key_press_queue, batch_interval=0.5):
        self.key_press_queue = key_press_queue
        self.batch_interval = batch_interval
        self.batch_commands = []
        self.last_batch_time = time.time()
        self.thread = threading.Thread(target=self.simulate_key_presses)

    def start(self):
        self.thread.start()

    def stop(self):
        self.key_press_queue.put(None)
        self.thread.join()

    def simulate_key_presses(self):
        while True:
            commands_to_press = self.key_press_queue.get()
            if commands_to_press is None:
                break

            self.batch_commands.extend(commands_to_press)
            current_time = time.time()
            if current_time - self.last_batch_time >= self.batch_interval:
                if self.batch_commands:
                    self.press_batch(self.batch_commands)
                    self.batch_commands = []
                    self.last_batch_time = current_time

    def press_batch(self, commands):
        for command in commands:
            pyautogui.press(command, interval=0.2)
