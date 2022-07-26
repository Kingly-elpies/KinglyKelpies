import arcade
from modules import start_menu
from modules import map_parser

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Starting Template"
MOVING_SPEED = 1    # Unit is tile/second


class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.start_menu = None
        self._setup = None
        self.maps = None

        self.background = arcade.load_texture(":resources:images/cybercity_background/far-buildings.png")
        self.background = arcade.color.DARK_BLUE_GRAY

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        self.start_menu = start_menu.StartMenu(self)
        self.start_menu.select_menu()

        self.maps = map_parser.MapManager()
        self.maps.load_map_data("tutorial1", 4.0)

    def game(self, c_manager):
        # Gets Called when the Game Begins
        self._setup = False

        # Temporary Pause to allow other client to connect
        arcade.pause(3)
        c_manager.send_message("Test Data")
        print(c_manager.export_updates())

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background) \
            if type(self.background) != tuple else arcade.set_background_color(self.background)

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
        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        map_name = "tutorial1"
        self.clear()
        match key:
            case arcade.key.W:
                self.maps.draw_layer(map_name, self.maps.Layers.GROUND)
            case arcade.key.A:
                self.maps.draw_layer(map_name, self.maps.Layers.OBJECTS)
            case arcade.key.S:
                self.maps.draw_layer(map_name, self.maps.Layers.PLAYERS)
            case arcade.key.D:
                self.maps.draw_layer(map_name)
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
