import arcade

class Player:
    def __init__(self, game, player_id):
        self.game = game
        self.id = player_id

        self.moving_speed = 64

        self.player = None

    def set_sprite(self,sprite,s_id):
        if self.id == 0 and s_id == 21:
            self.player = sprite
        elif self.id == 1 and s_id == 27:
            self.player = sprite


    def player_key_press(self, key, key_modifiers):
        match key:
            case (arcade.key.W|arcade.key.UP):
                self.player.center_y += self.moving_speed
            case (arcade.key.S|arcade.key.DOWN):
                self.player.center_y += -self.moving_speed
            case (arcade.key.A|arcade.key.LEFT):
                self.player.center_x += -self.moving_speed
            case (arcade.key.D|arcade.key.RIGHT):
                self.player.center_x += self.moving_speed

        self.game.c_manager.send_message(f"[Walk] {self.player.center_x},{self.player.center_y}")

    def player_key_release(self, key, key_modifiers):
        pass

class RobotPlayer:
    def __init__(self, game, player_id):
        self.game = game
        # Getting the Oposite of the PLayersNumber (0=1, 1=0)
        self.id = int(not(player_id))

        self.player = None

    def set_sprite(self, sprite, s_id):
        if self.id == 0 and s_id == 27:
            self.player = sprite
        elif self.id == 1 and s_id == 21:
            self.player = sprite
