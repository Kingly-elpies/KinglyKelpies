import arcade
from PIL import ImageOps
from datetime import datetime


class Player:
    """ The player wich is controlled by the Keyboard, on the other side it is represented as a RobotPlayer"""

    def __init__(self, game, player_id):
        self.game = game
        self.id = player_id # 0 for blue robot 1 for red robot
        
        self.moving_speed = 64

        self.player = None # The sprite of the player
        self.game.camera = arcade.Camera(self.game._width, self.game._height) # This camera follows the player

        self.direction = "left" # the direction the player is looking

        self.can_interact_with = None # Set as an value if the player stands of smth. he cab interact with, like a button
        self.e_offset = (0, 48) # The offset the e keystroke sprite has from the center of the player
        self.q_offset = (0, 48) # The offset the q keystroke sprite has from the center of the player

        self.can_pick_up = None # The box the player can pick up if he stands on it
        self.has_box = False
        self.box = None # The box object he picked up

        self.won = False # True if walked over a goal

        self.check_collisions = True # Used in debug to walk through walls press J do disable

    def center_camera_to_player(self):
        screen_center_x = self.player.center_x - (self.game.camera.viewport_width / 2)
        screen_center_y = self.player.center_y - (self.game.camera.viewport_height / 2)
        player_centered = screen_center_x, screen_center_y

        self.game.camera.move_to(player_centered)

    def get_textures(self, offset=0):
        """ Returns the 4 sprites that are connected to the id (0 for blue | 1 for red ).
        The offset is used to also load the textures with the box"""

        if self.id == 0:
            textures = self.map_manager.textures[21+offset:24+offset] # 21 is tile number of the first tile for the blue character
        else:
            textures = self.map_manager.textures[27+offset:30+offset] # 27 is tile number of the first tile for the blue character
        # textures = [lokking left, looking up, looking down]


        # Flips the texture sprite to have a sprite for walking left
        fliped = ImageOps.mirror(textures[0].image)
        textures.append(arcade.Texture(name=f"fliped-{self.id}-{offset}", image=fliped, hit_box_algorithm=None))
        return textures

    def assing(self, sprite, map_manger):
        self.player = sprite

        self.map_manager = map_manger
        self.map_manager.needs_updates.append(self)
        self.textures = self.get_textures()
        self.secondary_textures = self.get_textures(3)

        self.interact_e = arcade.Sprite(
            hit_box_algorithm=None,
            texture=self.map_manager.textures[37],
            scale=(self.map_manager.scale//4)*3,
            center_x=0,
            center_y=0)

        self.interact_q = arcade.Sprite(
            hit_box_algorithm=None,
            texture=self.map_manager.textures[38],
            scale=(self.map_manager.scale//4)*3,
            center_x=0,
            center_y=0)

        self.won = False

    def get_pos(self):
        return (self.player.center_x, self.player.center_y)

    def facing(self, direction):
        self.direction = direction

        match direction:
            case ("left"):
                self.player.texture = self.textures[0]
            case ("up"):
                self.player.texture = self.textures[1]
            case ("down"):
                self.player.texture = self.textures[2]
            case ("right"):
                self.player.texture = self.textures[3]

        self.game.c_manager.send_message(f"[Direction] {direction}")

    def move(self, m_x, m_y):
        temp_center_x = self.player.center_x + m_x
        temp_center_y = self.player.center_y + m_y

        if not self.map_manager.will_collide(temp_center_x, temp_center_y) or not self.check_collisions:
            self.player.center_x = temp_center_x
            self.player.center_y = temp_center_y

            self.game.sounds.sound("Footstep")

            self.game.c_manager.send_message(f"[Walk] {self.player.center_x},{self.player.center_y}")

    def run_interact(self):
        if self.can_interact_with is not None:
            self.can_interact_with.interact(self)

    def handle_box(self):
        if self.can_pick_up is not None and not self.has_box:
            self.can_pick_up.pick_up(self)
        elif self.has_box:
            self.put_down()

    def player_key_press(self, key, key_modifiers):
        match key:
            case (arcade.key.W | arcade.key.UP):
                self.move(0, self.moving_speed)
                self.facing("up")
            case (arcade.key.S | arcade.key.DOWN):
                self.move(0, -self.moving_speed)
                self.facing("down")
            case (arcade.key.A | arcade.key.LEFT):
                self.move(-self.moving_speed, 0)
                self.facing("left")
            case (arcade.key.D | arcade.key.RIGHT):
                self.move(self.moving_speed, 0)
                self.facing("right")
            case (arcade.key.E | arcade.key.SPACE):
                self.run_interact()
            case (arcade.key.Q):
                self.handle_box()
            case (arcade.key.R):
                self.map_manager.load_map_data(
                    self.map_manager.map_name, self, self.map_manager.sec_player, self.map_manager.c_manager)
            case (arcade.key.J):
                self.check_collisions = not self.check_collisions

    def swap_textures(self):
        old_textures = self.textures.copy()
        self.textures = self.secondary_textures
        self.secondary_textures = old_textures

    def pick_up(self, box):
        if not self.has_box:
            self.has_box = True
            self.box = box
            self.swap_textures()
            self.facing(self.direction)

            # self.game.c_manager.send_message(f"[Box]")

    def put_down(self):
        if self.has_box:
            self.swap_textures()
            self.facing(self.direction)

            self.box.put_down(self)

            self.has_box = False
            self.box = None

            # self.game.c_manager.send_message(f"[Box]")

    def update(self):
        self.center_camera_to_player()

        found = False

        for interactable in self.map_manager.interactables:
            if arcade.check_for_collision(self.player, interactable.sprite):
                self.can_interact_with = interactable

                self.e_offset = (-24, 48) if self.has_box or self.can_pick_up else (0, 48)

                self.interact_e.center_x = self.get_pos()[0] + self.e_offset[0]
                self.interact_e.center_y = self.get_pos()[1] + self.e_offset[1]
                found = True
                break

        if not found:
            self.can_interact_with = None

        found_box = False
        for box in self.map_manager.boxes:
            if arcade.check_for_collision(self.player, box.sprite):
                self.can_pick_up = box

                self.q_offset = (24, 48) if found else (0, 48)

                self.interact_q.center_x = self.get_pos()[0] + self.q_offset[0]
                self.interact_q.center_y = self.get_pos()[1] + self.q_offset[1]
                found_box = True
                break

        if not found_box:
            self.can_pick_up = None

        if self.has_box:
            self.q_offset = (24, 48) if found else (0, 48)

            self.interact_q.center_x = self.get_pos()[0] + self.q_offset[0]
            self.interact_q.center_y = self.get_pos()[1] + self.q_offset[1]


class RobotPlayer:

    def __init__(self, game, player_id):
        self.game = game
        # Getting the Oposite of the PLayersNumber (0=1, 1)
        self.id = int(not(player_id))

        self.player = None

        self.won = False

    def get_textures(self, offset=0):
        if self.id == 0:
            textures = self.map_manager.textures[21+offset:24+offset]
        else:
            textures = self.map_manager.textures[27+offset:30+offset]
        fliped = ImageOps.mirror(textures[0].image)
        textures.append(arcade.Texture(name=f"fliped-{self.id}-{offset}", image=fliped, hit_box_algorithm=None))
        return textures

    def assing(self, sprite, map_manager):
        self.player = sprite

        self.map_manager = map_manager
        self.map_manager.needs_wb_updates.append(self)
        self.textures = self.get_textures()
        self.secondary_textures = self.get_textures(3)

        self.won = False

    def sprite_update_box(self):
        old_textures = self.textures.copy()
        self.textures = self.secondary_textures
        self.secondary_textures = old_textures
        self.facing(self.direction)

    def facing(self, direction):
        self.direction = direction

        match direction:
            case ("left"):
                self.player.texture = self.textures[0]
            case ("up"):
                self.player.texture = self.textures[1]
            case ("down"):
                self.player.texture = self.textures[2]
            case ("right"):
                self.player.texture = self.textures[3]

    def wb_update(self, update):
        if "[Walk]" in update:
            x, y = update.replace("[Walk] ", "").split(",")
            self.player.center_x, self.player.center_y = int(x), int(y)

        elif "[Direction]" in update:
            direction = update.replace("[Direction] ", "")
            self.facing(direction)
