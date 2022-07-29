class Wall:

    def __init__(self, sprite, map_manager):
        self.map_manager = map_manager

        self.sprite = sprite
        self.map_manager.collision.append(self)


class Door:

    def __init__(self, sprite, kwargs, x, y, map_manager):
        self.map_manager = map_manager

        self.sprite = sprite
        self.map_manager.collision.append(self)
        self.map_manager.doors.append(self)

        self.x = x
        self.y = y
        
        self.counter = kwargs["counter"]
        self.open = False

    def update_counter(self, amount):
        self.counter += amount

        if amount <= 0 and not self.open:
            # Open the door by removing collison and changing the sprite

            self.sprite.texture = self.map_manager.textures[16]
            self.map_manager.collision.remove(self)
        elif amount > 0 and self.open:
            # Close the door by adding collision and chnaging the sprite

            self.sprite.texture = self.map_manager.textures[15]
            self.map_manager.collision.append(self)
