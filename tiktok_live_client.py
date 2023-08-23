# tiktok_live_client.py
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent, GiftEvent
from PIL import Image
import constants
import os
import random

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
        self.recent_comments = []
        self.client.on("connect")(self.on_connect)
        self.client.add_listener("comment", self.on_comment)
        self.client.on("gift")(self.on_gift)
        self.mode = MODE
        self.admin_list = self.read_lines(constants.ADMIN_PATH)
        self.whitelist = self.read_lines(constants.WHITELIST_PATH)
        self.banned_list = self.read_lines(constants.BANNED_PATH)

    def read_lines(self, filename):
        with open(filename) as file:
            return file.read().splitlines()

    def run(self):
        self.client.run()

    def get_recent_comments(self):
        return self.recent_comments

    async def on_connect(self, _: ConnectEvent):
        print("Connected to Room ID:", self.client.room_id)

    async def on_comment(self, event: CommentEvent):
        print(f"{event.user.nickname}: {event.comment}")

        # if event.comment == "TEST_BUDDY":
        #     self.randomize_buddy()
        #
        # if event.comment == "TEST_MODE":
        #     self.toggle_mode()

        # Check if the comment is a whitelisting command and user is in admin_list
        if event.comment.startswith("!whitelist") and event.user.unique_id in self.admin_list:
            parts = event.comment.split()
            if len(parts) == 2 and parts[0] == "!whitelist" and parts[1] not in self.whitelist:
                username_to_whitelist = parts[1]
                print("WHITELISTING A USER: " + username_to_whitelist)
                with open(constants.WHITELIST_PATH, "a") as whitelist_file:
                    self.whitelist.append(username_to_whitelist)
                    whitelist_file.write(username_to_whitelist + "\n")
        elif event.comment.startswith("!remove_whitelist") and event.user.unique_id in self.admin_list:
            parts = event.comment.split()
            if len(parts) == 2 and parts[0] == "!whitelist" and parts[1] not in self.whitelist:
                username_to_whitelist = parts[1]
                print("REMOVING A USER FROM WHITELIST: " + username_to_whitelist)
                self.whitelist.remove(username_to_whitelist)
                with open(constants.WHITELIST_PATH, "w") as whitelist_file:
                    for user in self.whitelist:
                        whitelist_file.write(user + "\n")
        elif event.comment.startswith("!ban") and event.user.unique_id in self.whitelist:
            parts = event.comment.split()
            if len(parts) == 2 and parts[0] == "!ban" and parts[1] not in self.banned_list:
                username_to_ban = parts[1]
                print("BANNING A USER: " + username_to_ban)
                if username_to_ban not in self.admin_list:
                    if username_to_ban in self.whitelist and event.user.unique_id in self.admin_list:
                        self.whitelist.remove(username_to_ban)
                        with open(constants.WHITELIST_PATH, "w") as whitelist_file:
                            for user in self.whitelist:
                                whitelist_file.write(user + "\n")
                    with open(constants.BANNED_PATH, "a") as banned_file:
                        self.banned_list.append(username_to_ban)
                        banned_file.write(username_to_ban + "\n")

        else:
            # Parse the comment and check for custom commands
            if event.user.unique_id not in self.banned_list:
                commands_triggered = [constants.command_to_key_mapping[command.lower()] for command in event.comment.split()
                                      if command.lower() in constants.command_to_key_mapping]

                # if event.comment == "NEW BUDDY":
                #     self.randomize_buddy()

                if len(commands_triggered) > 0:
                    self.key_press_queue.put([commands_triggered[0]])
                    comment_data = {
                        'avatar': event.user.avatar.urls[0],
                        'username': event.user.unique_id,
                        'comment': commands_triggered[0]
                    }
                    self.recent_comments.append(comment_data)  # Store the comment data

    async def on_gift(self, event: GiftEvent):
        print(f"{event.user.nickname} sent \"{event.gift.info.name}\"")
        if "Game Controller" in event.gift.info.name:
            self.toggle_mode()

        if "Enjoy Music" in event.gift.info.name:
            print("NOT IMPLEMENTED!!! TODO: PROGRAM ANIME THEME SONG...")

        if "Rose" in event.gift.info.name:
            self.randomize_buddy()

    def toggle_mode(self):
        print("TOGGLING GAME MODE")
        if self.mode[0] == "ORDER":
            self.mode[0] = "CHAOS"
            new_mode_file = constants.CHAOS_IMAGE
        else:
            self.mode[0] = "ORDER"
            new_mode_file = constants.ORDER_IMAGE

        new_mode_image = Image.open(new_mode_file)
        new_mode_image.save(constants.CURRENT_MODE_IMAGE)
        new_mode_image.close()
        print(f"Game mode is now: {self.mode[0]}")

    def randomize_buddy(self):
        print("RANDOMIZING BUDDY...")
        new_buddy_file = random.choice(os.listdir(constants.POKEMON_DIRECTORIES))
        print("new_buddy_file: " + new_buddy_file)
        new_buddy_image = Image.open(os.path.join(constants.POKEMON_DIRECTORIES, new_buddy_file))
        new_buddy_image.save(constants.CURRENT_BUDDY_IMAGE)
        new_buddy_image.close()