import json
import random
import arcade
import arcade.gui
from arcade.experimental.uislider import UISlider
from modules import websocket_communication as websocket


class StartMenu:

    def __init__(self, game):
        self.game = game
        # Setting Initial Variables
        self.full_box = None
        self.background_box = None
        self.loading_text = None
        self.max_texts = None
        self.title = None

        # Setting _setup to True to indicate that the Game is in the Setup Menu
        self.game._setup = True

        # Creating UIManager, UIBoxLayout (VBox) and additional Sprites
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()
        self.additionals = arcade.SpriteList()

        # Load Json from settings.json
        self.settings_path = "./resources/settings.json"
        with open(self.settings_path) as json_file:
            self.game.settings_json = json.load(json_file)
        # Setting Game Values (MasterVolume, Music, Sound) to the according json values
        self.game.volume, self.game.music, self.game.sound = self.game.settings_json["master_volume"], \
            self.game.settings_json["music"], self.game.settings_json[
            "sound"]  # Fix that Later when loading a json to save settings

        # Setting Games Playsound Function as an alias of self.playsound
        self.game.play_sound = self.play_sound
        # Setting Default Style for UI Buttons etc.
        self.game.default_style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": (173, 227, 124),  # (110, 200, 137) arcade.color.AMARANTH_PINK
            "border_width": 2,
            "border_color": None,
            "bg_color": (43, 137, 137),

            # used if button is pressed
            "bg_color_pressed": arcade.color.EERIE_BLACK,
            "border_color_pressed": (173, 227, 124),  # also used when hovered
            "font_color_pressed": (173, 227, 124),
        }

    def play_sound(self, filename):
        """ Custom SoundPlaying Function. Takes Master Volume and Sound/Music Settings in account. """
        sound = arcade.Sound(file_name=filename)
        # Checking if File is a Music file and Music is allowed by Settings
        if "music" in filename and self.game.music:
            sound.play(volume=self.game.volume / 100, loop=True)
        # Checking if File is a Sound file and Sound is allowed by Settings
        elif "sound" in filename and self.game.sound:
            sound.play(volume=self.game.volume / 100)

    def clear_manager(self):
        """ Clears the UIManager and the Sprites. Adds the Main Title to the Manager and initializes the VBox. """
        # Clears the UIManager and the Sprites
        self.manager.clear()
        self.additionals = arcade.SpriteList()
        # Creating new fresh UIBoxLayout (VBox)
        self.v_box = arcade.gui.UIBoxLayout()
        # Always add/stay on top
        self.title = arcade.gui.UILabel(text="for list in list(range(int('14'))", font_name=("calibri", "arial"), font_size=14,
                                        text_color=self.game.default_style["font_color"], bold=True, dpi=200, align="center")
        # Adding Title to the VBox and the VBox to the UIManager
        self.v_box.add(self.title.with_space_around(bottom=100))
        self.manager.add(
            arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.v_box))

    def update_frames(self, frames):
        """ Alias to arcade.Window().test(). """
        # Update Frames by amount with a shit Method
        self.game.test(frames)

    def loading_animation(self, max_texts):
        """ Creates a Loading Animation. max_texts parameter passes the amount of planned updates. """
        # Clearing the Manager and Setting Function Parameters
        self.clear_manager()
        self.max_texts, self.amount = max_texts+1, 1
        # Adding Loading Text to the VBox, which will later be updated with the UpdateTexts
        self.loading_text = arcade.gui.UILabel(text="Loading...", font_name=("calibri", "arial"), font_size=10,
                                               text_color=self.game.default_style["font_color"], bold=True, dpi=200, align="center",
                                               width=2000)
        self.v_box.add(self.loading_text.with_space_around(bottom=200))
        # The Background Box in dark grey, showing the Border of a Full Progress Bar
        self.background_box = arcade.SpriteSolidColor(304, 14, self.game.default_style["bg_color"])
        self.background_box.center_x, self.background_box.center_y = self.game._width // 2, self.game._height // 2 - 50
        self.additionals.append(self.background_box)
        # The Progress Bar in Green
        self.full_box = arcade.SpriteSolidColor(300 // self.max_texts, 10, self.game.default_style["font_color"])
        self.full_box.center_x, self.full_box.center_y = self.game._width // 2, self.game._height // 2 - 50
        self.additionals.append(self.full_box)
        # Updating the Game to the next Frame to ensure Loading
        self.update_frames(1)

    def update_loading_status(self, text):
        """ Function to Update the Loading Status and Text of the Loading Animation. """
        self.amount += 1
        # Setting the Loading Labels text to the UpdateText
        self.loading_text.text = text
        # Setting the Progress Bar Width to show progress is being made
        self.full_box.width = 300//self.max_texts*self.amount
        # Updating the Game to the next Frame to ensure Loading
        self.update_frames(1)

    def client_click(self):
        """ Function Getting Called when clicking the Client Button. Loads a IP:PORT Input. """
        # Clearing the UIManager
        self.clear_manager()
        # Adding a the IP:PORT Input to the VBox (With a Border to see the input better)
        self.default_client_text = "Enter IP:PORT to Connect to"
        self.client_input = arcade.gui.UIInputText(x=self.game._width // 2, y=self.game._height // 2 + 200,
                                                   width=300, height=20, text=self.default_client_text,
                                                   font_name=('Arial',), font_size=12,
                                                   text_color=self.game.default_style["font_color"], multiline=False,
                                                   size_hint_min=None, size_hint_max=None)

        self.input_border = arcade.gui.UIBorder(
            child=self.client_input, border_color=self.game.default_style["bg_color"])
        self.v_box.add(self.input_border.with_space_around(bottom=20))

        # Deleting the Default Text from the Client Input when its clicked
        @ self.client_input.event()
        def on_event(event: arcade.gui.UIMousePressEvent):
            if type(event) == arcade.gui.UIMousePressEvent:
                if self.client_input.text == self.default_client_text:
                    self.client_input.text = ""

        # Initializing a new VBox for horizontal Layout
        self.buttons_ui = arcade.gui.UIBoxLayout(vertical=False)
        # Adding Back Button to the new VBox (Arrow to the Left)
        texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/left.png")
        back_button = arcade.gui.UITextureButton(texture=texture, scale=0.5)
        self.buttons_ui.add(back_button.with_space_around(left=20))
        # Adding Continue Button to the new VBox (Arrow to the Right)
        texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/right.png")
        continue_button = arcade.gui.UITextureButton(texture=texture, scale=0.5)
        self.buttons_ui.add(continue_button.with_space_around(left=20))
        # Adding the new VBox to the main VBox
        self.v_box.add(self.buttons_ui)

        # Going Back to the StartMenu when Clicking the Back Button
        @ back_button.event("on_click")
        def on_back_click(event):
            self.select_menu()

        # Event for Clicking the Continue Button
        @ continue_button.event("on_click")
        def on_continue_click(event):
            # Initializing a Loading Animation with 3 Incoming Updates
            self.loading_animation(3)
            # Getting the IP and Port from the IP:Port Input and Checking it for Integer
            try:
                self.game.ip, self.game.port = self.client_input.text.split(":")[0], int(
                    self.client_input.text.split(":")[1])
            # If an Incorrect IP:PORT is entered
            except Exception:
                # Placeholder to Get a Full Status Bar
                self.update_loading_status(".")
                self.update_loading_status(".")
                # Updating the Status to wrong IP:Port
                self.update_loading_status("ERROR: Wrong IP:PORT")
                # Waiting 2 Seconds for the Gamer to See
                arcade.pause(2)
                # Going Back to the ServerPort Input
                self.client_click()
                return
            # Starting the Client and connecting to the entered IP:Port
            c_manager = websocket.start_websocket(self.game.ip, self.game.port, is_host=False)
            self.update_loading_status("Attempting Connection")
            # Waiting for The ConnectionManager to Finish Searching
            while c_manager.status == "Searching":
                arcade.pause(2)
            # If the Server Couldnt be found
            if c_manager.status == "Failure":
                # Placeholder to Get a Full Status Bar
                self.update_loading_status(".")
                # Updating the Status to Connection Failed
                self.update_loading_status(f"Could not connect to {self.client_input.text}")
                # Waiting 2 Seconds for the Gamer to See
                arcade.pause(2)
                # Going Back to the ServerPort Input
                self.client_click()
                return
            else:
                # Updating the Status to Connection Successful
                self.update_loading_status(f"Connected successfully to {self.client_input.text}")
                # Getting PlayerPosition set by the Server
                # Get the message
                while True:
                    try:
                        player_choice_message = [msg for msg in c_manager.export_updates() if "PlayerChoice" in msg][0]
                        break
                    except IndexError:
                        pass
                # Getting just the Integer from the message
                my_player = int(player_choice_message.replace("[PlayerChoice] ", ""))
                # Pausing the Game for 1 Second for a better visual experience
                arcade.pause(1)
                # Updating the Status to Loading Game
                self.update_loading_status(f"Loading Game...")
                # Pausing the Game for 1 Second for a better visual experience
                arcade.pause(1)
                # Setting self.game.host to False
                self.game.host = False
                # Calling the main.py game() Function
                self.game.game(c_manager, my_player)

    def server_click(self):
        """ Function Getting Called when clicking the Server Button. Loads a PORT Input. """
        # Clearing the UIManager
        self.clear_manager()
        # Adding a the PORT Input to the VBox (With a Border to see the input better)
        self.default_server_text = "Enter PORT to start the Host on"
        self.server_input = arcade.gui.UIInputText(x=self.game._width // 2, y=self.game._height // 2 + 200,
                                                   width=300, height=20, text=self.default_server_text,
                                                   font_name=('Arial',), font_size=12,
                                                   text_color=self.game.default_style["font_color"], multiline=False,
                                                   size_hint_min=None, size_hint_max=None)
        self.input_border = arcade.gui.UIBorder(
            child=self.server_input, border_color=self.game.default_style["bg_color"])
        self.v_box.add(self.input_border.with_space_around(bottom=20))

        # Deleting the Default Text from the Server Input when its clicked
        @ self.server_input.event()
        def on_event(event: arcade.gui.UIMousePressEvent):
            if type(event) == arcade.gui.UIMousePressEvent:
                if self.server_input.text == self.default_server_text:
                    self.server_input.text = ""

        # Initializing a new VBox for horizontal Layout
        self.buttons_ui = arcade.gui.UIBoxLayout(vertical=False)
        # Adding Back Button to the new VBox (Arrow to the Left)
        texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/left.png")
        back_button = arcade.gui.UITextureButton(texture=texture, scale=0.5)
        self.buttons_ui.add(back_button.with_space_around(left=20))
        # Adding Continue Button to the new VBox (Arrow to the Right)
        texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/right.png")
        continue_button = arcade.gui.UITextureButton(texture=texture, scale=0.5)
        self.buttons_ui.add(continue_button.with_space_around(left=20))
        # Adding the new VBox to the main VBox
        self.v_box.add(self.buttons_ui)

        # Going Back to the StartMenu when Clicking the Back Button
        @ back_button.event("on_click")
        def on_back_click(event):
            self.select_menu()

        # Event for Clicking the Continue Button
        @ continue_button.event("on_click")
        def on_continue_click(event):
            # Initializing a Loading Animation with 3 Incoming Updates
            self.loading_animation(4)
            # Getting the Port from the Port Input and Checking it for Integer
            try:
                self.game.ip, self.game.port = "localhost", int(self.server_input.text)
            # If an Incorrect PORT is entered
            except Exception:
                # Placeholder to Get a Full Status Bar
                self.update_loading_status(".")
                self.update_loading_status(".")
                self.update_loading_status(".")
                # Updating the Status to Bad Port
                self.update_loading_status("ERROR: Bad PORT")
                # Waiting 2 Seconds for the Gamer to See
                arcade.pause(2)
                # Going Back to the ServerPort Input
                self.server_click()
                return
            # Starting the Server on Localhost and the entered Port
            c_manager = websocket.start_websocket(self.game.ip, self.game.port, is_host=True)
            self.update_loading_status("Attempting Connection")
            # Pausing the Game for 1 Second for a better visual experience
            arcade.pause(1)
            # If the Server couldnt be opened on the given Port
            if c_manager.status == "Failure":
                # Placeholder to Get a Full Status Bar
                self.update_loading_status(".")
                self.update_loading_status(".")
                # Updating the Status to Bad Port
                self.update_loading_status(f"Could not open port on {self.server_input.text}")
                # Waiting 2 Seconds for the Gamer to See
                arcade.pause(2)
                # Going Back to the ServerPort Input
                self.server_click()
                return
            else:
                # Waiting for a Client to Connect
                self.update_loading_status("Waiting for a Client to Connect")
                # While Loop to Wait until C_Manager Status isnt "Searching"
                while c_manager.status == "Searching":
                    arcade.pause(1)
                # Set the Message to the Server beeing successfully opened
                self.update_loading_status(f"Host opened successfully on {self.server_input.text}")
                # Selecting own Player by randomization
                my_player = random.randint(0, 1)
                # And sending the other player to the client
                other_player = 0 if my_player == 1 else 1
                c_manager.send_message(f"[PlayerChoice] {other_player}")
                # Pausing the Game for 1 Second for a better visual experience
                arcade.pause(1)
                # Updating Status
                self.update_loading_status(f"Loading Game...")
                # Pausing the Game for 1 Second for a better visual experience
                arcade.pause(1)
                # Setting self.game.host to True (Who could have guessed?!?!?!)
                self.game.host = True
                # Calling the main.py game() Function
                self.game.game(c_manager, my_player)

    def settings_click(self):
        """ Function Getting Called when clicking the Settings Button. Loads the Settings Menu. """
        # Clearing the Manager
        self.clear_manager()
        # Initializing a horizontal UIBoxLayout for the VolumeUI
        self.volumes_ui = arcade.gui.UIBoxLayout(vertical=False)
        # Adding a Text Label for Master Volume to the New UIManager
        volume_label = arcade.gui.UILabel(text="Master Volume", font_name=("calibri", "arial"), font_size=10,
                                          text_color=self.game.default_style["font_color"], dpi=100)
        self.volumes_ui.add(volume_label.with_space_around(left=20))
        # Adding a Slider to the New UIManager
        ui_slider = UISlider(value=self.game.volume, width=150, height=30)
        self.volumes_ui.add(arcade.gui.UIAnchorWidget(child=ui_slider).with_space_around(left=20))
        # Adding the VolumeUI to the main VBox
        self.v_box.add(self.volumes_ui.with_space_around(bottom=20))

        # Updating the Games Volume when the Slider value changes
        @ ui_slider.event()
        def on_change(event: arcade.gui.UIOnChangeEvent):
            self.game.volume = int(ui_slider.value)

        # Initializing a horizontal UIBoxLayout for the SoundsUI
        self.sounds_ui = arcade.gui.UIBoxLayout(vertical=False)
        # Adding a Text Label for Sound to the New UIManager
        sound_label = arcade.gui.UILabel(text="Sound ON/OFF", font_name=("calibri", "arial"), font_size=10,
                                         text_color=self.game.default_style["font_color"], dpi=100)
        self.sounds_ui.add(sound_label.with_space_around(left=20))
        # Adding the Sound Button to the new UIManager
        sound_button = arcade.gui.UIFlatButton(width=100, height=30, text="ON" if self.game.sound else "OFF",
                                               style=self.game.default_style)
        self.sounds_ui.add(sound_button.with_space_around(left=20))
        self.v_box.add(self.sounds_ui.with_space_around(bottom=20))
        # Adding the SoundsUI to the main VBox
        self.musics_ui = arcade.gui.UIBoxLayout(vertical=False)

        # Changing the Games SoundBoolean when the Button is clicked
        # And Changing the Buttons Text
        @ sound_button.event("on_click")
        def on_sound_button_click(event):
            sound_button.text = "ON" if sound_button.text == "OFF" else "OFF"
            self.game.sound = False if sound_button.text == "OFF" else True

        # Initializing a horizontal UIBoxLayout for the MusicUI
        self.musics_ui = arcade.gui.UIBoxLayout(vertical=False)
        # Adding a Text Label for Music to the New UIManager
        music_label = arcade.gui.UILabel(text="Music ON/OFF", font_name=("calibri", "arial"), font_size=10,
                                         text_color=self.game.default_style["font_color"], dpi=100)
        self.musics_ui.add(music_label.with_space_around(left=20))
        # Adding the Music Button to the new UIManager
        music_button = arcade.gui.UIFlatButton(width=100, height=30, text="ON" if self.game.music else "OFF",
                                               style=self.game.default_style)
        self.musics_ui.add(music_button.with_space_around(left=20))
        # Adding the MusicUI to the main VBox
        self.v_box.add(self.musics_ui.with_space_around(bottom=20))

        # Changing the Games MusicBoolean when the Button is clicked
        # And Changing the Buttons Text
        @ music_button.event("on_click")
        def on_sound_button_click(event):
            music_button.text = "ON" if music_button.text == "OFF" else "OFF"
            self.game.music = False if music_button.text == "OFF" else True

        # Adding the Back Button (Arrow to the Left) to the VBox
        texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/left.png")
        back_button = arcade.gui.UITextureButton(texture=texture, scale=0.5)
        self.v_box.add(back_button.with_space_around(left=20))

        # When Clicking the BackButton, saving the Settings to the JSON and going back to the Select Menu
        @ back_button.event("on_click")
        def on_back_click(event):
            self.game.settings_json["master_volume"], self.game.settings_json["music"], self.game.settings_json[
                "sound"] = self.game.volume, self.game.music, self.game.sound
            with open(self.settings_path, 'w') as json_file:
                json.dump(self.game.settings_json, json_file)
            self.select_menu()

    def select_menu(self):
        """ Main Menu Select Function. Builts Buttons for Client, Server and Settings. """
        # Clearing the UIManager
        self.clear_manager()
        # Adding the Client Button to the VBox
        client_button = arcade.gui.UIFlatButton(x=self.game._width // 2, y=self.game._height // 2 + 200, width=150,
                                                height=50, text="Client", style=self.game.default_style)
        self.v_box.add(client_button.with_space_around(bottom=20))
        # Adding the Server Button to the VBox
        server_button = arcade.gui.UIFlatButton(x=self.game._width // 2, y=self.game._height // 2 - 200, width=150,
                                                height=50, text="Host", style=self.game.default_style)
        self.v_box.add(server_button.with_space_around(bottom=20))
        # Adding the Settings Button to the VBox
        settings_button = arcade.gui.UIFlatButton(x=self.game._width // 2, y=self.game._height // 2 - 200, width=150,
                                                  height=50, text="Settings", style=self.game.default_style)
        self.v_box.add(settings_button.with_space_around(bottom=20))
        # Adding the Quit Button to the VBox
        quit_button = arcade.gui.UIFlatButton(x=self.game._width // 2, y=self.game._height // 2 - 200, width=150,
                                              height=50, text="Quit", style=self.game.default_style)
        self.v_box.add(quit_button.with_space_around(bottom=20))

        # Calling matching Function if on of the Buttons is clicked
        @ client_button.event("on_click")
        def on_client_click(event):
            self.client_click()

        @ server_button.event("on_click")
        def on_server_click(event):
            self.server_click()

        @ settings_button.event("on_click")
        def on_settings_click(event):
            self.settings_click()

        # Quiting the Game when clicking the QuitButton
        # This doesnt quit the Interpreter
        @quit_button.event("on_click")
        def on_quit_click(event):
            self.game.close()
            arcade.exit()

    def draw_start_menu(self):
        """ Draws the UIManager and the additional Sprites to the screen. """
        if self.game._setup:
            self.manager.draw()
            for sprite in self.additionals:
                sprite.draw()
