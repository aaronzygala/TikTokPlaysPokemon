# main.py
import tiktok_live_client
import key_press_simulator
import queue
import backend

def main():
    MODE = ["ORDER"]
    # Create a queue for key press batching
    key_press_queue = queue.Queue()
    # Create instances of TikTokLiveManager and KeyPressSimulator
    live_manager = tiktok_live_client.TikTokLiveManager("@baz4k", key_press_queue, MODE=MODE)
    key_simulator = key_press_simulator.KeyPressSimulator("mGBA", key_press_queue, MODE=MODE)
    # Pass the live_manager to the backend
    backend.live_manager = live_manager
    try:
        # Start the key press simulator thread
        key_simulator.start()

        # Run the TikTokLiveManager
        live_manager.run()

    finally:
    #     # Stop the key press simulator thread
        key_simulator.stop()


if __name__ == '__main__':
    backend.run_flask_thread()
    main()
