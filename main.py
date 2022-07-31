import arcade
from modules import start_menu, pause_menu, maps_loader, player, sounds, level_menu
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "for list in list(range(int('14'))"


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.background_menu = (61, 169, 143)
        self.background = None

        self.camera = None
        self.default_args = dict(vars(self))
        self.host = False
        # If you have sprite lists, you should create them here,
        # and set them to None
        self.level = 0

        self.counter = 20

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Clearing Game Variables to Default (Support for re-starting the Game)
        for item in vars(self):
            if item not in self.default_args:
                del item

        self.background = self.background_menu

        # Initializing Modules
        self.start_menu = start_menu.StartMenu(self)
        self.pause_menu = pause_menu.PauseMenu(self)
        self.level_menu = level_menu.LevelMenu(self)
        self.maps_loader = maps_loader.MapManager(self)
        self.sounds = sounds.Sounds(self)
        # Calling the Select Menu to show on Startup
        self.start_menu.select_menu()
        self.level = 0

    def game(self, c_manager, my_player):
        """ Custom Function which gets called when joining a Game.
        C_Manager is the CommunicationManager, My_Player is the random Player you are playing as. (int)"""
        # Gets Called when the Game Begins
        self._setup = False

        self.c_manager = c_manager
        self.player = player.Player(self, my_player)
        self.sec_player = player.RobotPlayer(self, my_player)

        self.maps_loader.load_map_data("0", self.player, self.sec_player, c_manager)
        # Play ShitMusic
        self.play_sound("./resources/music-tobu-infectious.mp3")

        self.my_player = my_player

    def next_level(self, level=None, self_triggered=True):
        """ Runs the next level or the passed level"""

        if self._setup == False: # only works in game
            if level is None:
                self.level += 1
            else:
                self.level = int(level)

            self.maps_loader = maps_loader.MapManager(self)

            self.player = player.Player(self, self.my_player)
            self.sec_player = player.RobotPlayer(self, self.my_player)

            self.maps_loader.load_map_data(str(self.level), self.player, self.sec_player, self.c_manager)

            if self_triggered: # send the info of which level to the other client
                self.c_manager.send_message(f"[level] {self.level}")

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        if self.camera:
            self.camera.use()

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background) if type(
            self.background) != tuple else arcade.set_background_color(self.background)

        # Draw the game or the menue the functions check if they siuld be drawn
        self.start_menu.draw_start_menu()
        self.maps_loader.draw_layer()

        # Always draw on Top
        self.pause_menu.draw_pause_menu()
        self.level_menu.draw_level_menu()

    def on_update(self, delta_time):
        """
        This function is called about 20 times per secound to update the level if needed.
        """
        self.maps_loader.update()
        
        # Keeps the connection alive
        if self.host and self.counter == 10:
            self.c_manager.send_message("[PING]")

        self.counter = (self.counter - 1)%21

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

        # Fi in game the keys get passed along to the player
        if not self._setup:
            self.player.player_key_press(key, key_modifiers)


def main():
    """ Main function """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
