import os
import pygame
from pygame import mixer

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