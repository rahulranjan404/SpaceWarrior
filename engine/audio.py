from unicodedata import name
import settings
import pygame

pygame.mixer.init()

class AudioManager:

    def __init__(self):

        self.volume = 0.5

        self.sounds = {}

        self.soundenabled = settings.soundenabled
        self.musicenabled = settings.musicenabled

    def load(self, name, path):
       

        sound = pygame.mixer.Sound(path)
        sound.set_volume(self.volume)

        self.sounds[name] = sound

    def play(self, name):
        if settings.soundenabled == True :

            if name in self.sounds:
                self.sounds[name].play()

    def set_volume(self, volume):

        self.volume = volume

        for sound in self.sounds.values():
            sound.set_volume(volume)

    def play_loop(self, name):
        if settings.musicenabled == True:
            if settings.soundenabled == False and name == "alive":
                pass
            else:
                if name in self.sounds:
                    self.sounds[name].play(loops=-1)
        


    def stop(self, name):

        if name in self.sounds:
            self.sounds[name].stop()


audio = AudioManager()