import arcade
import arcade.gui


class LevelMenu:

    def __init__(self, game):
        self.game = game
        # Setting the _escape Value to know if the Escape Menu should be opened
        self.game._level = False

    def level(self):
        """ Level Select Menu. """
        # Creating and enabling the EscapeUIManager
        self.level_ui = arcade.gui.UIManager()
        self.level_ui.enable()
        # Creating a UIBoxLayout for the VBox and the Background
        self.level_v_box = arcade.gui.UIBoxLayout()
        self.bg_v_box = arcade.gui.UIBoxLayout()

        # Adding a Background (Its Translucent Black to Darken the Background)
        bg = arcade.gui.UISpace(x=-5, y=-5, width=self.game._width+10,
                                height=self.game._height+10, color=(0, 0, 0, 170))
        self.level_ui.add(bg)

        # Create input line
        inp_width = 300
        self.default_client_text = "Enter level in range(14)"
        self.level_input = arcade.gui.UIInputText( x=self.game._width//2-inp_width//2,y =self.game._height//2,width=inp_width, height=20, text=self.default_client_text,
                                                   font_name=('Arial',), font_size=12,
                                                   text_color=self.game.default_style["font_color"], multiline=False,
                                                   size_hint_min=None, size_hint_max=None)

        self.input_border = arcade.gui.UIBorder(
            child=self.level_input, border_color=self.game.default_style["bg_color"])
        self.level_ui.add(self.input_border.with_space_around(bottom=20))

        @self.level_input.event()
        def on_event(event: arcade.gui.UIMousePressEvent):
            if type(event) == arcade.gui.UIMousePressEvent:
                if self.level_input.text == self.default_client_text:
                    self.level_input.text = ""

        # create back button
        button_width = 150
        button_offset = 200

        back_button = arcade.gui.UIFlatButton(
            x = self.game._width//2-button_width//2 + button_offset,
            y = self.game._height//2-80,
            width=button_width, height=50, text=f"Back", style=self.game.default_style)
        self.level_ui.add(back_button.with_space_around(top=400))

        # back_button the Game when clicking the RestartButton
        @ back_button.event("on_click")
        def on_back_click(event):
            self.unlevel()
            self.game.pause_menu.pause()

        # create and add ok button
        ok_button = arcade.gui.UIFlatButton(
            x = self.game._width//2-button_width//2 - button_offset,
            y = self.game._height//2-80,
        width=150, height=50, text=f"Go", style=self.game.default_style)
        self.level_ui.add(ok_button.with_space_around(top=400))

        @ ok_button.event("on_click")
        def on_back_click(event):
            self.unlevel()
            self.game.pause_menu.pause()
            try:
                if int(self.level_input.text) in range(-1,14):
                    self.game.next_level(level=self.level_input.text)
            except ValueError:
                pass

        # Adding the BackgroundUI and the EscapeVBox to the EscapeUI
        self.level_ui.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.bg_v_box))
        self.level_ui.add(arcade.gui.UIAnchorWidget(anchor_x="center_x",
                                                    anchor_y="center_y", child=self.level_v_box))

        self.game._level = True

    def unlevel(self):
        """ Unpauses the game by Disabling the EscapeUI. """
        # Clearing the EscapeUI and disabling it for it to not be drawn anymore
        self.level_ui.clear()
        self.level_ui.disable()

        self.game._level = False

    def draw_level_menu(self):
        """ Draws the EscapeUI if the Escape Menu should be opened. """
        # Drawing the EscapeUI if the EscapeMenu should be open.
        if self.game._level:
            self.level_ui.draw()
