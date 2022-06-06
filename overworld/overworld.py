from typing import List
from level import Level
import pygame,os,random
from overworld.config import asset
from overworld.maprenderer import MapRenderer
from overworld.entity import Entity
from overworld.enemy import Mon
from overworld.menu import Menu
from fight.fight import Fight
from codeview.codeview import CodeView

def get_level_list()-> List:
    return random.sample({f.path for f in os.scandir(os.getcwd()+'/overworld/assets/levels')},5)

class OverWorld(Level):
    def __init__(self):
        self.state = 0#1
        self.fight = Fight()
        self.code = CodeView()
        self.menu = Menu()
        maps = get_level_list()
        self.maprenderer = MapRenderer(asset,maps)
        self.load_map()
        #self.fight.reset(("m", 1))#delete later !!!!!!!!!!!!!!!!!!!!!!!!!

    def load_map(self):
        """Entities, Assign Variables etc"""
        self.entity = Entity(asset,self.maprenderer.done_map)
        self.monster = Mon(asset, self.maprenderer.done_map)  
        
    def update(self):
        """Update everything important"""
        if self.state == 0:   
            fight_tup = self.monster.update(self.maprenderer.walls, self.entity.playergroup)

            if fight_tup != None:
                self.fight.reset(fight_tup)
                self.state = 1
            
            self.menu.update()
        elif self.state == 1:
            self.fight.update()
        elif self.state == 2:
            self.code.update()

    def draw(self, screen):
        """Draw everything important on the screen."""
        if self.state == 0:
            self.maprenderer.draw(screen)
            self.entity.draw(screen)
            self.monster.draw(screen)
            self.menu.draw(screen)
        elif self.state == 1:
            self.fight.draw(screen)
        elif self.state == 2:
            self.code.draw(screen)
        #self.entity.draw(screen)

    def give_event(self,event):
        """Get the Events and handle them"""
        if self.state == 0:
            if event.type == pygame.KEYDOWN:
                self.entity.move(event, self.maprenderer.walls)
                if self.maprenderer.checkend(self.entity.playergroup):
                    self.load_map()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.menu.is_mouse_on_code():
                    self.code.reset()
                    self.state = 2
        elif self.state == 1:
            result = self.fight.give_event(event)
            if result != None:
                if result:
                    print("gewonnen")#fill later
                else:
                    print("verloren")#fill later
                self.state = 0
        elif self.state == 2:
            if self.code.give_event(event):
                self.state = 0
            

