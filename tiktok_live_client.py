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

    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, key_press_queue, sound_request_queue, MODE):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.client = TikTokLiveClient(
                constants.TIKTOK_USERNAME,
                # ws_ping_interval=30.0,  # Increase the interval between keepalive pings
                # ws_timeout=20.0,  # Increase the websocket timeout
                # http_timeout=20.0  # Increase the HTTP request timeout
            )
            self.key_press_queue = key_press_queue
            self.recent_comments = deque()
            self.most_recent_comment = None
            self.client.add_listener("connect", self.on_connect)
            self.client.add_listener("comment", self.on_comment)
            self.client.add_listener("gift", self.on_gift)
            self.client.add_listener("follow", self.on_follow)

            self.mode = MODE
            self.init_images()
            self.admin_list = self.read_lines(path_constants.ADMIN_PATH)
            self.whitelist = self.read_lines(path_constants.WHITELIST_PATH)
            self.ban_votes_per_user = {}
            self.banned_list = self.read_lines(path_constants.BANNED_PATH)
            self.sound_request_queue = sound_request_queue
            self.processed_gifts = {}
            self.comment_count = 0
            self.follower_count = 0
            self.gift_count = 0

    def init_images(self):
        chaos_image = Image.open(path_constants.CHAOS_IMAGE)
        chaos_image.save(path_constants.CURRENT_MODE_IMAGE)
        chaos_image.close()

        buddy_image = Image.open(path_constants.DEFAULT_BUDDY_IMAGE)
        buddy_image.save(path_constants.CURRENT_BUDDY_IMAGE)
        buddy_image.close()

    def read_lines(self, filename):
        with open(filename) as file:
            return file.read().splitlines()

    def run(self):
        self.client.run()

    def stop(self):
        self.client.stop()

    def get_recent_comments(self):
        return self.recent_comments

    def get_most_recent_comment(self):
        if self.most_recent_comment is not None:
            return self.most_recent_comment
        else:
            return 0

    async def on_connect(self, _: ConnectEvent):
        print("Connected to Room ID:", self.client.room_id)

    async def on_comment(self, event: CommentEvent):
        print(f"{event.user.nickname}: {event.comment}")
        if event.comment is None:
            return  # Ignore comments with None content
        self.comment_count += 1

        # Check if the comment is a whitelisting command and user is in admin_list
        if event.comment.startswith("!whitelist") and event.user.unique_id in self.admin_list:
            parts = event.comment.split()
            if len(parts) == 2 and parts[0] == "!whitelist" and parts[1] not in self.whitelist:
                username_to_whitelist = parts[1]
                self.whitelist_user(username_to_whitelist)

        elif event.comment.startswith("!remove_whitelist") and event.user.unique_id in self.admin_list:
            parts = event.comment.split()
            if len(parts) == 2 and parts[0] == "!whitelist" and parts[1] not in self.whitelist:
                username_to_whitelist = parts[1]
                self.remove_from_whitelist(username_to_whitelist)

        elif event.comment.startswith("!ban") and event.user.unique_id in self.whitelist:
            parts = event.comment.split()
            if len(parts) == 2 and parts[0] == "!ban" and parts[1] not in self.banned_list:
                username_to_ban = parts[1]
                self.ban_user(username_to_ban, event.user.unique_id)
        else:
            # Parse the comment and check for custom commands
            if event.user.unique_id in self.admin_list:
                if event.comment == "CHANGE_BUDDY":
                    self.randomize_buddy()

                if event.comment == "CHANGE_MODE":
                    self.toggle_mode()

                if event.comment == "START_SONG":
                    self.play_theme_song()

            if event.user.unique_id not in self.banned_list:
                commands_triggered = [command for command in event.comment.split()
                                      if command.lower() in constants.command_to_key_mapping]

                keys_to_trigger = [constants.command_to_key_mapping[command.lower()] for command in commands_triggered]

                if len(commands_triggered) > 0:
                    self.key_press_queue.put([keys_to_trigger[0]])
                    comment_data = {
                        'avatar': event.user.avatar.urls[0],
                        'username': event.user.unique_id,
                        'comment': commands_triggered[0].capitalize(),
                        'timestamp': time.time()
                    }
                    self.recent_comments.appendleft(comment_data)  # Store the comment data
                    self.most_recent_comment = comment_data

    def add_to_file(self, file_path, string_to_add):
        with open(file_path, "a") as whitelist_file:
            whitelist_file.write(string_to_add + "\n")

    def rewrite_file(self, file_path, rewrite_list):
        with open(file_path, "w") as whitelist_file:
            for string in rewrite_list:
                whitelist_file.write(string + "\n")

    def admin_user(self, username):
        print("ADMINNING A USER: " + username)
        self.admin_list.append(username)
        self.add_to_file(path_constants.ADMIN_PATH, username)

    def remove_from_admin(self, username):
        print("REMOVING A USER FROM ADMINS: " + username)
        self.admin_list.remove(username)
        self.rewrite_file(path_constants.ADMIN_PATH, self.admin_list)
    def whitelist_user(self, username):
        print("WHITELISTING A USER: " + username)
        self.whitelist.append(username)
        self.add_to_file(path_constants.WHITELIST_PATH, username)

    def remove_from_whitelist(self, username):
        print("REMOVING A USER FROM WHITELIST: " + username)
        self.whitelist.remove(username)
        self.rewrite_file(path_constants.WHITELIST_PATH, self.whitelist)

    def ban_user(self, username_to_ban, username_of_caller):
        if username_to_ban in self.admin_list:
            return

        print("BANNING A USER: " + username_to_ban)
        if username_of_caller in self.admin_list:
            if username_to_ban in self.whitelist:
                self.whitelist.remove(username_to_ban)
                self.rewrite_file(path_constants.WHITELIST_PATH, self.whitelist)
            self.banned_list.append(username_to_ban)
            self.add_to_file(path_constants.BANNED_PATH, username_to_ban)
        elif username_of_caller in self.whitelist:
            if username_to_ban in self.whitelist:
                print("Whitelisted users are not allowed to ban other whitelisted users.")
            else:
                self.add_ban_vote(username_to_ban)
                vote_count = self.get_ban_vote_count(username_to_ban)
                if vote_count >= path_constants.VOTE_BAN_MINIMUM:
                    self.banned_list.append(username_to_ban)
                    self.add_to_file(path_constants.BANNED_PATH, username_to_ban)
                    del self.ban_votes_per_user[username_to_ban]
                else:
                    print(f"{constants.VOTE_BAN_MINIMUM - vote_count} more votes are needed to ban {username_to_ban}.")
        else:
            print("Only admins or whitelisted users are allowed to ban users.")

    def remove_from_banned_list(self, username):
        print("REMOVING A USER FROM BANNED LIST: " + username)
        self.banned_list.remove(username)
        self.rewrite_file(path_constants.BANNED_PATH, self.banned_list)

    def get_ban_vote_count(self, username):
        return self.ban_votes_per_user[username]

    def add_ban_vote(self, username):
        if username in self.ban_votes_per_user:
            self.ban_votes_per_user[username] += 1
        else:
            self.ban_votes_per_user[username] = 1

    async def on_gift(self, event: GiftEvent):
        self.gift_count += 1
        unique_identifier = self.create_unique_identifier(event)
        current_time = time.time()

        if unique_identifier in self.processed_gifts:
            if current_time - self.processed_gifts[unique_identifier] <= 5:
                return
        print(f"{event.user.nickname} sent \"{event.gift.info.name}\"")

        if constants.ORDER_MODE_GIFT in event.gift.info.name and constants.ORDER_MODE_AVAILABLE:
            self.toggle_mode()

        if constants.THEME_SONG_GIFT in event.gift.info.name and constants.THEME_SONG_AVAILABLE:
            self.play_theme_song()

        if constants.BUDDY_GIFT in event.gift.info.name and constants.BUDDY_AVAILABLE:
            self.randomize_buddy()

        self.processed_gifts[unique_identifier] = current_time

    def create_unique_identifier(self, event: GiftEvent):
        # Combine attributes to create a unique identifier
        identifier = f"{event.user.unique_id}_{event.gift.id}"
        return identifier

    def cleanup_old_gifts(self, current_time):
        # Remove expired entries from the processed_gifts dictionary
        valid_window = 5  # 5 seconds
        expired_gifts = {
            identifier: timestamp for identifier, timestamp in self.processed_gifts.items()
            if current_time - timestamp > valid_window
        }
        for identifier in expired_gifts:
            del self.processed_gifts[identifier]

    def toggle_mode(self):
        print("TOGGLING GAME MODE...")
        if self.mode[0] == "ORDER":
            self.mode[0] = "CHAOS"
            new_mode_file = path_constants.CHAOS_IMAGE
        else:
            self.mode[0] = "ORDER"
            new_mode_file = path_constants.ORDER_IMAGE

        new_mode_image = Image.open(new_mode_file)
        new_mode_image.save(path_constants.CURRENT_MODE_IMAGE)
        new_mode_image.close()
        print(f"Game mode is now: {self.mode[0]}")
        return self.mode[0]

    def randomize_buddy(self):
        print("RANDOMIZING BUDDY...")
        new_buddy_file = random.choice(os.listdir(path_constants.POKEMON_DIRECTORY))
        print("new_buddy_file: " + new_buddy_file)
        new_buddy_image = Image.open(os.path.join(path_constants.POKEMON_DIRECTORY, new_buddy_file))
        new_buddy_image.save(path_constants.CURRENT_BUDDY_IMAGE)
        new_buddy_image.close()

    def play_theme_song(self):
        print("PLAYING ANIME THEME SONG...")
        self.sound_request_queue.put("theme_song")

    def get_comment_count(self):
        return self.comment_count
    def get_gift_count(self):
        return self.gift_count

    async def on_follow(self, event: FollowEvent):
        print(f"@{event.user.unique_id} followed you!")
        self.follower_count += 1

    def get_follow_count(self):
        return self.follower_count

    def get_mode(self):
        return self.mode[0]


