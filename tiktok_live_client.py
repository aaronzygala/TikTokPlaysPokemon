# tiktok_live_client.py
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent, GiftEvent
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

    def __init__(self, unique_id, key_press_queue, MODE):
        self.client = TikTokLiveClient(
            unique_id,
            # ws_ping_interval=30.0,  # Increase the interval between keepalive pings
            # ws_timeout=20.0,  # Increase the websocket timeout
            # http_timeout=20.0  # Increase the HTTP request timeout
        )
        self.key_press_queue = key_press_queue
        self.recent_comments = []# Store recent comments here
        self.client.on("connect")(self.on_connect)
        self.client.add_listener("comment", self.on_comment)
        self.client.on("gift")(self.on_gift)
        self.mode = MODE

    def run(self):
        self.client.run()

    def get_recent_comments(self):
        return self.recent_comments

    async def on_connect(self, _: ConnectEvent):
        print("Connected to Room ID:", self.client.room_id)

    async def on_comment(self, event: CommentEvent):
        print(f"{event.user.nickname}: {event.comment}")

        # Parse the comment and check for custom commands
        commands_triggered = [constants.command_to_key_mapping[command.lower()] for command in event.comment.split() if
                              command.lower() in constants.command_to_key_mapping]

        # if event.comment == "TOGGLE":
        #     self.toggle_mode()

        if len(commands_triggered) > 0:
            self.key_press_queue.put([commands_triggered[0]])
            # print("TESTING: ", event.user.avatar.urls[0])
            comment_data = {
                'avatar' : event.user.avatar.urls[0],
                'username': event.user.nickname,
                'comment': commands_triggered[0]
            }
            self.recent_comments.append(comment_data)  # Store the comment data

    async def on_gift(self, event: GiftEvent):
        print(f"{event.user.nickname} sent \"{event.gift.info.name}\"")
        if "Game Controller" in event.gift.info.name:
            print("TOGGLING GAME MODE")
            self.toggle_mode()
            print(f"Game mode is now: {self.mode[0]}")

        if "Enjoy Music" in event.gift.info.name:
            print("PLAYING ANIME THEME SONG...")

        if "Rose" in event.gift.info.name:
            print("RANDOMIZING BUDDY...")


    def toggle_mode(self):
        if self.mode[0] == "ORDER":
            self.mode[0] = "CHAOS"
        else:
            self.mode[0] = "ORDER"
