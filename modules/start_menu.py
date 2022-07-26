import json
import os.path
import arcade
import arcade.gui
from arcade.experimental.uislider import UISlider
from modules import websocket_communication as websocket


class StartMenu:
    def __init__(self, game):
        self.full_box = None
        self.background_box = None
        self.loading_text = None
        self.max_texts = None
        self.title = None

        self.game = game
        self.game._setup = True

        self.game.manager = arcade.gui.UIManager()
        self.game.manager.enable()
        self.game.v_box = arcade.gui.UIBoxLayout()
        self.game.additionals = arcade.SpriteList()

        # Load Json from settings.json
        self.settings_path = os.path.dirname(os.path.dirname(__file__)) + "\\resources\\settings.json"
        with open(self.settings_path) as json_file:
            self.game.settings_json = json.load(json_file)
        self.game.volume, self.game.music, self.game.sound = self.game.settings_json["master_volume"], \
                                                             self.game.settings_json["music"], self.game.settings_json[
                                                                 "sound"]  # Fix that Later when loading a json to save settings

        self.game.play_sound = self.play_sound
        self.game.default_style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.AMARANTH_PINK,
            "border_width": 2,
            "border_color": None,
            "bg_color": (27, 27, 27),

            # used if button is pressed
            "bg_color_pressed": arcade.color.EERIE_BLACK,
            "border_color_pressed": arcade.color.AMARANTH_PINK,  # also used when hovered
            "font_color_pressed": arcade.color.AMARANTH_PINK,
        }

    def play_sound(self, filename):
        sound = arcade.Sound(file_name=filename)
        if "music" in filename and self.game.music:
            sound.play(volume=self.game.volume / 100)
        elif "music" not in filename and self.game.sound:
            sound.play(volume=self.game.volume / 100)

    def clear_manager(self):
        self.game.manager.clear()
        self.game.additionals = []

        self.game.v_box = arcade.gui.UIBoxLayout()
        # Always add/stay on top
        self.title = arcade.gui.UILabel(text="Your Ad Here", font_name=("calibri", "arial"), font_size=20,
                                        text_color=arcade.color.AMARANTH_PINK, bold=True, dpi=200, align="center")
        self.game.v_box.add(self.title.with_space_around(bottom=100))
        self.game.manager.add(
            arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.game.v_box))

    def update_frames(self, frames):
        # Update Frames by amount with a shit Method
        self.game.test(frames)

    def loading_animation(self, max_texts):
        self.clear_manager()
        self.max_texts, self.amount = max_texts+1, 1
        self.loading_text = arcade.gui.UILabel(text="Loading...", font_name=("calibri", "arial"), font_size=10,
                                               text_color=arcade.color.WHITE, bold=True, dpi=200, align="center",
                                               width=2000)
        self.game.v_box.add(self.loading_text.with_space_around(bottom=200))

        self.background_box = arcade.SpriteSolidColor(304, 14, (27, 27, 27))
        self.background_box.center_x, self.background_box.center_y = self.game._width // 2, self.game._height // 2 - 50

        self.full_box = arcade.SpriteSolidColor(300 // self.max_texts, 10, arcade.color.GREEN, )
        self.full_box.center_x, self.full_box.center_y = self.game._width // 2, self.game._height // 2 - 50

        self.game.additionals.append(self.background_box)
        self.game.additionals.append(self.full_box)
        self.update_frames(1)

    def update_loading_status(self, text):
        self.amount += 1
        self.loading_text.text = text
        self.game.manager.trigger_render()
        self.full_box.width = 300//self.max_texts*self.amount
        self.update_frames(1)

    def select_menu(self):
        self.clear_manager()
        client_button = arcade.gui.UIFlatButton(x=self.game._width // 2, y=self.game._height // 2 + 200, width=150,
                                                height=50, text="Client", style=self.game.default_style)
        self.game.v_box.add(client_button.with_space_around(bottom=20))
        server_button = arcade.gui.UIFlatButton(x=self.game._width // 2, y=self.game._height // 2 - 200, width=150,
                                                height=50, text="Server", style=self.game.default_style)
        self.game.v_box.add(server_button.with_space_around(bottom=20))
        settings_button = arcade.gui.UIFlatButton(x=self.game._width // 2, y=self.game._height // 2 - 200, width=150,
                                                  height=50, text="Settings", style=self.game.default_style)
        self.game.v_box.add(settings_button.with_space_around(bottom=20))

        @client_button.event("on_click")
        def on_client_click(event):
            self.clear_manager()

            self.default_client_text = "Enter IP:PORT to Connect to"
            self.client_input = arcade.gui.UIInputText(x=self.game._width // 2, y=self.game._height // 2 + 200,
                                                       width=300, height=20, text=self.default_client_text,
                                                       font_name=('Arial',), font_size=12,
                                                       text_color=arcade.color.AMARANTH_PINK, multiline=False,
                                                       size_hint_min=None, size_hint_max=None)
            self.input_border = arcade.gui.UIBorder(child=self.client_input, border_color=(27, 27, 27))
            self.game.v_box.add(self.input_border.with_space_around(bottom=20))

            @self.client_input.event()
            def on_event(event: arcade.gui.UIMousePressEvent):
                if type(event) == arcade.gui.UIMousePressEvent:
                    if self.client_input.text == self.default_client_text:
                        self.client_input.text = ""

            self.buttons_ui = arcade.gui.UIBoxLayout(vertical=False)
            texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/left.png")
            back_button = arcade.gui.UITextureButton(texture=texture, scale=0.5)
            self.buttons_ui.add(back_button.with_space_around(left=20))

            texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/right.png")
            continue_button = arcade.gui.UITextureButton(texture=texture, scale=0.5)
            self.buttons_ui.add(continue_button.with_space_around(left=20))
            self.game.v_box.add(self.buttons_ui)

            # Handle Clicks
            @back_button.event("on_click")
            def on_back_click(event):
                self.select_menu()

            @continue_button.event("on_click")
            def on_continue_click(event):
                self.loading_animation(3)
                try:
                    self.game.ip, self.game.port = self.client_input.text.split(":")[0], int(
                        self.client_input.text.split(":")[1])
                # If an Incorrect IP:PORT is entered
                except Exception:
                    # Placeholder to Get a Full Status Bar
                    self.update_loading_status(".")
                    self.update_loading_status(".")
                    self.update_loading_status("ERROR: Bad Port")
                    arcade.pause(2)
                    on_server_click("Placeholder")
                    return

                c_manager = websocket.start_websocket(self.game.ip, self.game.port, is_host=False)
                self.update_loading_status("Attempting Connection")
                while c_manager.status == "Searching":
                    arcade.pause(2)

                if c_manager.status == "Failure":
                    # Placeholder to Get a Full Status Bar
                    self.update_loading_status(".")
                    self.update_loading_status(f"Could not connect to {self.client_input.text}")
                    arcade.pause(2)
                    on_server_click("Placeholder")
                    return
                else:
                    self.update_loading_status(f"Connected successfully to {self.client_input.text}")
                    arcade.pause(1)
                    self.update_loading_status(f"Loading Game...")
                    arcade.pause(1)
                    self.game.game(c_manager)

        @server_button.event("on_click")
        def on_server_click(event):
            self.clear_manager()

            self.default_server_text = "Enter PORT to host Server on"
            self.server_input = arcade.gui.UIInputText(x=self.game._width // 2, y=self.game._height // 2 + 200,
                                                       width=300, height=20, text=self.default_server_text,
                                                       font_name=('Arial',), font_size=12,
                                                       text_color=arcade.color.AMARANTH_PINK, multiline=False,
                                                       size_hint_min=None, size_hint_max=None)
            self.input_border = arcade.gui.UIBorder(child=self.server_input, border_color=(27, 27, 27))
            self.game.v_box.add(self.input_border.with_space_around(bottom=20))

            @self.server_input.event()
            def on_event(event: arcade.gui.UIMousePressEvent):
                if type(event) == arcade.gui.UIMousePressEvent:
                    if self.server_input.text == self.default_server_text:
                        self.server_input.text = ""

            self.buttons_ui = arcade.gui.UIBoxLayout(vertical=False)
            texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/left.png")
            back_button = arcade.gui.UITextureButton(texture=texture, scale=0.5)
            self.buttons_ui.add(back_button.with_space_around(left=20))

            texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/right.png")
            continue_button = arcade.gui.UITextureButton(texture=texture, scale=0.5)
            self.buttons_ui.add(continue_button.with_space_around(left=20))
            self.game.v_box.add(self.buttons_ui)

            @back_button.event("on_click")
            def on_back_click(event):
                self.select_menu()

            @continue_button.event("on_click")
            def on_continue_click(event):
                self.loading_animation(3)
                try:
                    self.game.ip, self.game.port = "localhost", int(self.server_input.text)
                # If an Incorrect IP:PORT is entered
                except Exception:
                    # Placeholder to Get a Full Status Bar
                    self.update_loading_status(".")
                    self.update_loading_status(".")
                    self.update_loading_status("ERROR: Wrong IP:PORT")
                    arcade.pause(2)
                    on_client_click("Placeholder")
                    return

                c_manager = websocket.start_websocket(self.game.ip, self.game.port, is_host=True)
                self.update_loading_status("Attempting Connection")
                arcade.pause(1)
                if c_manager.status == "Failure":
                    # Placeholder to Get a Full Status Bar
                    self.update_loading_status(".")
                    self.update_loading_status(f"Could not open port on {self.server_input.text}")
                    arcade.pause(2)
                    on_client_click("Placeholder")
                    return
                else:
                    self.update_loading_status(f"Server opened successfully on {self.server_input.text}")
                    arcade.pause(1)
                    self.update_loading_status(f"Loading Game...")
                    arcade.pause(1)
                    self.game.game(c_manager)

        @settings_button.event("on_click")
        def one_settings_click(event):
            self.clear_manager()

            self.volumes_ui = arcade.gui.UIBoxLayout(vertical=False)
            volume_label = arcade.gui.UILabel(text="Master Volume", font_name=("calibri", "arial"), font_size=10,
                                              text_color=arcade.color.AMARANTH_PINK, dpi=100)

            ui_slider = UISlider(value=self.game.volume, width=150, height=30)

            @ui_slider.event()
            def on_change(event: arcade.gui.UIOnChangeEvent):
                self.game.volume = int(ui_slider.value)

            self.volumes_ui.add(volume_label.with_space_around(left=20))
            self.volumes_ui.add(arcade.gui.UIAnchorWidget(child=ui_slider).with_space_around(left=20))
            self.game.v_box.add(self.volumes_ui.with_space_around(bottom=20))

            self.sounds_ui = arcade.gui.UIBoxLayout(vertical=False)
            sound_label = arcade.gui.UILabel(text="Sound ON/OFF", font_name=("calibri", "arial"), font_size=10,
                                             text_color=arcade.color.AMARANTH_PINK, dpi=100)

            sound_button = arcade.gui.UIFlatButton(width=100, height=30, text="ON" if self.game.sound else "OFF",
                                                   style=self.game.default_style)

            @sound_button.event("on_click")
            def on_sound_button_click(event):
                sound_button.text = "ON" if sound_button.text == "OFF" else "OFF"
                self.game.sound = False if sound_button.text == "OFF" else True

            self.sounds_ui.add(sound_label.with_space_around(left=20))
            self.sounds_ui.add(sound_button.with_space_around(left=20))
            self.game.v_box.add(self.sounds_ui.with_space_around(bottom=20))

            self.musics_ui = arcade.gui.UIBoxLayout(vertical=False)
            music_label = arcade.gui.UILabel(text="Music ON/OFF", font_name=("calibri", "arial"), font_size=10,
                                             text_color=arcade.color.AMARANTH_PINK, dpi=100)

            music_button = arcade.gui.UIFlatButton(width=100, height=30, text="ON" if self.game.music else "OFF",
                                                   style=self.game.default_style)

            @music_button.event("on_click")
            def on_sound_button_click(event):
                music_button.text = "ON" if music_button.text == "OFF" else "OFF"
                self.game.music = False if music_button.text == "OFF" else True

            self.musics_ui.add(music_label.with_space_around(left=20))
            self.musics_ui.add(music_button.with_space_around(left=20))
            self.game.v_box.add(self.musics_ui.with_space_around(bottom=20))

            self.buttons_ui = arcade.gui.UIBoxLayout(vertical=False)
            texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/left.png")
            back_button = arcade.gui.UITextureButton(texture=texture, scale=0.5)
            self.buttons_ui.add(back_button.with_space_around(left=20))
            self.game.v_box.add(self.buttons_ui)

            # Handle Clicks
            @back_button.event("on_click")
            def on_back_click(event):
                self.game.settings_json["master_volume"], self.game.settings_json["music"], self.game.settings_json[
                    "sound"] = self.game.volume, self.game.music, self.game.sound
                with open(self.settings_path, 'w') as json_file:
                    json.dump(self.game.settings_json, json_file)
                self.select_menu()

    def draw_start_menu(self):
        if self.game._setup:
            self.game.manager.draw()
            for sprite in self.game.additionals:
                sprite.draw()
