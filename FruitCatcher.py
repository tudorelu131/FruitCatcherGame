import pygame
from pygame.locals import *
from pygame.math import Vector2
import random

class Item:
    x: int
    y: int
    bad: int
    pos: Vector2
    def __init__(self):
        self.x, self.y = random.randint(0,18), -20
        self.bad = random.randint(0,100)
        self.item_img = None
        
    def load_image(self):
        if self.bad < 30:
            self.item_img = pygame.image.load('Assets/bomb_30x30.png')
        else:
            self.item_img = pygame.image.load('Assets/apple_30x30.png')

    def draw_item(self, screen: pygame.Surface):
        self.item_rect = pygame.Rect(self.x * 20, self.y, 30, 30)
        self.load_image()
        screen.blit(self.item_img, self.item_rect)

class Player:
    x: int
    y: int
    pos: Vector2
    size = width, height = 100, 50
    rect: pygame.Rect
    
    def __init__(self):
        self.basket = None
        self.rect = pygame.Rect(275, 370, 50, 30)
        self.x = 275
        self.y = 370
    
    def load_images(self):
        self.player_img = pygame.image.load('Assets/basket_50x30.png')
        
    def draw_player(self, screen: pygame.Surface):
        x_pos = self.x
        y_pos = self.y
        player_rect = pygame.Rect(x_pos, y_pos, self.width, self.height)
        screen.blit(self.player_img, player_rect)
    
class Game:
    _screen_update = pygame.USEREVENT
    _add_item = pygame.USEREVENT
    _clock = pygame.time.Clock()
    _game_area = pygame.Surface((400,400))
    _game_rect = pygame.Rect(20,100,400,400)
    items: list
    size = ()
    
    def __init__(self):
        first_item = Item()
        self._running = True
        self._game_over_state = False
        self._score = 0
        self._screen = None
        self._size = self.width, self.height = 440, 520
        self._player = Player()
        self.items = [first_item]
        self._item = None
        self._font = None
    
    def on_init(self):
        pygame.init()
        pygame.time.set_timer(self._add_item, 800)
        self._screen = pygame.display.set_mode(self._size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        
        self._player = Player()
        self._player.load_images()
        
        self._font = pygame.font.SysFont('impact', 40)
        pygame.display.set_caption('Fruit Catcher')
        self._font_render = self._font.render(f"Score: {self._score}", True, pygame.Color('BLACK'), None)
        self._font_rect = (20, 50)
        
    def on_event(self, event: pygame.event):
        if event.type == pygame.QUIT:
            self._running =  False
            
        if event.type == self._add_item:
            self.add_item()
    
    def on_render(self):
        self._game_area.fill(pygame.Color(100, 100, 200))
        for currItem in self.items:
            currItem.draw_item(self._game_area)
            
    def move_player(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self._player.x < 350:
            self._player.x += 5
            self._player.rect.x += 5
        if keys[pygame.K_LEFT] and self._player.x > 0:
            self._player.x -= 5
            self._player.rect.x -= 5
            
    def on_cleanup(self):
        pygame.quit
        
    def add_item(self):
        new_item = Item()
        self.items.append(new_item)
        
    def move_items(self):
        for index, currItem in enumerate(self.items):
            currItem.y += 3
            currItem.item_rect.y += 3
        
        self.items = [item for item in self.items if item.y <= 400]
        
    def check_collision(self):
        items_to_remove = []
        for index, currItem in enumerate(self.items):
            if(pygame.Rect.colliderect(self._player.rect, currItem.item_rect)):
                items_to_remove.append(index)
                if currItem.bad > 30:
                    self._score += 10
                else:
                    self._game_over_state = True
                    self._font_render = self._font.render(f"You lost. Final Score: {self._score}", True, pygame.Color('BLACK'), None)
                    self._font_rect = (20, 200)
                if not self._game_over_state:
                    self._font_render = self._font.render(f"Score: {self._score}", True, pygame.Color('BLACK'), None)
        
        for index in reversed(items_to_remove):
            del self.items[index]
                
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
            
        while self._running:
            self._screen.fill(pygame.Color(0, 85, 120))
            
            for event in pygame.event.get():
                self.on_event(event)
            
            if not self._game_over_state:    
                self.on_render()
                self.move_items()
                self.move_player()
                self._player.draw_player(self._game_area)
                self.check_collision()
                self._screen.blit(self._game_area, self._game_rect)
            else:
                self.on_render()
            
            self._screen.blit(self._font_render, self._font_rect)
            pygame.display.update()
            self._clock.tick(60)
            
        self.on_cleanup()
        
if __name__ == "__main__":
    FruitCatcher = Game()
    FruitCatcher.on_execute()
    
    