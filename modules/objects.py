import arcade
from datetime import datetime

class Blank:

    def __init__(self, sprite, x, y, map_manager):
        self.map_manager = map_manager
        self.sprite = sprite

        self.x = x
        self.y = y

        self.creation = datetime.now().timestamp()
        self.map_manager.all_tiles.append(self)

    def delete_references(self):
        for l in self.map_manager.list_of_lists:
            try:
                if self in l:
                    l.remove(self)
                
                elif self.sprite in l:
                    l.remove(self.sprite)
            except AttributeError:
                pass

    def clean(self):
        for tile in self.map_manager.all_tiles:
            if arcade.check_for_collision(self.sprite, tile.sprite):
                if (tile.x,tile.y) == (self.x,self.y) and tile.creation < self.creation and type(tile) is type(self):
                    self.delete_references()

class Wall(Blank):

    def __init__(self, sprite, x, y, map_manager):
        super().__init__(sprite, x, y, map_manager)
        self.map_manager.collision.append(self)


class Button(Blank):

    def __init__(self, sprite, kwargs, x, y, map_manager):
        super().__init__(sprite, x, y, map_manager)

        self.state = kwargs["state"]
        if type(kwargs["link"]) is list:
            self.link_list = True
        else:
            self.link_list = False

        self.link = kwargs["link"]

        self.map_manager.interactables.append(self)
        self.map_manager.needs_wb_updates.append(self)

    def change_state(self):
        if self.state == 1:  # button pressed
            texture = self.map_manager.textures[14]
            amount = -1
        else:  # button un pressed
            texture = self.map_manager.textures[13]
            amount = 1

        self.sprite.texture = texture  # update texture
        self.run_door(amount)

    def run_door(self,amount):
        if self.link_list:
            for link in self.link:
                x,y = link["x"],link["y"]
                self.map_manager.get_door(x, y).update_counter(amount)
        else:
            x,y = self.link["x"],self.link["y"]
            self.map_manager.get_door(x, y).update_counter(amount)


    def interact(self, who):
        self.state = (self.state + 1) % 2
        self.change_state()
        self.map_manager.c_manager.send_message(f"[Button] {self.x},{self.y},{self.state}")

    def wb_update(self, update: str):
        if "[Button]" in update:
            x, y, state = update.replace("[Button] ", "").split(",")
            if (int(x), int(y)) == (self.x, self.y):
                self.state = int(state)
                self.change_state()


class Plate(Blank):

    def __init__(self, sprite, kwargs, x, y, map_manager):
        super().__init__(sprite, x, y, map_manager)

        self.state = kwargs["state"]
        if type(kwargs["link"]) is list:
            self.link_list = True
        else:
            self.link_list = False

        self.link = kwargs["link"]

        self.down = False
        self.forced = False

        self.map_manager.needs_updates.append(self)
        self.map_manager.plates.append(self)

    def run_door(self,amount):
        if self.link_list:
            for link in self.link:
                x,y = link["x"],link["y"]
                self.map_manager.get_door(x, y).update_counter(amount)
        else:
            x,y = self.link["x"],self.link["y"]
            self.map_manager.get_door(x, y).update_counter(amount)


    def change_state(self, texture_id, amount, down, state):
        self.sprite.texture = self.map_manager.textures[texture_id]  # update own texture
        self.run_door(amount)  # update linked door

        self.down = down
        self.state = state

    def collision(self) -> bool:
        player_col = arcade.check_for_collision(self.sprite, self.map_manager.player.player)
        sec_player_col = arcade.check_for_collision(self.sprite, self.map_manager.sec_player.player)
        box_collision = False
        for box in self.map_manager.boxes:
            if arcade.check_for_collision(self.sprite, box.sprite):
                box_collision = True

        return bool(player_col + sec_player_col + box_collision)

    def update(self):
        if self.collision() and not self.down:
            # Plate down if a player is on it
            self.change_state(18, -1, True, 1)

        elif not self.collision() and self.down:  # plate up
            # Plate up if he isn't
            self.change_state(17, 1, False, 0)


