import arcade
import arcade.gui

class PauseMenu:
    def __init__(self, game):
        self.game = game
        self.game._escape = False

    def pause(self):
        self.escape_ui = arcade.gui.UIManager()
        self.escape_ui.enable()
        self.escape_v_box = arcade.gui.UIBoxLayout()
        self.bg_v_box = arcade.gui.UIBoxLayout()


        # bg_sprite = arcade.SpriteSolidColor(self.game._width+10, self.game._height+10, (0,0,0, 170))
        # bg = arcade.gui.UISpriteWidget(x=-5, y=-5, width=self.game._width+10, height=self.game._height+10, sprite=bg_sprite)
        bg = arcade.gui.UISpace(x=-5, y=-5, width=self.game._width+10, height=self.game._height+10, color=(0,0,0, 170))
        @bg.event()
        def events(event):
            pass
        self.escape_ui.add(bg)

        self.title = arcade.gui.UILabel(text="Your Ad Here", font_name=("calibri", "arial"), font_size=20, text_color=arcade.color.AMARANTH_PINK, bold=True, dpi=200, align="center")
        self.pause_title = arcade.gui.UILabel(text="Pause Menu", font_name=("calibri", "arial"), font_size=10, text_color=arcade.color.AMARANTH_PINK, bold=True, dpi=200, align="center")
        self.escape_v_box.add(self.title.with_space_around(bottom=20))
        self.escape_v_box.add(self.pause_title.with_space_around(bottom=100))

        continue_button = arcade.gui.UIFlatButton(x=self.game._width//2, y=self.game._height//2+200, width=150, height=50, text="Continue", style=self.game.default_style)
        self.escape_v_box.add(continue_button.with_space_around(bottom=20))
        restart_button = arcade.gui.UIFlatButton(x=self.game._width//2, y=self.game._height//2-200, width=150, height=50, text="Restart Game", style=self.game.default_style)
        self.escape_v_box.add(restart_button.with_space_around(bottom=20))
        quit_button = arcade.gui.UIFlatButton(x=self.game._width//2, y=self.game._height//2-200, width=150, height=50, text="Quit Game", style=self.game.default_style)
        self.escape_v_box.add(quit_button.with_space_around(bottom=20))

        @continue_button.event("on_click")
        def on_continue_click(event):
            self.game._escape = False
            self.unpause()

        @restart_button.event("on_click")
        def on_restart_click(event):
            self.game.setup()

        @quit_button.event("on_click")
        def on_quit_click(event):
            self.game.close()
            arcade.exit()

        self.escape_ui.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.bg_v_box))
        self.escape_ui.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.escape_v_box))


    def unpause(self):
        self.escape_ui.clear()
        self.escape_ui.disable()

    def draw_pause_menu(self):
        if self.game._escape:
            self.escape_ui.draw()
            # for sprite in self.escape_items:
            #     sprite.draw()
