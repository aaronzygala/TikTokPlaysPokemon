# tiktok_live_client.py
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent, GiftEvent, ViewerUpdateEvent, FollowEvent
from PIL import Image
import constants
import path_constants
import os
import random
import time
from collections import deque


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

    def __init__(self, key_press_queue, sound_request_queue):
        print("Entering TikTokManager.__init__: ")

        self.client = TikTokLiveClient(
            constants.TIKTOK_USERNAME,
            # ws_ping_interval=30.0,  # Increase the interval between keepalive pings
            # ws_timeout=20.0,  # Increase the websocket timeout
            # http_timeout=20.0  # Increase the HTTP request timeout
        )
        self.key_press_queue = key_press_queue
        self.client.add_listener("connect", self.on_connect)
        self.client.add_listener("comment", self.on_comment)
        self.client.add_listener("gift", self.on_gift)

        self.init_images()
        self.admin_list = self.read_lines(path_constants.ADMIN_PATH)
        self.ban_votes_per_user = {}
        self.banned_list = self.read_lines(path_constants.BANNED_PATH)
        self.sound_request_queue = sound_request_queue
        self.processed_gifts = {}

    def read_lines(self, filename):
        print("Entering TikTokManager.read_lines: ")

        with open(filename) as file:
            return file.read().splitlines()

    def run(self):
        print("Entering TikTokManager.run: ")

        self.client.run()

    def stop(self):
        print("Entering TikTokManager.stop: ")

        self.client.stop()

    async def on_connect(self, _: ConnectEvent):
        print("Entering TikTokManager.on_connect: ")

        print("Connected to Room ID:", self.client.room_id)

    async def on_comment(self, event: CommentEvent):
        print("Entering TikTokManager.on_comment: ")

        print(f"{event.user.nickname}: {event.comment}")
        if event.comment is None:
            return  # Ignore comments with None content
        self.comment_count += 1

        if event.comment.startswith("!ban") and event.user.unique_id in self.admin_list:
            parts = event.comment.split()
            if len(parts) == 2 and parts[0] == "!ban" and parts[1] not in self.banned_list:
                username_to_ban = parts[1]
                self.ban_user(username_to_ban, event.user.unique_id)
        else:
            # Parse the comment and check for custom commands
            if event.user.unique_id in self.admin_list:
                if event.comment == "CHANGE_BUDDY":
                    self.randomize_buddy()

                if event.comment == "START_SONG":
                    self.play_theme_song()

            if event.user.unique_id not in self.banned_list:
                commands_triggered = [command for command in event.comment.split()
                                      if command.lower() in constants.command_to_key_mapping]

                keys_to_trigger = [constants.command_to_key_mapping[command.lower()] for command in commands_triggered]

                if len(commands_triggered) > 0:
                    self.key_press_queue.put([keys_to_trigger[0]])

    def add_to_file(self, file_path, string_to_add):
        print("Entering TikTokManager.add_to_file: ")

        with open(file_path, "a") as whitelist_file:
            whitelist_file.write(string_to_add + "\n")

    def rewrite_file(self, file_path, rewrite_list):
        print("Entering TikTokManager.rewrite_file: ")

        with open(file_path, "w") as whitelist_file:
            for string in rewrite_list:
                whitelist_file.write(string + "\n")

    def ban_user(self, username_to_ban, username_of_caller):
        print("Entering TikTokManager.ban_user: ")

        if username_to_ban in self.admin_list:
            return

        print("BANNING A USER: " + username_to_ban)
        if username_of_caller in self.admin_list:
            self.banned_list.append(username_to_ban)
            self.add_to_file(path_constants.BANNED_PATH, username_to_ban)
        else:
            print("Only admins are allowed to ban users.")

    def remove_from_banned_list(self, username):
        print("Entering TikTokManager.remove_from_banned_list: ")

        print("REMOVING A USER FROM BANNED LIST: " + username)
        self.banned_list.remove(username)
        self.rewrite_file(path_constants.BANNED_PATH, self.banned_list)

    def get_ban_vote_count(self, username):
        print("Entering TikTokManager.get_ban_vote_count: ")

        return self.ban_votes_per_user[username]

    def add_ban_vote(self, username):
        print("Entering TikTokManager.add_ban_vote: ")

        if username in self.ban_votes_per_user:
            self.ban_votes_per_user[username] += 1
        else:
            self.ban_votes_per_user[username] = 1

    async def on_gift(self, event: GiftEvent):
        print("Entering TikTokManager.on_gift: ")

        self.gift_count += 1
        unique_identifier = self.create_unique_identifier(event)
        current_time = time.time()

        if unique_identifier in self.processed_gifts:
            if current_time - self.processed_gifts[unique_identifier] <= 5:
                return
        print(f"{event.user.nickname} sent \"{event.gift.info.name}\"")

        if constants.THEME_SONG_GIFT in event.gift.info.name and constants.THEME_SONG_AVAILABLE:
            self.play_theme_song()

        if constants.BUDDY_GIFT in event.gift.info.name and constants.BUDDY_AVAILABLE:
            self.randomize_buddy()

        self.processed_gifts[unique_identifier] = current_time

    def create_unique_identifier(self, event: GiftEvent):
        print("Entering TikTokManager.create_unique_identifier: ")

        # Combine attributes to create a unique identifier
        identifier = f"{event.user.unique_id}_{event.gift.id}"
        return identifier

    def randomize_buddy(self):
        print("Entering TikTokManager.randomize_buddy: ")

        print("RANDOMIZING BUDDY...")
        new_buddy_file = random.choice(os.listdir(path_constants.POKEMON_DIRECTORY))
        print("new_buddy_file: " + new_buddy_file)
        new_buddy_image = Image.open(os.path.join(path_constants.POKEMON_DIRECTORY, new_buddy_file))
        new_buddy_image.save(path_constants.CURRENT_BUDDY_IMAGE)
        new_buddy_image.close()

    def play_theme_song(self):
        print("Entering TikTokManager.play_theme_song: ")

        print("PLAYING ANIME THEME SONG...")
        self.sound_request_queue.put("theme_song")
