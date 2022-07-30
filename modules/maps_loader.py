import arcade
import json
from PIL import Image


class MapManager:
    def __init__(self, game,screen_size = (800,600)) -> None:
        self.game = game
        self.map = [[]]
        self.scale = 4
        self.tile_size = 16
        self.screen_size = screen_size

        self.textures = self.load_textures("./resources/tilesets/KelpiesTileset.png")
        self.sprites = []

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

    def handle_assingment(self,sprite,tile):
        match tile["type"]:
            case (21):
                self.player.set_sprite(sprite,21)
                self.sec_player.set_sprite(sprite, 27)
            case (27):
                self.player.set_sprite(sprite,27)
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
                    center_x=
                        x*self.tile_size*self.scale # calculate width of the map
                        +(self.tile_size*self.scale)//2, # offset the map by half a tile to account of center positions
                    center_y=
                        self.screen_size[1] # sub from the top of the screen to make the Corrds like in pygame
                        -y*self.tile_size*self.scale # calculate height of the map
                        -(self.tile_size*self.scale)//2 # offset the map by half a tile to account of center positions
                )
                self.sprites.append(sprite)

                self.handle_assingment(sprite, tile)

    def load_map_data(self, map_name: str, player, sec_player) -> None:
        """
        Load a tile map file from the resources/tilemaps folder
        :param str map_name: The name of the file without file extension
        :param float scaling: Factor by which the size of the map should be increased (default: 1)
        """
        # Loading the map
        self.map = json.load(open(f"./resources/tilemaps/{map_name}.json", "r"))["Map"]
        self.player = player
        self.sec_player = sec_player
        self.generate_sprites()
        self.game.background = (43,137,137)

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
                                            (172,182,184))

            for sprite in self.sprites:
                sprite.draw(pixelated = True)
