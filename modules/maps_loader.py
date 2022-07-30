import arcade
import json
from PIL import Image
from modules import objects


class MapManager:
    def __init__(self, game, screen_size=(800, 600)) -> None:
        self.game = game
        self.map = [[]]
        self.scale = 4
        self.tile_size = 16
        self.screen_size = screen_size

        self.textures = self.load_textures("./resources/tilesets/KelpiesTileset.png")
        self.sprites = []

        self.collision = []
        self.doors = []
        self.interactables = []
        self.needs_updates = []

        self.loaded = False

    def will_collide(self, x, y):
        for collidable in self.collision:
            w_x, w_y = collidable.sprite.center_x, collidable.sprite.center_y

            if w_x == x and w_y == y:
                return True
        return False

    def get_door(self,x,y):
        return [door for door in self.doors if door.x == x and door.y == y][0] #return the door with the matching coordinates

    def load_textures(self, fp, tile_size=16):
        tile_map = Image.open(fp)
        map_width, map_height = tile_map.size

        tile_list = []

        for y in range(map_height//tile_size):
            for x in range(map_width//tile_size):
                # loop through the tiles on the img
                croped_tile = tile_map.crop((x*tile_size, y*tile_size, x*tile_size+16, y*tile_size+16))
                tile_list.append(croped_tile)

        # convert them to textures
        return [arcade.Texture(name=n, image=img, hit_box_algorithm=None) for n, img in enumerate(tile_list)]

    def handle_assingment(self, sprite, tile, x, y):
        match tile["type"]:
            case (0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12):  # walls
                objects.Wall(sprite, self)
            case (13 | 14): # Buttons on | off
                objects.Button(sprite, tile, self)
            case (15 | 16): # Door closed | Door open
                objects.Door(sprite, tile, x, y, self)
            case (17 | 18 | 19): # Plates on| ("off" can't be default) | with box
                objects.Plate(sprite, tile, self)
            case (21):  # P1
                self.player.assing(sprite, 21, self)
                self.sec_player.set_sprite(sprite, 27)
            case (27):  # P2
                self.player.assing(sprite, 27, self)
                self.sec_player.set_sprite(sprite, 21)

    def generate_sprites(self):
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                texture = self.textures[tile["type"]]
                rotation = int(tile["rotation"])*90
                sprite = arcade.Sprite(
                    hit_box_algorithm=None,
                    texture=texture,
                    angle=rotation,
                    scale=self.scale,
                    center_x=x*self.tile_size*self.scale  # calculate width of the map
                    + (self.tile_size*self.scale)//2,  # offset the map by half a tile to account of center positions
                    center_y=self.screen_size[1]  # sub from the top of the screen to make the Corrds like in pygame
                    - y*self.tile_size*self.scale  # calculate height of the map
                    - (self.tile_size*self.scale)//2  # offset the map by half a tile to account of center positions
                )
                self.sprites.append(sprite)

                self.handle_assingment(sprite, tile, x, y)

    def load_map_data(self, map_name: str, player,sec_player, c_manager) -> None:
        """
        Load a tile map file from the resources/tilemaps folder
        :param str map_name: The name of the file without file extension
        :param float scaling: Factor by which the size of the map should be increased (default: 1)
        """
        # Loading the map
        self.map = json.load(open(f"./resources/tilemaps/{map_name}.json", "r"))["Map"]
        self.player = player
        self.sec_player = sec_player
        self.c_manager = c_manager
        self.generate_sprites()
        self.game.background = (43, 137, 137)

        self.loaded = True

    def update(self) -> None:
        """Updates the differend objects"""
        if self.loaded:
            for obj in self.needs_updates:
                obj.update()

    def trigger_interaction(self):
        pass

    def draw_layer(self) -> None:
        """
        Draws one or all layer of a map to the screen
        :param str map_name: The name of the map
        :param Layers layer: The layer to be drawn (defaults to all)
        """
        if not self.game._setup:
            arcade.draw_rectangle_filled((self.tile_size*len(self.map)*self.scale)//2,
                                         self.screen_size[1]-(self.tile_size*len(self.map)*self.scale)//2,
                                         self.tile_size*len(self.map)*self.scale,
                                         self.tile_size*len(self.map)*self.scale,
                                         (172, 182, 184))

            for sprite in self.sprites:
                sprite.draw(pixelated=True)

            if self.player.can_interact_with is not None:
                self.player.interact_e.draw(pixelated=True)
                
