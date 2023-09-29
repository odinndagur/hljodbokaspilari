import pygame

class Display:
    def __init__(self,display):
        self.display = display

    def  fill(self, color: int | tuple = 0):
        self.display.fill(color)

    def fill_rectangle(self,x: int, y: int, width: int, height: int, color: int | tuple):
        pygame.draw.rect(
            surface=self.display,
            color=color,
            rect=pygame.Rect(x,y,width,height)
                         )
    
    def stroke_rectangle(self,x: int, y: int, width: int, height: int, color: int | tuple):
        self.hline(x=x,y=y,width=width,color=color)
        self.hline(x=x,y=height + y,width=width,color=color)
        self.vline(x=x,y=y,height=height,color=color)
        self.vline(x=width + x,y=y,height=height,color=color)

    def line(self,start_pos:tuple,end_pos:tuple,color:int | tuple):
        pygame.draw.line(surface=self.display,color=color,start_pos=start_pos,end_pos=end_pos)

    def hline(self, x: int, y: int, width: int, color: int | tuple):
        pygame.draw.line(surface=self.display,color=color,start_pos=(x,y),end_pos=(x+width,y))
  
    def vline(self, x: int, y: int, height: int, color: int | tuple):
        pygame.draw.line(surface=self.display,color=color,start_pos=(x,y),end_pos=(x,y+height))

    def pixel(self,x: int, y: int, color: int | tuple | None = None):
        pygame.draw.line(surface=self.display,color=color,start_pos=(x,y),end_pos=(x,y))

    def show(self):
        pygame.display.flip()
        