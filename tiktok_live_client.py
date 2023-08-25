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

    def __init__(self, unique_id, key_press_queue, sound_request_queue, MODE):
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
        self.client.add_listener("gift", self.on_gift)
        self.mode = MODE
        self.init_images()
        self.admin_list = self.read_lines(constants.ADMIN_PATH)
        self.whitelist = self.read_lines(constants.WHITELIST_PATH)
        self.ban_votes_per_user = {}
        self.banned_list = self.read_lines(constants.BANNED_PATH)
        self.sound_request_queue = sound_request_queue
        self.processed_gifts = set()  # Track processed gifts

    def init_images(self):
        chaos_image = Image.open(constants.CHAOS_IMAGE)
        chaos_image.save(constants.CURRENT_MODE_IMAGE)
        chaos_image.close()

        buddy_image = Image.open(constants.DEFAULT_BUDDY_IMAGE)
        buddy_image.save(constants.CURRENT_BUDDY_IMAGE)
        buddy_image.close()

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

        if event.comment is None:
            return  # Ignore comments with None content

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
                commands_triggered = [constants.command_to_key_mapping[command.lower()] for command in event.comment.split()
                                      if command.lower() in constants.command_to_key_mapping]

                if len(commands_triggered) > 0:
                    self.key_press_queue.put([commands_triggered[0]])
                    comment_data = {
                        'avatar': event.user.avatar.urls[0],
                        'username': event.user.unique_id,
                        'comment': commands_triggered[0]
                    }
                    self.recent_comments.append(comment_data)  # Store the comment data

    def add_to_file(self, file_path, string_to_add):
        with open(file_path, "a") as whitelist_file:
            whitelist_file.write(string_to_add + "\n")

    def rewrite_file(self, file_path, rewrite_list):
        with open(file_path, "w") as whitelist_file:
            for string in rewrite_list:
                whitelist_file.write(string + "\n")
    def whitelist_user(self, username):
        print("WHITELISTING A USER: " + username)
        self.whitelist.append(username)
        self.add_to_file(constants.WHITELIST_PATH, username)

    def remove_from_whitelist(self, username):
        print("REMOVING A USER FROM WHITELIST: " + username)
        self.whitelist.remove(username)
        self.rewrite_file(constants.WHITELIST_PATH, self.whitelist)

    def ban_user(self, username_to_ban, username_of_caller):
        if username_to_ban in self.admin_list:
            return

        print("BANNING A USER: " + username_to_ban)
        if username_of_caller in self.admin_list:
            if username_to_ban in self.whitelist:
                self.whitelist.remove(username_to_ban)
                self.rewrite_file(constants.WHITELIST_PATH, self.whitelist)
            self.banned_list.append(username_to_ban)
            self.add_to_file(constants.BANNED_PATH, username_to_ban)
        elif username_of_caller in self.whitelist:
            if username_to_ban in self.whitelist:
                print("Whitelisted users are not allowed to ban other whitelisted users.")
            else:
                self.add_ban_vote(username_to_ban)
                vote_count = self.get_ban_vote_count(username_to_ban)
                if vote_count >= constants.VOTE_BAN_MINIMUM:
                    self.banned_list.append(username_to_ban)
                    self.add_to_file(constants.BANNED_PATH, username_to_ban)
                    del self.ban_votes_per_user[username_to_ban]
                else:
                    print(f"{constants.VOTE_BAN_MINIMUM - vote_count} more votes are needed to ban {username_to_ban}.")
        else:
            print("Only admins or whitelisted users are allowed to ban users.")

    def get_ban_vote_count(self, username):
        return self.ban_votes_per_user[username]

    def add_ban_vote(self, username):
        if username in self.ban_votes_per_user:
            self.ban_votes_per_user[username] += 1
        else:
            self.ban_votes_per_user[username] = 1

    async def on_gift(self, event: GiftEvent):
        if event.gift.id in self.processed_gifts:
            return
        print(f"{event.user.nickname} sent \"{event.gift.info.name}\"")
        if "Pizza" in event.gift.info.name:
            self.toggle_mode()

        if "Enjoy Music" in event.gift.info.name:
            self.play_theme_song()

        if "Rose" in event.gift.info.name:
            self.randomize_buddy()

        self.processed_gifts.add(event.gift.id)

    def toggle_mode(self):
        print("TOGGLING GAME MODE...")
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
        new_buddy_file = random.choice(os.listdir(constants.POKEMON_DIRECTORY))
        print("new_buddy_file: " + new_buddy_file)
        new_buddy_image = Image.open(os.path.join(constants.POKEMON_DIRECTORY, new_buddy_file))
        new_buddy_image.save(constants.CURRENT_BUDDY_IMAGE)
        new_buddy_image.close()

    def play_theme_song(self):
        print("PLAYING ANIME THEME SONG...")
        self.sound_request_queue.put("theme_song")
