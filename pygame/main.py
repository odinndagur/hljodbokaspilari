import pygame
import sys
from pygame import mixer
from mutagen.mp3 import MP3
import datetime
from xspf_lib import Playlist
import os

from display import Display
from audiobook import AudioBook
from player import Player
from misc import mapf





pygame.init()
mixer.init()

mixer.music.set_volume(0.2)

width, height = 320, 240

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255,0,0)
blue = (0, 0, 128)

display = pygame.display.set_mode((width, height))
oled = Display(display=display)
pygame.display.set_caption('Hljóðadót')

# font18 = pygame.font.Font('freesansbold.ttf', 18)
# font = pygame.font.Font('freesansbold.ttf', 24)


lotr_1 = AudioBook(
    short_name='LOTR',
    title='Lord of the Rings: The Fellowship of the Ring',
    author='J.R.R. Tolkien',
    chapters=Playlist.parse('/Users/odinndagur/Code/2023/hljodbokaspilari/pygame/Hringadróttins saga  1 24948/playlist.xspf'),
    folder_name='Hringadróttins saga  1 24948'
    )

book = lotr_1
player = Player(book=lotr_1,display=oled,pygame_display=display)



def main_loop():
    oled.fill(black)
    player.show()
    # oled.hline(0,100,320,white)
    # oled.fill_rectangle(20,20,100,180,red)

current_sound_length = player.book.chapters[book.current_chapter].duration


buttons = { 
    pygame.K_q: 'dogs-barking.mp3',
    pygame.K_w: 'Þegar ég verð 36.mp3',
    pygame.K_e: 'cat,screaming,a.mp3',
}

while True:
    main_loop()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
         
        # checking if keydown event happened or not
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            player.mouse_click(pos=pos)
        if event.type == pygame.KEYDOWN:
            if event.key in buttons:
                song_path = buttons[event.key]
                mixer.music.load(song_path)
                song = MP3(song_path)
                current_sound_length = song.info.length * 1000
                mixer.music.play()
                # showText(buttons[event.key])
            if event.key == pygame.K_SPACE:
                if mixer.music.get_busy():
                    # last_sound_offset = mixer.music.get_pos()
                    mixer.music.pause()
                else:
                    mixer.music.play()
                    # print(f'{last_sound_offset=}')



