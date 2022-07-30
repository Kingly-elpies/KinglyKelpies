import arcade
from modules import start_menu, pause_menu, maps_loader, player

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

        self.background = (61, 169, 143)
        self.default_args = dict(vars(self))
        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Clearing Game Variables to Default (Support for re-starting the Game)
        for item in vars(self):
            if item not in self.default_args:
                del item

        # Create your sprites and sprite lists here

        # Initializing Modules
        self.start_menu = start_menu.StartMenu(self)
        self.pause_menu = pause_menu.PauseMenu(self)
        self.maps_loader = maps_loader.MapManager(self)
        # Calling the Select Menu to show on Startup
        self.start_menu.select_menu()

    def game(self, c_manager, my_player):
        """ Custom Function which gets called when joining a Game.
        C_Manager is the CommunicationManager, My_Player is the random Player you are playing as. """
        # Gets Called when the Game Begins
        self._setup = False

        self.c_manager = c_manager
        self.player = player.Player(self,my_player)
        self.sec_player = player.RobotPlayer(self, my_player)

        self.maps_loader.load_map_data("test_map",self.player, self.sec_player,c_manager)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background) if type(
            self.background) != tuple else arcade.set_background_color(self.background)

        # Call draw() on all your sprite lists below
        self.start_menu.draw_start_menu()
        self.maps_loader.draw_layer()

        # Always draw on Top
        self.pause_menu.draw_pause_menu()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.maps_loader.update()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        # Support for Pause Menu
        if key == arcade.key.ESCAPE and not self._setup:
            # Setting self._escape to the opposite of the Bool
            self._escape = not self._escape
            # Pausing the Game if the Escape Bool is now true else unpause the game
            self.pause_menu.pause() if self._escape else self.pause_menu.unpause()
        #
        if not self._setup:
            self.player.player_key_press(key, key_modifiers)

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
