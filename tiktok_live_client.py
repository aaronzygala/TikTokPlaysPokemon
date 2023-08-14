# tiktok_live_client.py
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent
import constants


class TikTokLiveManager:
    """
    A class that manages TikTok Live interactions and processes comments for key presses.

    Args:
        unique_id (str): The unique identifier for the user.
        key_press_queue (Queue): A queue to send key press commands.

    Attributes:
        client (TikTokLiveClient): The TikTok Live client instance.
        key_press_queue (Queue): The queue for sending key press commands.

    Methods:
        run(): Start the TikTok Live interaction.
        on_connect(event): Callback for handling connection events.
        on_comment(event): Callback for handling comment events and sending key press commands.
    """

    def __init__(self, unique_id, key_press_queue):
        self.client = TikTokLiveClient(
            unique_id,
            # ws_ping_interval=30.0,  # Increase the interval between keepalive pings
            # ws_timeout=20.0,  # Increase the websocket timeout
            # http_timeout=20.0  # Increase the HTTP request timeout
        )
        self.key_press_queue = key_press_queue
        self.client.on("connect")(self.on_connect)
        self.client.add_listener("comment", self.on_comment)

    def run(self):
        self.client.run()

    async def on_connect(self, _: ConnectEvent):
        print("Connected to Room ID:", self.client.room_id)

    async def on_comment(self, event: CommentEvent):
        print(f"{event.user.nickname}: {event.comment}")

        # Parse the comment and check for custom commands
        commands_triggered = [constants.command_to_key_mapping[command] for command in event.comment.split() if
                              command in constants.command_to_key_mapping]

        if len(commands_triggered) > 0:
            self.key_press_queue.put(commands_triggered)
