import arcade

class Wall:

    def __init__(self, sprite, map_manager):
        self.map_manager = map_manager

        self.sprite = sprite
        self.map_manager.collision.append(self)

class Button:

    def __init__(self,sprite,kwargs, x, y, map_manager):
        self.map_manager = map_manager

        self.sprite = sprite

        self.state = kwargs["state"]
        self.link_x,self.link_y = kwargs["link"]["x"], kwargs["link"]["y"]

        self.x = x
        self.y = y

        self.map_manager.interactables.append(self)
        self.map_manager.needs_wb_updates.append(self)

    def change_state(self):
        if self.state == 1: # button pressed
            texture = self.map_manager.textures[14]
            amount = -1
        else: # button un pressed
            texture = self.map_manager.textures[13]
            amount  = 1

        self.sprite.texture = texture #update texture
        self.map_manager.get_door(self.link_x,self.link_y).update_counter(amount) # update linked door

    def interact(self):
        self.state = (self.state + 1)%2
        self.change_state()
        self.map_manager.c_manager.send_message(f"[Button] {self.x},{self.y},{self.state}")

    def wb_update(self,update:str):
        if "[Button]" in update:
            x,y,state = update.replace("[Button] ", "").split(",")
            if (int(x),int(y)) == (self.x,self.y):
                self.state = int(state)
                self.change_state()

class Plate():

    def __init__(self,sprite,kwargs, x, y, map_manager):
        self.map_manager = map_manager

        self.sprite = sprite

        self.x = x
        self.y = y

        self.state = kwargs["state"]
        self.link_x,self.link_y = kwargs["link"]["x"], kwargs["link"]["y"]

        self.down = False
        self.forced = False

        self.map_manager.needs_updates.append(self)

    def change_state(self,texture_id,amount,down,state):
        self.sprite.texture = self.map_manager.textures[texture_id] #update own texture
        self.map_manager.get_door(self.link_x,self.link_y).update_counter(amount) # update linked door
    
        self.down = down
        self.state = state

    def collision(self)->bool:
        player_col = arcade.check_for_collision(self.sprite, self.map_manager.player.player)
        sec_player_col = arcade.check_for_collision(self.sprite, self.map_manager.sec_player.player)
        return bool(player_col + sec_player_col)

    def update(self):
        if self.collision() and not self.down:
            # Plate down if a player is on it
            self.change_state(18,-1,True,1)

        elif not self.collision() and self.down: # plate up
            # Plate up if he isn't
            self.change_state(17,1,False,0)




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
