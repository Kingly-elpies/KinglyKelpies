import arcade

class Player:
    def __init__(self, game, player_id):
        self.game = game
        self.id = player_id

        self.moving_speed = 64

        self.player = None

    def assing(self,sprite,s_id,map_manger):
        if self.id == 0 and s_id == 21:
            self.player = sprite
        elif self.id == 1 and s_id == 27:
            self.player = sprite

        self.map_manager = map_manger

    def move(self,m_x,m_y):
        temp_center_x = self.player.center_x + m_x
        temp_center_y = self.player.center_y + m_y

        if not self.map_manager.will_collide(temp_center_x,temp_center_y):
            self.player.center_x = temp_center_x
            self.player.center_y = temp_center_y

        

    def player_key_press(self, key, key_modifiers):
        match key:
            case (arcade.key.W|arcade.key.UP):
                self.move(0,self.moving_speed)
            case (arcade.key.S|arcade.key.DOWN):
                self.move(0,-self.moving_speed)
            case (arcade.key.A|arcade.key.LEFT):
                self.move(-self.moving_speed,0)
            case (arcade.key.D|arcade.key.RIGHT):
                self.move(self.moving_speed,0)
            case (arcade.key.E):
                    self.map_manager.get_door(2, 5).update_counter(-1)

    def player_key_release(self, key, key_modifiers):
        pass
        # match key:
        #     case (arcade.key.W|arcade.key.UP|arcade.key.S|arcade.key.DOWN):
        #         self.player.center_y = 0
        #     case (arcade.key.A|arcade.key.LEFT|arcade.key.D|arcade.key.RIGHT):
        #         self.player.change_x = 0
