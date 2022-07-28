import arcade

class Player:
    def __init__(self, game, player_sprite):
        self.game = game
        self.player = player_sprite
        # Setting the PlayerSpeed (this should be modified)
        self.moving_speed = 5
        # Getting the Walls/Layers from the game level
        self.layers = self.game.maps_loader.sprite_lists[self.game.maps_loader.map_name]
        self.walls = self.layers["Ground"]
        # Initializing a TopDown-WallCollision PhysicsEngine
        self.physics_engine = arcade.PhysicsEngineSimple(player_sprite=self.player, walls=arcade.SpriteList())
        self.game.physics_engines.append(self.physics_engine)

    def player_key_press(self, key, key_modifiers):
        match key:
            case (arcade.key.W|arcade.key.UP):
                self.player.change_y = self.moving_speed
            case (arcade.key.S|arcade.key.DOWN):
                self.player.change_y = -self.moving_speed
            case (arcade.key.A|arcade.key.LEFT):
                self.player.change_x = -self.moving_speed
            case (arcade.key.D|arcade.key.RIGHT):
                self.player.change_x = self.moving_speed

    def player_key_release(self, key, key_modifiers):
        match key:
            case (arcade.key.W|arcade.key.UP|arcade.key.S|arcade.key.DOWN):
                self.player.change_y = 0
            case (arcade.key.A|arcade.key.LEFT|arcade.key.D|arcade.key.RIGHT):
                self.player.change_x = 0
