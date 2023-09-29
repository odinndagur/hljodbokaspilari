import pygame
import sys
from pygame import mixer
from mutagen.mp3 import MP3
import datetime
from display import Display
from xspf_lib import Playlist
import os

def mapf(val, in_min, in_max, out_min, out_max, clamped=False):
    new_val = (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    if clamped:
        if new_val < 0:
            new_val = 0
        if new_val > out_max:
            new_val = out_max
    return new_val


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


class AudioBook:
    def __init__(self,short_name,title,author,chapters,folder_name):
        self.short_name = short_name
        self.title = title
        self.author = author
        self.chapters = chapters
        self.current_chapter = 10
        self.folder_name=folder_name
        self.playing = False
        self.load_chapter(self.current_chapter)
        self.last_position_millis = 0

    def load_chapter(self,chapter_number):
        print(self.folder_name,self.chapters[chapter_number].location[0])
        current_chapter_file = os.path.join(self.folder_name,self.chapters[chapter_number].location[0])
        mixer.music.load(current_chapter_file)

    
    def prev_chapter(self):
        mixer.music.pause()
        self.current_chapter = self.current_chapter - 1 if self.current_chapter > 0 else self.current_chapter
        self.load_chapter(self.current_chapter)
        mixer.music.play()

    def next_chapter(self):
        mixer.music.pause()
        self.current_chapter = self.current_chapter + 1 if self.current_chapter < len(self.chapters) - 1 else self.current_chapter
        self.load_chapter(self.current_chapter)
        mixer.music.play()

    def seek(self, progress):
        if not self.playing:
            self.toggle()
        new_position_millis = progress * self.chapters[self.current_chapter].duration
        self.last_position_millis = new_position_millis
        mixer.music.set_pos(new_position_millis / 1000)

    def toggle(self):
        if self.playing:
            self.last_position_millis = mixer.music.get_pos()
            mixer.music.pause()
        else:
            mixer.music.play(start=self.last_position_millis/1000.0)
        self.playing = not self.playing

class Player():
    def __init__(self):
        pass

    def display(self):
        self.now_playing()

    def mouse_click(self,pos):
        mouse_x, mouse_y = pos
        pad = 20
        if (mouse_y > 120 - pad and mouse_y < 120 + pad): # horizontal line in the center
            if(mouse_x > 60 - pad and mouse_x < 60 + pad): #left arrow
                print('left')
                book.prev_chapter()
            if(mouse_x < 260 + pad and mouse_x > 260 - pad): #right arrow
                print('right')
                book.next_chapter()
            if(mouse_x > 160 - pad and mouse_x < 160 + pad): #play/pause button
                print('play/pause')
                book.toggle()
        if (mouse_y > 240 - 80 and mouse_y < 240 - 80 + 20 and mouse_x > 40 and mouse_x < 360 - 40): #progress bar
            selected_progress_val = mapf(mouse_x,80,360-80,0.0,1.0,clamped=True)
            book.seek(selected_progress_val)
            print(f'progress?, {selected_progress_val=}')
            
        print(pos)


    def showText(self,txt,x=160 ,y=120,size=24):
        font = pygame.font.Font('freesansbold.ttf', size=size)
        text = font.render(txt, True, white, black)
        textRect = text.get_rect()
        textRect.center = (x, y)
        display.blit(text,textRect)




    def progress_bar(self,x:int,y:int,width:int,height:int,color:int | tuple,progress:float):
        oled.stroke_rectangle(x,y,width,height,color)
        oled.fill_rectangle(x,y,width * progress,height,color)

    def book_title(self,title:str):
        self.showText(title,y=20)

    def convertMillis(self,millis):
        seconds=int(millis/1000)%60
        minutes=int(millis/(1000*60))%60
        hours=int(millis/(1000*60*60))%24
        return f'{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}'

    def play_button(self,x,y,size=20):
        oled.vline(x=x-size/2,y=y-size/2,height=size,color=white)
        oled.line(start_pos=(x-size/2,y-size/2),end_pos=(x+size/2,y),color=white)
        oled.line(start_pos=(x-size/2,y+size/2),end_pos=(x+size/2,y),color=white)

    def pause_button(self,x,y,size=20):
        oled.stroke_rectangle(x-size/2,y-size/2,size/3,size,white)
        oled.stroke_rectangle(x-size/2 + (size/3 * 2),y-size/2,size/3,size,white)

    def now_playing(self):
        oled.stroke_rectangle(20,20,280,200,white)
        # print(current_pos,current_sound_length)

        current_pos = pygame.mixer.music.get_pos()
        
        self.progress_bar(40, 240 - 80, 320-80, 20, white,current_pos / (current_sound_length+0.01))
        
        self.showText(self.convertMillis(current_pos),x=60,y=200,size=16)
        self.showText(f'-{self.convertMillis(book.chapters[book.current_chapter].duration-current_pos)}',x=320-60,y=200,size=16)
        self.book_title(book.short_name)
        self.showText(f'{book.current_chapter + 1}/{len(book.chapters)}',y=50,size=18)
        self.showText(book.chapters[book.current_chapter].title,y=70,size=18)
        self.showText('>',x=260)
        self.showText('<',x=60)
        if mixer.music.get_busy():
            self.pause_button(x=160,y=120)
        else:
            self.play_button(x=160,y=120)


        oled.show()


lotr_1 = AudioBook(
    short_name='LOTR',
    title='Lord of the Rings: The Fellowship of the Ring',
    author='J.R.R. Tolkien',
    chapters=Playlist.parse('/Users/odinndagur/Code/2023/hljodbokaspilari/pygame/Hringadróttins saga  1 24948/playlist.xspf'),
    folder_name='Hringadróttins saga  1 24948'
    )

book = lotr_1

player = Player()



def main_loop():
    oled.fill(black)
    player.display()
    # oled.hline(0,100,320,white)
    # oled.fill_rectangle(20,20,100,180,red)

current_sound_length = book.chapters[book.current_chapter].duration


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



