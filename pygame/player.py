import pygame
from pygame import mixer
from misc import mapf

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255,0,0)
blue = (0, 0, 128)

class Player():
    def __init__(self, book, display, pygame_display):
        self.book = book
        self.display = display
        self.pygame_display = pygame_display
        self.size = pygame_display.get_size()

    def show(self):
        self.now_playing()

    def mouse_click(self,pos):
        mouse_x, mouse_y = pos
        pad = 20
        if (mouse_y > 120 - pad and mouse_y < 120 + pad): # horizontal line in the center
            if(mouse_x > 60 - pad and mouse_x < 60 + pad): #left arrow
                print('left')
                self.book.prev_chapter()
            if(mouse_x < 260 + pad and mouse_x > 260 - pad): #right arrow
                print('right')
                self.book.next_chapter()
            if(mouse_x > 160 - pad and mouse_x < 160 + pad): #play/pause button
                print('play/pause')
                self.book.toggle()
        if (mouse_y > 240 - 80 and mouse_y < 240 - 80 + 20 and mouse_x > 40 and mouse_x < 360 - 40): #progress bar
            selected_progress_val = mapf(mouse_x,80,360-80,0.0,1.0,clamped=True)
            self.book.seek(selected_progress_val)
            print(f'progress?, {selected_progress_val=}')
            
        print(pos)


    def showText(self,txt,x=160 ,y=120,size=24):
        font = pygame.font.Font('freesansbold.ttf', size=size)
        text = font.render(txt, True, white, black)
        textRect = text.get_rect()
        textRect.center = (x, y)
        self.pygame_display.blit(text,textRect)




    def progress_bar(self,x:int,y:int,width:int,height:int,color:int | tuple,progress:float):
        self.display.stroke_rectangle(x,y,width,height,color)
        self.display.fill_rectangle(x,y,width * progress,height,color)

    def book_title(self,title:str):
        self.showText(title,y=20)

    def convertMillis(self,millis):
        seconds=int(millis/1000)%60
        minutes=int(millis/(1000*60))%60
        hours=int(millis/(1000*60*60))%24
        return f'{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}'

    def play_button(self,x,y,size=20):
        self.display.vline(x=x-size/2,y=y-size/2,height=size,color=white)
        self.display.line(start_pos=(x-size/2,y-size/2),end_pos=(x+size/2,y),color=white)
        self.display.line(start_pos=(x-size/2,y+size/2),end_pos=(x+size/2,y),color=white)

    def pause_button(self,x,y,size=20):
        self.display.stroke_rectangle(x-size/2,y-size/2,size/3,size,white)
        self.display.stroke_rectangle(x-size/2 + (size/3 * 2),y-size/2,size/3,size,white)

    def now_playing(self):
        # self.display.stroke_rectangle(10,10,self.size[0]-20,self.size[1]-20,white)
        self.display.stroke_rectangle(20,20,280,200,white)
        # print(current_pos,current_sound_length)

        current_pos = pygame.mixer.music.get_pos()
        current_sound_length = self.book.chapters[self.book.current_chapter].duration
        
        self.progress_bar(40, 240 - 80, 320-80, 20, white,current_pos / (current_sound_length+0.01))
        
        self.showText(self.convertMillis(current_pos),x=60,y=200,size=16)
        self.showText(f'-{self.convertMillis(self.book.chapters[self.book.current_chapter].duration-current_pos)}',x=320-60,y=200,size=16)
        self.book_title(self.book.short_name)
        self.showText(f'{self.book.current_chapter + 1}/{len(self.book.chapters)}',y=50,size=18)
        self.showText(self.book.chapters[self.book.current_chapter].title,y=70,size=18)
        self.showText('>',x=260)
        self.showText('<',x=60)
        if mixer.music.get_busy():
            self.pause_button(x=160,y=120)
        else:
            self.play_button(x=160,y=120)


        self.display.show()
