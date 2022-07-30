import arcade
from modules import start_menu

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Starting Template"


class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.background = arcade.load_texture(":resources:images/cybercity_background/far-buildings.png")
        self.background = arcade.color.DARK_BLUE_GRAY
        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        self.start_menu = start_menu.StartMenu(self)
        self.start_menu.select_menu()

    def game(self, c_manager):
        # Gets Called when the Game Begins
        self._setup = False
<<<<<<< Updated upstream

        # Temporary Pause to allow other client to connect
        arcade.pause(3)
        c_manager.send_message("Test Data")
        print(c_manager.export_updates())
=======
        self.c_manager = c_manager
        self.player = player.Player(self,my_player)
        self.sec_player = player.RobotPlayer(self, my_player)
        self.maps_loader.load_map_data("tutorial1", self.player, self.sec_player)
>>>>>>> Stashed changes

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background) if type(self.background) != tuple else arcade.set_background_color(self.background)

        # Call draw() on all your sprite lists below

        # Check if Game is in Setup State, if so, draw setup
        if self._setup:
            self.manager.draw()
            for sprite in self.additionals:
                sprite.draw()


    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
<<<<<<< Updated upstream
        pass
=======
        if not self._setup:
            for update in self.c_manager.export_updates():
                if "[Walk]" in update:
                    x, y = update.replace("[Walk] ", "").split(",")
                    self.sec_player.player.center_x, self.sec_player.player.center_y = int(x), int(y)
>>>>>>> Stashed changes

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main function """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
