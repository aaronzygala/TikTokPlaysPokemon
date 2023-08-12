# key_press_simulator.py
import pyautogui
import threading
import time


class KeyPressSimulator:
    def __init__(self, key_press_queue, batch_interval=0.5):
        self.key_press_queue = key_press_queue
        self.batch_interval = batch_interval  # Time interval to collect commands before simulating
        self.batch_commands = []  # List to hold commands for the current batch
        self.last_batch_time = time.time()  # Record the last batch time
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
        pyautogui.typewrite(''.join(commands), interval=1.0)
