# main.py
from queue import Queue
from tiktok_live_client import TikTokLiveManager
from key_press_simulator import KeyPressSimulator
import subprocess
import time

key_press_queue = Queue()
sound_request_queue = Queue()
live_manager = TikTokLiveManager(key_press_queue, sound_request_queue)
key_press_simulator = KeyPressSimulator(key_press_queue, sound_request_queue)

def main():
    try:
        print("Before key_press_simulator.start()")
        #key_press_simulator.start()
        print("After key_press_simulator.start()")

        print("Before live_manager.start()")
        live_manager.run()
        print("After live_manager.start()")


    finally:
        key_press_simulator.stop()
        live_manager.stop()

def restart_program():
    print("Stopping the program...")
    live_manager.stop()
    key_press_simulator.stop()
    time.sleep(2)  # Allow time for cleanup if needed
    print("Restarting the program...")
    subprocess.run(["python", "main.py"])

if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print(f"An error occurred: {e}")

        print("Waiting for 10 minutes before restarting...")
        time.sleep(10 * 60)  # 10 minutes
        restart_program()

