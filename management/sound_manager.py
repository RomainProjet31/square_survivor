from pygame import mixer

__SOUND_PATH = "assets/sounds/"


def play(sound):
    mixer.music.load(__SOUND_PATH + sound)
    mixer.music.play()
