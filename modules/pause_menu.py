import arcade
import arcade.gui


class PauseMenu:

    def __init__(self, game):
        self.game = game
        # Setting the _escape Value to know if the Escape Menu should be opened
        self.game._escape = False

    def pause(self):
        """ Pausing the Game by creating a EscapeUI. """
        # Creating and enabling the EscapeUIManager
        self.escape_ui = arcade.gui.UIManager()
        self.escape_ui.enable()
        # Creating a UIBoxLayout for the VBox and the Background
        self.escape_v_box = arcade.gui.UIBoxLayout()
        self.bg_v_box = arcade.gui.UIBoxLayout()

        # Adding a Background (Its Translucent Black to Darken the Background)
        bg = arcade.gui.UISpace(x=-5, y=-5, width=self.game._width+10,
                                height=self.game._height+10, color=(0, 0, 0, 170))
        self.escape_ui.add(bg)
        # Adding the Games Title and a "Pause Menu" Text
        self.title = arcade.gui.UILabel(text="for level_id in range(14)", font_name=(
            "calibri", "arial"), font_size=20, text_color=arcade.color.AMARANTH_PINK, bold=True, dpi=200, align="center")
        self.pause_title = arcade.gui.UILabel(text="Pause Menu", font_name=(
            "calibri", "arial"), font_size=10, text_color=arcade.color.AMARANTH_PINK, bold=True, dpi=200, align="center")
        self.escape_v_box.add(self.title.with_space_around(bottom=20))
        self.escape_v_box.add(self.pause_title.with_space_around(bottom=100))
        # Creating a Continue Button
        continue_button = arcade.gui.UIFlatButton(
            x=self.game._width//2, y=self.game._height//2+200, width=150, height=50, text="Continue", style=self.game.default_style)
        self.escape_v_box.add(continue_button.with_space_around(bottom=20))
        # Creating a LevelMenu Button
        if self.game.host:
            level_button = arcade.gui.UIFlatButton(x=self.game._width//2, y=self.game._height
                                                   // 2+200, width=150, height=50, text="Level Menu", style=self.game.default_style)
            self.escape_v_box.add(level_button.with_space_around(bottom=20))

            # Going to LevelMenu when clicking the LevelButton
            @level_button.event("on_click")
            def on_level_click(event):
                self.game.level_menu.level()
        # Creating a Restart Button
        reload_button = arcade.gui.UIFlatButton(
            x=self.game._width//2, y=self.game._height//2-200, width=150, height=50, text="Reload Level", style=self.game.default_style)
        self.escape_v_box.add(reload_button.with_space_around(bottom=20))
        # Creating a Quit Button
        quit_button = arcade.gui.UIFlatButton(x=self.game._width//2, y=self.game._height
                                              // 2-200, width=150, height=50, text="Quit Game", style=self.game.default_style)
        self.escape_v_box.add(quit_button.with_space_around(bottom=20))

        # Unpausing Game when clicking the ContinueButton
        @continue_button.event("on_click")
        def on_continue_click(event):
            self.game._escape = False
            self.unpause()

        # Restarting the Game when clicking the RestartButton
        @reload_button.event("on_click")
        def on_restart_click(event):
            self.game.maps_loader.load_map_data(
                    self.game.maps_loader.map_name, self.game.player, self.game.maps_loader.sec_player, self.game.maps_loader.c_manager)

        # Quiting the Game when clicking the QuitButton
        # This doesnt quit the Interpreter
        @quit_button.event("on_click")
        def on_quit_click(event):
            self.game.close()
            self.game.c_manager.send_message("websocket.disconnect")
            arcade.exit()

        # Adding the BackgroundUI and the EscapeVBox to the EscapeUI
        self.escape_ui.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.bg_v_box))
        self.escape_ui.add(arcade.gui.UIAnchorWidget(anchor_x="center_x",
                           anchor_y="center_y", child=self.escape_v_box))

    def unpause(self):
        """ Unpauses the game by Disabling the EscapeUI. """
        # Clearing the EscapeUI and disabling it for it to not be drawn anymore
        self.escape_ui.clear()
        self.escape_ui.disable()

    def draw_pause_menu(self):
        """ Draws the EscapeUI if the Escape Menu should be opened. """
        # Drawing the EscapeUI if the EscapeMenu should be open.
        if self.game._escape:
            self.escape_ui.draw()
