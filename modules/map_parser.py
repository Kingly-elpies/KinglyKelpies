import arcade
from enum import Enum


def get_sprite(player_id: int) -> arcade.Sprite:
    """
    Creates an arcade sprite for the player
    :param int player_id: The id of the player we want the sprite (0 or 1)
    """
    return arcade.Sprite(
        filename=f"./resources/sprites/player{player_id}.png",
        scale=4.0,
        image_width=16, image_height=16,
        center_x=8, center_y=8,
        hit_box_algorithm='Simple'
    )


class MapManager:
    def __init__(self) -> None:
        self.maps = None
        self.tile_map = None
        self.sprite_lists = None
        self.physics_engine = None

    class Layers(Enum):
        """ Represents any layer that can be present in a map for this game """

        ALL = 0
        """ All layers on the map (includes Ground, Objects and Players) """

        PLAYERS = "Players"
        """ The layer that has the players """

        OBJECTS = "Objects"
        """ The layer that has all activators, activables, holes, rails and carts """

        GROUND = "Ground"
        """ The layer that has the walls, ground, glitches and tunnels """

    def load_map_data(self, map_name: str, scaling: float = 1.0) -> None:
        """
        Load a tile map file from the resources/tilemaps folder
        :param str map_name: The name of the file without file extension
        :param float scaling: Factor by which the size of the map should be increased (default: 1)
        """
        # Loading the map
        self.tile_map = arcade.load_tilemap(f"./resources/tilemaps/{map_name}.tmx", scaling)

        # Getting all the sprite layers in this map
        self.sprite_lists = self.maps.sprite_lists
        """self.physics_engine = arcade.PhysicsEngineSimple(
            player_sprite=get_sprite(self.player_id),
            walls=self.sprite_lists["Walls"]
        )"""

    def draw_layer(self, map_name: str, layer: Layers = Layers.ALL) -> None:
        """
        Draws one or all layer of a map to the screen
        :param str map_name: The name of the map
        :param Layers layer: The layer to be drawn (defaults to all)
        """
        if layer == self.Layers.ALL:
            sprite_lists = self.sprite_lists[map_name]
            for layer in sprite_lists:
                sprite_lists[layer].draw()
        else:
            self.sprite_lists[map_name][layer.value].draw()
