# main.py
import pygetwindow as gw
import tiktok_live_client
import key_press_simulator
import constants


def main():
    # Find the emulator window using partial title match
    emulator_windows = gw.getWindowsWithTitle("mGBA")
    emulator_window = emulator_windows[0] if emulator_windows else None

    # Create a queue for key press batching
    key_press_queue = queue.Queue()

    # Create instances of TikTokLiveManager and KeyPressSimulator
    live_manager = tiktok_live_client.TikTokLiveManager("@baz4k", key_press_queue)
    key_simulator = key_press_simulator.KeyPressSimulator(key_press_queue)

    if emulator_window:
        emulator_window.activate()  # Activating the window
    else:
        print("Emulator window not found.")

    try:
        # Start the key press simulator thread
        key_simulator.start()

        # Run the TikTokLiveManager
        live_manager.run()

    finally:
        # Stop the key press simulator thread
        key_simulator.stop()


if __name__ == '__main__':
    main()
