import pygame
import math  
import random  as random
from Settings import keybinds


pygame.init()
pygame.mixer.init()
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.NOFRAME)
screen_width = info.current_w
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.space_pressed = False
        super().__init__()
        self.health = 100
        self.max_health = 100  
        self.is_attacking = False  
        self.direction = True  # True for right, False for left
        
        # Player Idle Position images
        self.Idle_List = self.images_loader("graphic/Player/Idle/Idle", 10)
        self.scale_image(self.Idle_List)
        self.Idle_index = 0
        self.image = self.Idle_List[self.Idle_index]
        self.rect = self.image.get_rect(midbottom = (120, 800))
        self.hitbox = self.rect.inflate(-60, -40)  

        # Player run position images
        self.Run_List = self.images_loader("graphic/Player/Run/Run", 10)
        self.scale_image(self.Run_List)
        self.Run_index = 0  
        self.image = self.Run_List[self.Run_index]

        # player jump images
        self.Jump_List = self.images_loader("graphic/Player/Jump/Jump", 3)
        self.scale_image(self.Jump_List)
        self.Jump_index = 0
        self.gravity = 0
        self.image = self.Jump_List[self.Jump_index]
       
        # player Normal attack images
        self.attack_list = self.images_loader("graphic/Player/Player_Attack_1/n_attack", 4)
        self.attack_index = 0
        self.scale_image(self.attack_list)
        self.image = self.attack_list[self.attack_index]

        # player Slide images
        self.slide_list = self.images_loader("graphic/Player/Slide/Slide",4)
        self.scale_image(self.slide_list)
        self.slide_index = 0    
        self.image = self.slide_list[self.slide_index]

        # player Crouch images
        self.crouch_list = self.images_loader("graphic/Player/Crouch/Crouch",3)
        self.scale_image(self.crouch_list)  
        self.crouch_index = 0  
        self.image = self.crouch_list[self.crouch_index]

        # player TurnAround images
        self.Turn_list = self.images_loader("graphic/Player/TurnAround/TurnAround",3)
        self.scale_image(self.Turn_list)  
        self.Turn_index = 0 

        self.total_Flask = 3
        self.last_flask_use = 0
        self.flask_cooldown = 1000  # milliseconds (1 sec between uses)
         # --- Healing Flask setup ---
        self.Flask = pygame.image.load('graphic/Player/HUD/Health_Flask.png').convert_alpha()
        self.Flask = pygame.transform.scale(
            self.Flask,(int(self.Flask.get_width() * 3), int(self.Flask.get_height() * 3))
        )
        

    def Healing_Flask(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        # Check for key press and cooldown
        if keys[keybinds['heal']] and self.total_Flask > 0 and self.max_health > self.health and current_time - self.last_flask_use > self.flask_cooldown:
            self.health = self.max_health
            self.total_Flask -= 1
            self.last_flask_use = current_time

    def Draw_Flasks(self, surface):
        for i in range(self.total_Flask):
            surface.blit(self.Flask, (50 + i * 70, 100)) 
        
        
    def collide(self,Enemy):
        if self.hitbox.colliderect(Enemy.hitbox):
            if abs(Enemy.rect.centerx - self.rect.centerx) < 120:
                if Enemy.is_attacking:
                    self.health -=random.uniform(0.1,0.3)
                  
    # load images from a given path and number of images
    def images_loader(self,path,number):
        images = []
        for i in range(1,number+1):
            img = pygame.image.load(f'{path}_{i}.png').convert_alpha()
            images.append(img)
        return images
    
    # Handle player input for movement and actions`
    def player_input(self):
        key = pygame.key.get_pressed()
        mouse_Button = pygame.mouse.get_pressed()

        # Jump
        if key[keybinds['jump']] and self.space_pressed == False:
            self.gravity = -20
            self.space_pressed = True

        # Move Right
        if key[keybinds['move_right']]:
            if not self.direction:  # if facing left before
                self.direction = True
                self.Player_filp_animation()  # flip to face right
            self.rect.x += 5

        # Move Left
        elif key[keybinds['move_left']]:
            if self.direction:  # if facing right before
                self.direction = False
                self.Player_filp_animation()  # flip to face left
            self.rect.x -= 5
        
        # Slide
        elif key[keybinds['slide']]:
            if self.direction:  self.rect.x += 10
            else : self.rect.x -= 10
        else:
            pass

    # Scale images by a factor of certain amount 
    def scale_image(self,list):
        for i in range (len(list)):
            x = int(list[i].get_width() *5)
            y = int(list[i].get_height() *5)
            list[i] = pygame.transform.scale(list[i], (x, y))   
        return list 
    
    #` Apply gravity to the player for jumping and falling
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 800:	
            self.rect.bottom = 800
            self.gravity = 0         
            self.space_pressed = False

    # Flip player images horizontally
    def player_flip(self,list):
        for i in range(len(list)):
            list[i] = pygame.transform.flip(list[i], True, False)
        return list
    
    # Flip all player animations when changing direction
    def Player_filp_animation(self):
        self.Idle_List = self.player_flip(self.Idle_List)
        self.Run_List = self.player_flip(self.Run_List)
        self.Jump_List = self.player_flip(self.Jump_List)
        self.attack_list = self.player_flip(self.attack_list)
        self.slide_list = self.player_flip(self.slide_list)
        self.crouch_list = self.player_flip(self.crouch_list)
        self.Turn_list = self.player_flip(self.Turn_list)


    # Update player animation state based on actions
    def player_animation_state(self):
        keys = pygame.key.get_pressed()
        mouse_Button = pygame.mouse.get_pressed()
        if mouse_Button[0]:
            self.is_attacking = True  
            self.attack_index += 0.2
            if self.attack_index >= len(self.attack_list): 
                self.attack_index = 0
            self.image = self.attack_list[int(self.attack_index)]
        elif self.rect.bottom < 800:
            self.is_attacking = False 
            self.Jump_index += 0.1
            if self.Jump_index >= len(self.Jump_List): self.Jump_index = 0
            self.image = self.Jump_List[int(self.Jump_index)]
       
        elif keys[keybinds['move_right']] or keys[keybinds['move_left']]: 
            self.is_attacking = False 
            self.Run_index +=0.1
            if self.Run_index >= len(self.Run_List): self.Run_index =0
            self.image = self.Run_List[int(self.Run_index)]
        
        elif keys[keybinds['slide']]:
            self.is_attacking = False 
            self.slide_index +=0.2
            if self.slide_index >= len(self.slide_list): self.slide_index =0
            self.image = self.slide_list[int(self.slide_index)]
        
        elif keys[keybinds['crouch']]:
            self.is_attacking = False 
            self.crouch_index +=0.1
            if self.crouch_index >= len(self.crouch_list): self.crouch_index =0
            self.image = self.crouch_list[int(self.crouch_index)]
        else:
            self.is_attacking = False 
            self.Idle_index += 0.1
            if self.Idle_index >= len(self.Idle_List): self.Idle_index = 0
            self.image = self.Idle_List[int(self.Idle_index)]
            
    def draw_health_bar(self,screen):
        Bar_Background = pygame.image.load('graphic/Player/HUD/bar_background.png').convert_alpha()
        Bar_Background = pygame.transform.scale(Bar_Background,(int(Bar_Background.get_width()*5),int(Bar_Background.get_height()*10)))
        Bar = pygame.image.load('graphic/Player/HUD/bar.png').convert_alpha()
        Bar = pygame.transform.scale(Bar,(int(Bar.get_width()*5),int(Bar.get_height()*5)))
        screen.blit(Bar_Background, (50, 10))
        bar_width = Bar.get_width()*0.9
        fill = (self.health / self.max_health) * bar_width
        fill_rect = pygame.Rect(30, 15, fill, Bar.get_height()*0.7)
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
        screen.blit(Bar,(10,10) )

  
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.player_animation_state()
        self.Healing_Flask()
        self.hitbox.midbottom = self.rect.midbottom 

    def reset(self):
        self.health = self.max_health
        self.rect = self.image.get_rect(midbottom = (120, 800))
        self.gravity = 0         
        self.space_pressed = False
        self.is_attacking = False
        self.total_Flask = 3