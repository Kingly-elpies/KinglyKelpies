import os
import arcade


class Sounds:

    def __init__(self, game):
        self.game = game
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path1 = os.path.dirname(dir_path)
        print(dir_path, dir_path1)
        sound_folder = dir_path1 + r"/resources/sounds/"
        self.sound_array = {"Box": sound_folder + "box.mp3",
                            "Box": sound_folder + "box.mp3",
                            "Door": sound_folder + "door.mp3",
                            "Finish": sound_folder + "finish.mp3",
                            "Footstep": sound_folder + "footstep.mp3",
                            "Hole": sound_folder + "hole.mp3",
                            "Plate": sound_folder + "plate.mp3"}

    def sound(self, sound):
        sound_file = self.sound_array[sound]
        self.game.play_sound(sound_file)
