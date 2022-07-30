import arcade

class Wall:

    def __init__(self, sprite, map_manager):
        self.map_manager = map_manager

        self.sprite = sprite
        self.map_manager.collision.append(self)

class Button:

    def __init__(self,sprite,kwargs, map_manager):
        self.map_manager = map_manager

        self.sprite = sprite

        self.state = kwargs["state"]
        self.link_x,self.link_y = kwargs["link"]["x"], kwargs["link"]["y"]

        self.map_manager.interactables.append(self)

    def interact(self):
        self.state = (self.state + 1)%2

        if self.state == 1: # button pressed
            texture = self.map_manager.textures[14]
            amount = -1
        else: # button un pressed
            texture = self.map_manager.textures[13]
            amount  = 1

        self.sprite.texture = texture #update texture
        self.map_manager.get_door(self.link_x,self.link_y).update_counter(amount) # update linked door

class Plate():

    def __init__(self,sprite,kwargs, map_manager):
        self.map_manager = map_manager

        self.sprite = sprite

        self.state = kwargs["state"]
        self.link_x,self.link_y = kwargs["link"]["x"], kwargs["link"]["y"]

        self.down = False

        self.map_manager.needs_updates.append(self)

    def update(self):
        if arcade.check_for_collision(self.sprite, self.map_manager.player.player) and not self.down:
            # Plate down if a player is on it

            self.sprite.texture = self.map_manager.textures[18]
            self.map_manager.get_door(self.link_x,self.link_y).update_counter(-1) # update linked door

            self.down = True

        elif not arcade.check_for_collision(self.sprite, self.map_manager.player.player) and self.down: # plate up
            # Plate up if he isn't

            self.sprite.texture = self.map_manager.textures[17]
            self.map_manager.get_door(self.link_x,self.link_y).update_counter(1)
            self.down = False





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
            self.open = True
        elif amount > 0 and self.open:
            # Close the door by adding collision and chnaging the sprite

            self.sprite.texture = self.map_manager.textures[15]
            self.map_manager.collision.append(self)
            self.open = False
