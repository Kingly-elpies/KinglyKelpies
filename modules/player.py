import arcade
from PIL import ImageOps

class Player:
    def __init__(self, game, player_id):
        self.game = game
        self.id = player_id

        self.moving_speed = 64

        self.player = None

        self.direction = "left" 

        self.can_interact_with = None
        self.e_offset = (0,48)

    def get_textures(self):
        if self.id == 0:
            textures = self.map_manager.textures[21:24]
        else:
            textures = self.map_manager.textures[27:30]
        fliped = ImageOps.mirror(textures[0].image)
        textures.append(arcade.Texture(name=f"fliped-{self.id}", image=fliped, hit_box_algorithm=None))
        return textures

    def assing(self,sprite,s_id,map_manger):
        if self.id == 0 and s_id == 21:
            self.player = sprite
        elif self.id == 1 and s_id == 27:
            self.player = sprite

        self.map_manager = map_manger
        self.map_manager.needs_updates.append(self)
        self.textures = self.get_textures()

        self.interact_e = arcade.Sprite(
                    hit_box_algorithm=None,
                    texture=self.map_manager.textures[37],
                    scale=(self.map_manager.scale//4)*3,
                    center_x=0,
                    center_y=0)

    def get_pos(self):
        return (self.player.center_x, self.player.center_y)

    def facing(self,direction):
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
                

    def move(self,m_x,m_y):
        temp_center_x = self.player.center_x + m_x
        temp_center_y = self.player.center_y + m_y

        if not self.map_manager.will_collide(temp_center_x,temp_center_y):
            self.player.center_x = temp_center_x
            self.player.center_y = temp_center_y

    def run_interact(self):
        if self.can_interact_with is not None:
            self.can_interact_with.interact()

        

    def player_key_press(self, key, key_modifiers):
        match key:
            case (arcade.key.W|arcade.key.UP):
                self.move(0,self.moving_speed); self.facing("up")
            case (arcade.key.S|arcade.key.DOWN):
                self.move(0,-self.moving_speed); self.facing("down")
            case (arcade.key.A|arcade.key.LEFT):
                self.move(-self.moving_speed,0); self.facing("left")
            case (arcade.key.D|arcade.key.RIGHT):
                self.move(self.moving_speed,0); self.facing("right")
            case (arcade.key.E|arcade.key.SPACE):
                self.run_interact()
            case (arcade.key.X):
                    self.map_manager.get_door(2, 5).update_counter(-1)

    def update(self):
        found = False
        for interactable in self.map_manager.interactables:
            if arcade.check_for_collision(self.player, interactable.sprite):
                self.can_interact_with = interactable
                self.interact_e.center_x = self.get_pos()[0] + self.e_offset[0]
                self.interact_e.center_y = self.get_pos()[1] + self.e_offset[1]
                found = True
                break

        if not found:
            self.can_interact_with = None

    def player_key_release(self, key, key_modifiers):
        pass
        # match key:
        #     case (arcade.key.W|arcade.key.UP|arcade.key.S|arcade.key.DOWN):
        #         self.player.center_y = 0
        #     case (arcade.key.A|arcade.key.LEFT|arcade.key.D|arcade.key.RIGHT):
        #         self.player.change_x = 0
