from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent
import pygetwindow as gw
import pyautogui  # Using pyautogui instead of pydirectinput
import time
import constants

# Instantiate the client with the user's username
client: TikTokLiveClient = TikTokLiveClient(unique_id="@baz4k")

# Dictionary to keep track of the last processed time for each command
last_processed_times = {command: 0 for command in constants.command_to_key_mapping}

# Find the emulator window using partial title match
emulator_windows = gw.getWindowsWithTitle("mGBA")

# Check if the window was found
if not emulator_windows:
    print("Emulator window not found.")

# Activate the first window found
emulator_window = emulator_windows[0]
emulator_window.activate()  # Activating the window

# Define how you want to handle specific events via decorator
@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Connected to Room ID:", client.room_id)

# Handle comment events
async def on_comment(event: CommentEvent):
    print(f"{event.user.nickname} -> {event.comment}")

    # Get the current time
    current_time = time.time()

    # Parse the comment and check for custom commands
    for command in command_to_key_mapping:
        if command in event.comment.lower():
            time.sleep(0.1)  # Adding a small delay

            # Check if enough time has passed since the last processed command
            if current_time - last_processed_times[command] > 2:
                # Press the corresponding key to the command using pyautogui
                pyautogui.press(command_to_key_mapping[command])

                print(f"{event.user.unique_id} sent \"{command}\", pressed key \"{command_to_key_mapping[command]}\"")

                # Update the last processed time for this command
                last_processed_times[command] = current_time

            else:
                print(f"Not enough time has passed since the last processed \"{command}\" command.")

client.add_listener("comment", on_comment)

if __name__ == '__main__':
    # Run the client and block the main thread
    client.run()