class Door(Blank):

    def __init__(self, sprite, kwargs, x, y, map_manager, inverted = False):
        super().__init__(sprite, x, y, map_manager)

        self.counter = int(kwargs["counter"])

        self.inverted = inverted

        self.open = self.inverted
        
        if not self.open: self.map_manager.collision.append(self);

        self.map_manager.doors.append(self)

    def check_open(self):
        if not self.inverted:
            return self.counter <= 0
        else:
            return self.counter > 0

    def update_counter(self, amount):
        self.counter += amount

        if self.check_open() and not self.open:
            # Open the door by removing collison and changing the sprite

            self.sprite.texture = self.map_manager.textures[16]

            self.map_manager.collision.remove(self)

            self.open = True

        elif not self.check_open() and self.open:
            # Close the door by adding collision and chnaging the sprite

            self.sprite.texture = self.map_manager.textures[15]

            self.map_manager.collision.append(self)

            self.open = False


class Box(Blank):

    def __init__(self, sprite, x, y, map_manager):
        super().__init__(sprite, x, y, map_manager)

        self.map_manager.boxes.append(self)
        self.map_manager.box_obj.append(self)

        self.map_manager.needs_wb_updates.append(self)
        # self.map_manager.needs_updates.append(self)

        self.picked_up = False

    def pick_up(self, who):
        if not self.picked_up and not who.has_box:
            who.pick_up(self)
            self.picked_up = True
            self.hide()
            self.map_manager.c_manager.send_message(f"[Box] {self.x},{self.y},1")

    # def update(self):
    #     if not self.picked_up:
    #         for box in self.map_manager.boxes:
    #             if arcade.check_for_collision(self.sprite, box.sprite):
    #                 if (box.x,box.y) == (self.x,self.y) and box.creation < self.creation:
    #                     self.map_manager.boxes.remove(self)
    #                     self.map_manager.box_obj.remove(self)
    #                     self.map_manager.needs_wb_updates.remove(self)
    #                     self.map_manager.needs_updates.remove(self)
    #                     self.map_manager.sprites.remove(self.sprite)

    def hide(self):
        self.sprite.texture = self.map_manager.textures[33]
        self.map_manager.boxes.remove(self)

    def show(self, who):
        self.sprite.center_x, self.sprite.center_y, = who.player.center_x, who.player.center_y
        self.getSpriteCollison()
        self.map_manager.boxes.append(self)

    def put_down(self, who):
        if self.picked_up:
            self.picked_up = False
            self.show(who)
            self.map_manager.c_manager.send_message(f"[Box] {self.x},{self.y},0")

    def getSpriteCollison(self):
        collides = False
        for plate in self.map_manager.plates:
            if arcade.check_for_collision(self.sprite, plate.sprite):
                collides = True

        if collides:
            self.sprite.texture = self.map_manager.textures[19]
        else:
            self.sprite.texture = self.map_manager.textures[20]

    def wb_update(self, update:str):
        if "[Box]" in update:
            x,y,state = update.replace("[Box] ", "").split(",")
            if (int(x),int(y)) == (self.x,self.y):
                if state == "1":
                    self.hide()
                    self.map_manager.sec_player.sprite_update_box()
                else:
                    self.show(self.map_manager.sec_player)
                    self.map_manager.sec_player.sprite_update_box()

class Hole(Blank):

    def __init__(self, sprite, x, y, map_manager):
        super().__init__(sprite, x, y, map_manager)

        self.map_manager.needs_updates.append(self)
        self.map_manager.collision.append(self)

    def update(self):
        for box in self.map_manager.boxes:
            if arcade.get_distance_between_sprites(self.sprite, box.sprite) < self.sprite.width+1 and not box.picked_up:
                self.sprite.texture = self.map_manager.textures[35]
                self.map_manager.needs_updates.remove(self)
                self.map_manager.collision.remove(self)
                self.map_manager.needs_wb_updates.remove(box)
                self.map_manager.boxes.remove(box)
                self.map_manager.box_obj.remove(box)
                self.map_manager.sprites.remove(box.sprite)

class Goal(Blank):

    def __init__(self, sprite, x, y, map_manager):
        super().__init__(sprite, x, y, map_manager)

        self.map_manager.goals.append(self)
        self.map_manager.needs_updates.append(self)

    def update(self):
        if self.map_manager.game.host:
            if arcade.check_for_collision(self.sprite, self.map_manager.player.player) and not self.map_manager.player.won :
                self.map_manager.player.won = True

            if arcade.check_for_collision(self.sprite, self.map_manager.sec_player.player) and not self.map_manager.sec_player.won:
                self.map_manager.sec_player.won = True