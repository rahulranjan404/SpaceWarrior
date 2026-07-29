import pygame

pygame.mixer.init()

class AudioManager:

    def __init__(self):

        self.volume = 0.5

        self.sounds = {}

    def load(self, name, path):

        sound = pygame.mixer.Sound(path)
        sound.set_volume(self.volume)

        self.sounds[name] = sound

    def play(self, name):

        if name in self.sounds:
            self.sounds[name].play()

    def set_volume(self, volume):

        self.volume = volume

        for sound in self.sounds.values():
            sound.set_volume(volume)


audio = AudioManager()